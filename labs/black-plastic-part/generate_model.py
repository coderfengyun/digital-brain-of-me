"""Generate a printable approximation of the photographed black plastic part."""

from pathlib import Path
import struct

import numpy as np
from skimage import measure


# All dimensions are millimetres.
LENGTH = 12.5
OUTER_DIAMETER = 8.0
INNER_DIAMETER = 6.0
SIDE_HOLE_DIAMETER = 3.0
INTERNAL_SLOT_WIDTH = 2.0

# The photo shows a subtle waist. 0.25 mm preserves a printable wall.
WAIST_DEPTH = 0.25
VOXEL = 0.06
MARGIN = 1.0


def field(x: np.ndarray, y: np.ndarray, z: np.ndarray) -> np.ndarray:
    """Negative values are material; positive values are empty space."""
    half_length = LENGTH / 2
    outer_radius = OUTER_DIAMETER / 2
    inner_radius = INNER_DIAMETER / 2

    # Rounded end rims with a gentle central waist, matching the reference.
    axial = np.clip(np.abs(z) / half_length, 0.0, 1.0)
    local_radius = outer_radius - WAIST_DEPTH * (1.0 - axial**2)
    outer = np.maximum(np.sqrt(x * x + y * y) - local_radius, np.abs(z) - half_length)

    # Main axial bore and the 3 mm transverse through-hole.
    axial_bore = inner_radius - np.sqrt(x * x + y * y)
    side_hole = SIDE_HOLE_DIAMETER / 2 - np.sqrt(y * y + z * z)

    # A 2 mm-wide internal rectangular relief aligned with the main bore.
    # It lies within the 6 mm bore, so it records the supplied dimension while
    # keeping the functional opening circular and easy to tune later.
    slot = np.minimum(INTERNAL_SLOT_WIDTH / 2 - np.abs(x), inner_radius - np.abs(y))
    voids = np.maximum.reduce([axial_bore, side_hole, slot])
    return np.maximum(outer, voids)


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

    volume = field(x, y, z)
    vertices, faces, _, _ = measure.marching_cubes(volume, level=0.0, spacing=(VOXEL,) * 3)
    vertices += np.array([xs[0], ys[0], zs[0]], dtype=np.float32)

    write_binary_stl(output_dir / "black_plastic_part.stl", vertices, faces)
    print(f"Wrote {len(vertices):,} vertices and {len(faces):,} triangles")


if __name__ == "__main__":
    main()
