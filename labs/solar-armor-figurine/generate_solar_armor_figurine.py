#!/usr/bin/env python3
"""Generate a printable full-body solar-armor hero figurine as an ASCII STL.

The model is a fan-made, printable approximation of an Arc-style solar armor
hero silhouette: silver/red suit, raised fists, large sun chest armor, shoulder
guards, and wing-like forearm armor. Units are millimeters.
"""

from __future__ import annotations

import math
from pathlib import Path

import numpy as np


ROOT = Path(__file__).resolve().parent
OUT = ROOT / "generated" / "arc_solar_armor_full_figurine.stl"


class Mesh:
    def __init__(self) -> None:
        self.tris: list[np.ndarray] = []

    def add(self, tri: list[list[float]] | np.ndarray) -> None:
        self.tris.append(np.asarray(tri, dtype=float))

    def extend(self, other: "Mesh") -> None:
        self.tris.extend(other.tris)

    def transformed(self, matrix: np.ndarray, offset: np.ndarray) -> "Mesh":
        out = Mesh()
        for tri in self.tris:
            out.add(tri @ matrix.T + offset)
        return out


def unit(v: np.ndarray) -> np.ndarray:
    n = np.linalg.norm(v)
    if n == 0:
        return v
    return v / n


def basis_from_z(direction: np.ndarray) -> np.ndarray:
    z = unit(direction)
    helper = np.array([0.0, 1.0, 0.0]) if abs(z[1]) < 0.9 else np.array([1.0, 0.0, 0.0])
    x = unit(np.cross(helper, z))
    y = unit(np.cross(z, x))
    return np.column_stack([x, y, z])


def normal(tri: np.ndarray) -> np.ndarray:
    n = np.cross(tri[1] - tri[0], tri[2] - tri[0])
    return unit(n)


def ellipsoid(center, radii, seg=28, rings=14) -> Mesh:
    cx, cy, cz = center
    rx, ry, rz = radii
    verts = []
    for i in range(rings + 1):
        theta = math.pi * i / rings
        row = []
        for j in range(seg):
            phi = 2 * math.pi * j / seg
            row.append(
                np.array(
                    [
                        cx + rx * math.sin(theta) * math.cos(phi),
                        cy + ry * math.sin(theta) * math.sin(phi),
                        cz + rz * math.cos(theta),
                    ]
                )
            )
        verts.append(row)
    mesh = Mesh()
    for i in range(rings):
        for j in range(seg):
            a = verts[i][j]
            b = verts[i][(j + 1) % seg]
            c = verts[i + 1][(j + 1) % seg]
            d = verts[i + 1][j]
            if i == 0:
                mesh.add([a, c, d])
            elif i == rings - 1:
                mesh.add([a, b, d])
            else:
                mesh.add([a, b, c])
                mesh.add([a, c, d])
    return mesh


def cylinder_between(a, b, radius, seg=24, r2=None) -> Mesh:
    a = np.asarray(a, dtype=float)
    b = np.asarray(b, dtype=float)
    r2 = radius if r2 is None else r2
    axis = b - a
    rot = basis_from_z(axis)
    height = np.linalg.norm(axis)
    verts0 = []
    verts1 = []
    for i in range(seg):
        phi = 2 * math.pi * i / seg
        p0 = np.array([radius * math.cos(phi), radius * math.sin(phi), 0.0])
        p1 = np.array([r2 * math.cos(phi), r2 * math.sin(phi), height])
        verts0.append(rot @ p0 + a)
        verts1.append(rot @ p1 + a)
    mesh = Mesh()
    for i in range(seg):
        j = (i + 1) % seg
        mesh.add([verts0[i], verts0[j], verts1[j]])
        mesh.add([verts0[i], verts1[j], verts1[i]])
        mesh.add([a, verts0[i], verts0[j]])
        mesh.add([b, verts1[j], verts1[i]])
    return mesh


def box(center, size) -> Mesh:
    c = np.asarray(center, dtype=float)
    sx, sy, sz = np.asarray(size, dtype=float) / 2
    pts = [
        [-sx, -sy, -sz],
        [sx, -sy, -sz],
        [sx, sy, -sz],
        [-sx, sy, -sz],
        [-sx, -sy, sz],
        [sx, -sy, sz],
        [sx, sy, sz],
        [-sx, sy, sz],
    ]
    v = [c + np.asarray(p) for p in pts]
    faces = [
        [0, 1, 2, 3],
        [4, 7, 6, 5],
        [0, 4, 5, 1],
        [1, 5, 6, 2],
        [2, 6, 7, 3],
        [3, 7, 4, 0],
    ]
    mesh = Mesh()
    for f in faces:
        mesh.add([v[f[0]], v[f[1]], v[f[2]]])
        mesh.add([v[f[0]], v[f[2]], v[f[3]]])
    return mesh


