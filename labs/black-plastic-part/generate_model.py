"""Generate a printable approximation of the photographed black plastic part."""

from pathlib import Path
import struct

import numpy as np
from skimage import measure


# All dimensions are millimetres.
LENGTH = 12.5
OUTER_DIAMETER = 8.0
INNER_DIAMETER = 5.0
SIDE_HOLE_DIAMETER = 3.5
INTERNAL_SLOT_WIDTH = 2.0
INTERNAL_SLOT_HEIGHT = 5.0
COUNTERBORE_DEPTH = 4.0     # circular 5 mm recess from each end

# The photo shows a subtle waist. 0.25 mm preserves a printable wall.
WAIST_DEPTH = 0.25
VOXEL = 0.06
MARGIN = 1.0


def solid_mask(x: np.ndarray, y: np.ndarray, z: np.ndarray) -> np.ndarray:
    """Return a Boolean occupancy grid after all subtractive features."""
    half_length = LENGTH / 2
    outer_radius = OUTER_DIAMETER / 2
    inner_radius = INNER_DIAMETER / 2

    # Rounded end rims with a gentle central waist, matching the reference.
    axial = np.clip(np.abs(z) / half_length, 0.0, 1.0)
    local_radius = outer_radius - WAIST_DEPTH * (1.0 - axial**2)
    outer = (np.sqrt(x * x + y * y) <= local_radius) & (np.abs(z) <= half_length)

    # The 5 mm feature is a circular recess at each end, not a full bore.
    radial_inside = np.sqrt(x * x + y * y) <= inner_radius
    within_end_recess = np.abs(z) >= (half_length - COUNTERBORE_DEPTH)
    end_counterbores = radial_inside & within_end_recess

    # The rectangular opening seen inside the circular recess runs axially.
    axial_slot = ((np.abs(x) <= INTERNAL_SLOT_HEIGHT / 2)
                  & (np.abs(y) <= INTERNAL_SLOT_WIDTH / 2))
    side_hole = np.sqrt(y * y + z * z) <= SIDE_HOLE_DIAMETER / 2

    voids = end_counterbores | axial_slot | side_hole
    return outer & ~voids


def write_binary_stl(path: Path, vertices: np.ndarray, faces: np.ndarray) -> None:
    with path.open("wb") as fh:
        fh.write(b"black plastic part, dimensions in mm".ljust(80, b" "))
        fh.write(struct.pack("<I", len(faces)))
        for face in faces:
            tri = vertices[face]
            normal = np.cross(tri[1] - tri[0], tri[2] - tri[0])
            length = np.linalg.norm(normal)
            if length:
                normal /= length
            fh.write(struct.pack("<12fH", *(normal.tolist() + tri.reshape(-1).tolist()), 0))


def main() -> None:
    output_dir = Path(__file__).resolve().parent
    xy_limit = OUTER_DIAMETER / 2 + MARGIN
    z_limit = LENGTH / 2 + MARGIN
    xs = np.arange(-xy_limit, xy_limit + VOXEL, VOXEL, dtype=np.float32)
    ys = np.arange(-xy_limit, xy_limit + VOXEL, VOXEL, dtype=np.float32)
    zs = np.arange(-z_limit, z_limit + VOXEL, VOXEL, dtype=np.float32)
    x, y, z = np.meshgrid(xs, ys, zs, indexing="ij")

    volume = solid_mask(x, y, z).astype(np.uint8)
    vertices, faces, _, _ = measure.marching_cubes(volume, level=0.5, spacing=(VOXEL,) * 3)
    vertices += np.array([xs[0], ys[0], zs[0]], dtype=np.float32)

    # Merge numerically coincident marching-cubes vertices and remove any
    # collapsed/duplicate triangles at Boolean intersections.
    quantized = np.rint(vertices / 1e-5).astype(np.int64)
    _, first, inverse = np.unique(quantized, axis=0, return_index=True, return_inverse=True)
    vertices = vertices[first]
    faces = inverse[faces]
    valid = ((faces[:, 0] != faces[:, 1]) & (faces[:, 1] != faces[:, 2])
             & (faces[:, 2] != faces[:, 0]))
    faces = faces[valid]
    canonical = np.sort(faces, axis=1)
    _, unique_faces = np.unique(canonical, axis=0, return_index=True)
    faces = faces[np.sort(unique_faces)]

    # Place the model upright with its long axis perpendicular to the bed.
    upright = vertices.copy()
    upright[:, 2] -= upright[:, 2].min()
    write_binary_stl(output_dir / "black_plastic_part.stl", upright, faces)
    print(f"Wrote {len(vertices):,} vertices and {len(faces):,} triangles")


if __name__ == "__main__":
    main()
