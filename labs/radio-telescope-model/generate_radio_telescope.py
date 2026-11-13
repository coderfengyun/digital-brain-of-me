"""Generate a stylised, printable radio telescope from a single reference image.

The geometry is intentionally self-contained: it uses only NumPy and the Python
standard library, and writes both STL and standards-compliant 3MF files.
All dimensions are millimetres.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
import math
import struct
import zipfile
from xml.etree import ElementTree as ET

import numpy as np


OUT_DIR = Path(__file__).resolve().parent / "generated"


@dataclass
class Mesh:
    name: str
    color: str
    vertices: list[tuple[float, float, float]] = field(default_factory=list)
    faces: list[tuple[int, int, int]] = field(default_factory=list)

    def add(self, vertices: np.ndarray, faces: np.ndarray) -> None:
        offset = len(self.vertices)
        self.vertices.extend(map(tuple, np.asarray(vertices, dtype=float)))
        self.faces.extend(tuple(int(i) + offset for i in face) for face in faces)


def _basis(direction: np.ndarray) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    w = np.asarray(direction, dtype=float)
    w /= np.linalg.norm(w)
    helper = np.array([1.0, 0.0, 0.0])
    if abs(float(np.dot(w, helper))) > 0.9:
        helper = np.array([0.0, 1.0, 0.0])
    u = np.cross(w, helper)
    u /= np.linalg.norm(u)
    v = np.cross(w, u)
    return u, v, w


def frustum(mesh: Mesh, p0, p1, r0: float, r1: float, segments: int = 20) -> None:
    """Add a capped round frustum aligned between two points."""
    p0 = np.asarray(p0, dtype=float)
    p1 = np.asarray(p1, dtype=float)
    u, v, _ = _basis(p1 - p0)
    verts = []
    for point, radius in ((p0, r0), (p1, r1)):
        for i in range(segments):
            angle = 2 * math.pi * i / segments
            verts.append(point + radius * (math.cos(angle) * u + math.sin(angle) * v))
    verts.extend([p0, p1])
    faces = []
    for i in range(segments):
        j = (i + 1) % segments
        faces.extend([(i, j, segments + j), (i, segments + j, segments + i)])
        faces.append((2 * segments, j, i))
        faces.append((2 * segments + 1, segments + i, segments + j))
    mesh.add(np.asarray(verts), np.asarray(faces))


def cylinder(mesh: Mesh, p0, p1, radius: float, segments: int = 16) -> None:
    frustum(mesh, p0, p1, radius, radius, segments)


def beam(mesh: Mesh, p0, p1, width: float, depth: float | None = None) -> None:
    """Add a capped rectangular beam between arbitrary points."""
    if depth is None:
        depth = width
    p0 = np.asarray(p0, dtype=float)
    p1 = np.asarray(p1, dtype=float)
    u, v, _ = _basis(p1 - p0)
    corners = []
    for point in (p0, p1):
        corners.extend([
            point - u * width / 2 - v * depth / 2,
            point + u * width / 2 - v * depth / 2,
            point + u * width / 2 + v * depth / 2,
            point - u * width / 2 + v * depth / 2,
        ])
    faces = [
        (0, 2, 1), (0, 3, 2), (4, 5, 6), (4, 6, 7),
        (0, 1, 5), (0, 5, 4), (1, 2, 6), (1, 6, 5),
        (2, 3, 7), (2, 7, 6), (3, 0, 4), (3, 4, 7),
    ]
    mesh.add(np.asarray(corners), np.asarray(faces))


def box(mesh: Mesh, center, size) -> None:
    center = np.asarray(center, dtype=float)
    sx, sy, sz = np.asarray(size, dtype=float) / 2
    verts = np.asarray([
        [-sx, -sy, -sz], [sx, -sy, -sz], [sx, sy, -sz], [-sx, sy, -sz],
        [-sx, -sy, sz], [sx, -sy, sz], [sx, sy, sz], [-sx, sy, sz],
    ]) + center
    faces = np.asarray([
        (0, 2, 1), (0, 3, 2), (4, 5, 6), (4, 6, 7),
        (0, 1, 5), (0, 5, 4), (1, 2, 6), (1, 6, 5),
        (2, 3, 7), (2, 7, 6), (3, 0, 4), (3, 4, 7),
    ])
    mesh.add(verts, faces)


def dish(mesh: Mesh, vertex, normal, radius=60.0, depth=26.0,
         thickness=2.0, radial_steps=18, segments=96) -> tuple[np.ndarray, np.ndarray, np.ndarray, float]:
    """Add a closed parabolic reflector shell and return its local frame."""
    origin = np.asarray(vertex, dtype=float)
    normal = np.asarray(normal, dtype=float)
    normal /= np.linalg.norm(normal)
    # Keep one dish axis horizontal for an intentional, reference-like tilt.
    u = np.array([1.0, 0.0, 0.0])
    v = np.cross(normal, u)
    v /= np.linalg.norm(v)
    u = np.cross(v, normal)
    focal_length = radius * radius / (4 * depth)

    verts: list[np.ndarray] = [origin, origin - thickness * normal]
    inner_rings: list[list[int]] = []
    outer_rings: list[list[int]] = []
    for step in range(1, radial_steps + 1):
        r = radius * step / radial_steps
        z = r * r / (4 * focal_length)
        inner, outer = [], []
        for i in range(segments):
            a = 2 * math.pi * i / segments
            radial = r * (math.cos(a) * u + math.sin(a) * v)
            inner.append(len(verts))
            verts.append(origin + radial + z * normal)
            outer.append(len(verts))
            verts.append(origin + radial + (z - thickness) * normal)
        inner_rings.append(inner)
        outer_rings.append(outer)

    faces: list[tuple[int, int, int]] = []
    first_inner, first_outer = inner_rings[0], outer_rings[0]
    for i in range(segments):
        j = (i + 1) % segments
        faces.append((0, first_inner[i], first_inner[j]))
        faces.append((1, first_outer[j], first_outer[i]))
    for ring in range(radial_steps - 1):
        a_i, b_i = inner_rings[ring], inner_rings[ring + 1]
        a_o, b_o = outer_rings[ring], outer_rings[ring + 1]
        for i in range(segments):
            j = (i + 1) % segments
            faces.extend([(a_i[i], b_i[i], b_i[j]), (a_i[i], b_i[j], a_i[j])])
            faces.extend([(a_o[i], b_o[j], b_o[i]), (a_o[i], a_o[j], b_o[j])])
    rim_i, rim_o = inner_rings[-1], outer_rings[-1]
    for i in range(segments):
        j = (i + 1) % segments
        faces.extend([(rim_i[i], rim_o[i], rim_o[j]), (rim_i[i], rim_o[j], rim_i[j])])
    mesh.add(np.asarray(verts), np.asarray(faces))
    return u, v, normal, focal_length


def build_model() -> list[Mesh]:
    silver = Mesh("Reflector", "#BFC7CE")
    dark = Mesh("Frame", "#303840")
    charcoal = Mesh("Base", "#4A535B")

    # Four feet and square azimuth frame.
    for x in (-27, 27):
        for y in (-27, 27):
            box(charcoal, (x, y, 6), (13, 13, 12))
    for y in (-26, 26):
        beam(charcoal, (-31, y, 15), (31, y, 15), 6, 6)
    for x in (-26, 26):
        beam(charcoal, (x, -31, 15), (x, 31, 15), 6, 6)

    # Tapered pedestal, neck and four stabilising braces.
    frustum(charcoal, (0, 0, 15), (0, 0, 55), 12.0, 7.5, 28)
    cylinder(charcoal, (0, 0, 53), (0, 0, 72), 6.5, 24)
    for x, y in ((-25, -25), (25, -25), (25, 25), (-25, 25)):
        cylinder(dark, (x, y, 17), (0, 0, 49), 2.2, 12)
    cylinder(dark, (-17, 0, 68), (17, 0, 68), 4.0, 18)

    # Parabolic reflector. Its aperture tilts toward -Y, matching the photo.
    vertex = np.array([0.0, 0.0, 72.0])
    normal = np.array([0.0, -0.42, 0.907])
    u, v, n, focal = dish(silver, vertex, normal)

    def local_point(r: float, angle: float, z_extra: float = 0.0) -> np.ndarray:
        z = r * r / (4 * focal) + z_extra
        return vertex + r * (math.cos(angle) * u + math.sin(angle) * v) + z * n

    # Rear rim truss: an outer polygon plus alternating triangular braces.
    truss_angles = np.linspace(0, 2 * math.pi, 13)[:-1]
    outer_points = [local_point(60, a, -2.8) for a in truss_angles]
    inner_points = [local_point(45, a, -7.0) for a in truss_angles]
    for i in range(12):
        j = (i + 1) % 12
        cylinder(dark, outer_points[i], outer_points[j], 1.35, 10)
        cylinder(dark, inner_points[i], inner_points[j], 1.25, 10)
        cylinder(dark, outer_points[i], inner_points[i], 1.2, 10)
        cylinder(dark, inner_points[i], outer_points[j], 1.1, 10)

    # Feed horn at the focus with three support struts.
    focus = vertex + focal * n
    for angle in (math.radians(20), math.radians(160), math.radians(270)):
        anchor = local_point(57, angle, 1.0)
        cylinder(dark, anchor, focus - 2.5 * n, 1.45, 12)
    cylinder(dark, focus - 5.0 * n, focus + 5.0 * n, 2.7, 18)
    frustum(dark, focus + 4.0 * n, focus + 9.0 * n, 3.0, 4.8, 20)

    # Compact rear hub connecting the reflector to the elevation axis.
    cylinder(dark, vertex - 8.0 * n, vertex + 2.0 * n, 5.0, 20)
    cylinder(dark, (-14, 0, 70), (14, 0, 70), 3.2, 16)

    return [silver, dark, charcoal]


def write_stl(path: Path, meshes: list[Mesh]) -> None:
    triangle_count = sum(len(mesh.faces) for mesh in meshes)
    with path.open("wb") as fh:
        fh.write(b"Stylised radio telescope; units millimetres".ljust(80, b" "))
        fh.write(struct.pack("<I", triangle_count))
        for mesh in meshes:
            verts = np.asarray(mesh.vertices, dtype=np.float32)
            for face in mesh.faces:
                tri = verts[list(face)]
                normal = np.cross(tri[1] - tri[0], tri[2] - tri[0])
                norm = np.linalg.norm(normal)
                if norm:
                    normal /= norm
                fh.write(struct.pack("<12fH", *(normal.tolist() + tri.reshape(-1).tolist()), 0))


def write_3mf(path: Path, meshes: list[Mesh]) -> None:
    ns = "http://schemas.microsoft.com/3dmanufacturing/core/2015/02"
    ET.register_namespace("", ns)
    model = ET.Element(f"{{{ns}}}model", {"unit": "millimeter", "xml:lang": "en-US"})
    ET.SubElement(model, f"{{{ns}}}metadata", {"name": "Title"}).text = "Radio Telescope"
    ET.SubElement(model, f"{{{ns}}}metadata", {"name": "Designer"}).text = "OpenAI Codex"
    resources = ET.SubElement(model, f"{{{ns}}}resources")
    materials = ET.SubElement(resources, f"{{{ns}}}basematerials", {"id": "1"})
    for mesh in meshes:
        ET.SubElement(materials, f"{{{ns}}}base", {"name": mesh.name, "displaycolor": mesh.color})
    build = ET.SubElement(model, f"{{{ns}}}build")
    for object_id, mesh_data in enumerate(meshes, start=2):
        obj = ET.SubElement(resources, f"{{{ns}}}object", {
            "id": str(object_id), "name": mesh_data.name, "type": "model",
            "pid": "1", "pindex": str(object_id - 2),
        })
        mesh_node = ET.SubElement(obj, f"{{{ns}}}mesh")
        vertices_node = ET.SubElement(mesh_node, f"{{{ns}}}vertices")
        for x, y, z in mesh_data.vertices:
            ET.SubElement(vertices_node, f"{{{ns}}}vertex", {
                "x": f"{x:.5f}", "y": f"{y:.5f}", "z": f"{z:.5f}",
            })
        triangles_node = ET.SubElement(mesh_node, f"{{{ns}}}triangles")
        for a, b, c in mesh_data.faces:
            ET.SubElement(triangles_node, f"{{{ns}}}triangle", {
                "v1": str(a), "v2": str(b), "v3": str(c),
            })
        ET.SubElement(build, f"{{{ns}}}item", {"objectid": str(object_id)})

    content_types = b'''<?xml version="1.0" encoding="UTF-8"?>
<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">
  <Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>
  <Default Extension="model" ContentType="application/vnd.ms-package.3dmanufacturing-3dmodel+xml"/>
</Types>'''
    relationships = b'''<?xml version="1.0" encoding="UTF-8"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Target="/3D/3dmodel.model" Id="rel-1" Type="http://schemas.microsoft.com/3dmanufacturing/2013/01/3dmodel"/>
</Relationships>'''
    model_xml = ET.tostring(model, encoding="utf-8", xml_declaration=True)
    with zipfile.ZipFile(path, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        archive.writestr("[Content_Types].xml", content_types)
        archive.writestr("_rels/.rels", relationships)
        archive.writestr("3D/3dmodel.model", model_xml)


def validate(meshes: list[Mesh]) -> None:
    for mesh in meshes:
        vertices = np.asarray(mesh.vertices)
        faces = np.asarray(mesh.faces)
        if not np.isfinite(vertices).all():
            raise ValueError(f"{mesh.name}: non-finite vertex")
        triangles = vertices[faces]
        areas = np.linalg.norm(np.cross(triangles[:, 1] - triangles[:, 0],
                                        triangles[:, 2] - triangles[:, 0]), axis=1)
        if np.any(areas < 1e-8):
            raise ValueError(f"{mesh.name}: degenerate triangle")


def scaled_copy(meshes: list[Mesh], factor: float) -> list[Mesh]:
    """Return a uniformly scaled copy while preserving object names and colours."""
    result = []
    for mesh in meshes:
        scaled = Mesh(mesh.name, mesh.color)
        scaled.vertices = [tuple(np.asarray(vertex) * factor) for vertex in mesh.vertices]
        scaled.faces = list(mesh.faces)
        result.append(scaled)
    return result


def write_preview(path: Path, meshes: list[Mesh]) -> None:
    import matplotlib.pyplot as plt
    from mpl_toolkits.mplot3d.art3d import Poly3DCollection

    fig = plt.figure(figsize=(8, 8), dpi=160)
    ax = fig.add_subplot(111, projection="3d")
    for mesh in meshes:
        vertices = np.asarray(mesh.vertices)
        faces = np.asarray(mesh.faces)
        # Decimate only the preview, never the exported model.
        step = max(1, len(faces) // 6000)
        poly = Poly3DCollection(vertices[faces[::step]], linewidths=0.04,
                                edgecolors="#20262b", alpha=1.0)
        poly.set_facecolor(mesh.color)
        ax.add_collection3d(poly)
    all_vertices = np.vstack([np.asarray(mesh.vertices) for mesh in meshes])
    mins, maxs = all_vertices.min(axis=0), all_vertices.max(axis=0)
    center = (mins + maxs) / 2
    span = float((maxs - mins).max()) * 0.55
    ax.set(xlim=(center[0] - span, center[0] + span),
           ylim=(center[1] - span, center[1] + span),
           zlim=(0, 2 * span), xlabel="X (mm)", ylabel="Y (mm)", zlabel="Z (mm)")
    ax.set_box_aspect((1, 1, 1.25))
    ax.view_init(elev=22, azim=-55)
    ax.set_title("Printable Radio Telescope")
    fig.tight_layout()
    fig.savefig(path, bbox_inches="tight")
    plt.close(fig)


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    meshes = build_model()
    validate(meshes)
    write_stl(OUT_DIR / "radio_telescope.stl", meshes)
    write_3mf(OUT_DIR / "radio_telescope.3mf", meshes)
    # Safe near-maximum size for the user's 256 x 256 x 256 mm Bambu Lab A1.
    # At 190%, the model is about 233 x 212 x 230 mm, leaving room for supports.
    write_3mf(OUT_DIR / "radio_telescope_A1_190pct.3mf", scaled_copy(meshes, 1.9))
    write_preview(OUT_DIR / "radio_telescope_preview.png", meshes)
    vertices = sum(len(mesh.vertices) for mesh in meshes)
    faces = sum(len(mesh.faces) for mesh in meshes)
    all_vertices = np.vstack([np.asarray(mesh.vertices) for mesh in meshes])
    extent = all_vertices.max(axis=0) - all_vertices.min(axis=0)
    print(f"Generated {vertices:,} vertices / {faces:,} triangles")
    print("Size: " + " x ".join(f"{value:.1f}" for value in extent) + " mm")


if __name__ == "__main__":
    main()