def triangular_prism(points2d, z0, z1) -> Mesh:
    p = [np.array([x, y, z0], dtype=float) for x, y in points2d]
    q = [np.array([x, y, z1], dtype=float) for x, y in points2d]
    mesh = Mesh()
    mesh.add([p[0], p[1], p[2]])
    mesh.add([q[0], q[2], q[1]])
    for i in range(3):
        j = (i + 1) % 3
        mesh.add([p[i], p[j], q[j]])
        mesh.add([p[i], q[j], q[i]])
    return mesh


def sun_crest(center=(0, -20.5, 92), radius=10.0) -> Mesh:
    mesh = Mesh()
    mesh.extend(cylinder_between([center[0], center[1] - 2, center[2]], [center[0], center[1] + 2, center[2]], radius, seg=32))
    for i in range(12):
        angle = 2 * math.pi * i / 12
        inner = radius * 0.85
        outer = radius * 1.85
        width = 0.18
        pts = [
            (center[0] + inner * math.cos(angle - width), center[2] + inner * math.sin(angle - width)),
            (center[0] + outer * math.cos(angle), center[2] + outer * math.sin(angle)),
            (center[0] + inner * math.cos(angle + width), center[2] + inner * math.sin(angle + width)),
        ]
        prism = triangular_prism(pts, center[1] - 3.0, center[1] + 3.0)
        # triangular_prism uses x/y as horizontal/vertical, then z as depth.
        remapped = Mesh()
        for tri in prism.tris:
            remapped.add([[v[0], v[2], v[1]] for v in tri])
        mesh.extend(remapped)
    return mesh


def armor_petal(center, angle, inner, outer, width, y0, y1) -> Mesh:
    cx, _, cz = center
    pts = [
        (cx + inner * math.cos(angle - width), cz + inner * math.sin(angle - width)),
        (cx + outer * math.cos(angle), cz + outer * math.sin(angle)),
        (cx + inner * math.cos(angle + width), cz + inner * math.sin(angle + width)),
    ]
    return xz_prism(pts, y0, y1)


def solar_breastplate() -> Mesh:
    mesh = Mesh()
    center = (0, -22, 91)
    for i in range(10):
        angle = math.radians(-155 + i * 34)
        mesh.extend(armor_petal(center, angle, 12.0, 24.0, 0.18, -22.8, -14.8))
    mesh.extend(xz_prism([(-22, 82), (-10, 112), (0, 103)], -21.5, -15.0))
    mesh.extend(xz_prism([(22, 82), (10, 112), (0, 103)], -21.5, -15.0))
    mesh.extend(xz_prism([(-15, 75), (0, 61), (15, 75)], -18.0, -12.8))
    mesh.extend(sun_crest(center=(0, -24.5, 93), radius=9.6))
    mesh.extend(cylinder_between([-18, -18, 101], [18, -18, 101], 2.4, seg=12))
    return mesh


def xz_prism(points_xz, y0, y1) -> Mesh:
    """Create a triangular prism from x/z points with thickness on the y axis."""
    raw = triangular_prism(points_xz, y0, y1)
    mesh = Mesh()
    for tri in raw.tris:
        mesh.add([[v[0], v[2], v[1]] for v in tri])
    return mesh


def helmet_crest() -> Mesh:
    mesh = xz_prism([(-4.8, 121), (0, 145), (4.8, 121)], -7.5, -1.5)
    mesh.extend(xz_prism([(-10, 125), (-4, 139), (-2, 124)], -6.8, -2.4))
    mesh.extend(xz_prism([(10, 125), (4, 139), (2, 124)], -6.8, -2.4))
    return mesh


def suit_relief_stripes() -> Mesh:
    mesh = Mesh()
    # Raised red suit bands: chest V, abdomen, and lower-leg slashes.
    mesh.extend(xz_prism([(-14, 99), (-5, 82), (-10, 80)], -17.5, -13.5))
    mesh.extend(xz_prism([(14, 99), (5, 82), (10, 80)], -17.5, -13.5))
    mesh.extend(xz_prism([(-9, 70), (0, 58), (9, 70)], -16.0, -12.5))
    mesh.extend(xz_prism([(-16, 38), (-8, 17), (-5, 42)], -8.0, -4.0))
    mesh.extend(xz_prism([(16, 38), (8, 17), (5, 42)], -8.0, -4.0))
    return mesh


def side_wing_armor(side: int) -> Mesh:
    sx = side
    mesh = Mesh()
    plates = [
        [(0, 0), (sx * 20, 5), (sx * 7, 22)],
        [(sx * 5, 5), (sx * 27, 9), (sx * 11, 28)],
        [(sx * 9, 12), (sx * 24, 19), (sx * 12, 34)],
    ]
    for pts in plates:
        wing = triangular_prism(pts, -2.8, 2.8)
        remapped = Mesh()
        for tri in wing.tris:
            remapped.add([[v[0] + sx * 30, v[2] - 6, v[1] + 102] for v in tri])
        mesh.extend(remapped)
    return mesh


def shoulder_sun_armor(side: int) -> Mesh:
    sx = side
    mesh = Mesh()
    mesh.extend(ellipsoid([sx * 26, -4, 106], [14, 9, 8], seg=24, rings=10))
    mesh.extend(xz_prism([(sx * 17, 104), (sx * 43, 114), (sx * 24, 124)], -7.2, 1.0))
    mesh.extend(xz_prism([(sx * 27, 111), (sx * 50, 124), (sx * 35, 132)], -6.4, -1.2))
    mesh.extend(xz_prism([(sx * 18, 99), (sx * 42, 96), (sx * 28, 107)], -7.0, -1.6))
    return mesh


def write_stl(mesh: Mesh, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="ascii") as f:
        f.write("solid solar_armor_hero_figurine\n")
        for tri in mesh.tris:
            n = normal(tri)
            f.write(f"  facet normal {n[0]:.6f} {n[1]:.6f} {n[2]:.6f}\n")
            f.write("    outer loop\n")
            for v in tri:
                f.write(f"      vertex {v[0]:.6f} {v[1]:.6f} {v[2]:.6f}\n")
            f.write("    endloop\n")
            f.write("  endfacet\n")
        f.write("endsolid solar_armor_hero_figurine\n")


def build_model() -> Mesh:
    m = Mesh()

    # Stable base and boots.
    m.extend(cylinder_between([0, 0, -4], [0, 0, 0], 39, seg=48))
    m.extend(cylinder_between([-12, -2, 0], [-12, -2, 14], 5.6, seg=20, r2=4.6))
    m.extend(cylinder_between([12, -2, 0], [12, -2, 14], 5.6, seg=20, r2=4.6))
    m.extend(box([-12, -8, 1.2], [17, 14, 3]))
    m.extend(box([12, -8, 1.2], [17, 14, 3]))

    # Legs, torso, waist, and neck.
    m.extend(cylinder_between([-12, -1, 12], [-7, -1, 58], 5.7, seg=20, r2=7.2))
    m.extend(cylinder_between([12, -1, 12], [7, -1, 58], 5.7, seg=20, r2=7.2))
    m.extend(ellipsoid([0, -1, 63], [18, 12, 10], seg=28, rings=12))
    m.extend(ellipsoid([0, -1, 85], [20, 13, 29], seg=32, rings=16))
    m.extend(cylinder_between([0, -1, 109], [0, -1, 116], 6, seg=20))

    # Head and helmet.
    m.extend(ellipsoid([0, -1, 127], [12.5, 10.5, 15.5], seg=32, rings=16))
    m.extend(helmet_crest())
    m.extend(ellipsoid([-6.2, -10.5, 130], [3.7, 1.2, 2.0], seg=14, rings=8))
    m.extend(ellipsoid([6.2, -10.5, 130], [3.7, 1.2, 2.0], seg=14, rings=8))
    m.extend(box([0, -11.6, 121.5], [8, 2, 2.5]))

    # Shoulders, arms, fists.
    for side in [-1, 1]:
        sx = side
        m.extend(shoulder_sun_armor(sx))
        m.extend(cylinder_between([sx * 25, -2, 101], [sx * 38, -3, 115], 5.6, seg=18, r2=5.0))
        m.extend(cylinder_between([sx * 38, -3, 115], [sx * 29, -6, 130], 5.1, seg=18, r2=4.5))
        m.extend(ellipsoid([sx * 28, -8, 133], [6.5, 5.2, 5.2], seg=18, rings=10))
        m.extend(side_wing_armor(sx))

    # Solar chest armor and lower red suit ridge.
    m.extend(solar_breastplate())
    m.extend(suit_relief_stripes())

    return m


def main() -> None:
    mesh = build_model()
    write_stl(mesh, OUT)
    print(f"Wrote {OUT}")
    print(f"Triangles: {len(mesh.tris)}")


if __name__ == "__main__":
    main()
