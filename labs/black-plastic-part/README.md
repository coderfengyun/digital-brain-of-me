# Black plastic part

Parametric reconstruction from four reference photos.

- outer diameter: 8 mm
- circular end recess diameter: 6 mm
- transverse hole diameter: 3.5 mm
- length: 12.5 mm
- axial rectangular through-hole: 5 × 2 mm
- circular end recess depth: 4 mm (estimated from photo)

Generate the printable mesh with:

```bash
uv run generate_model.py
```

The output is `black_plastic_part.stl` in this directory. Print one test piece
before producing multiples; holes in FDM prints often need 0.1–0.3 mm clearance
depending on the printer and filament.

`black_plastic_part_laid_flat.stl` contains the identical mesh rotated 90° for
printing with its long axis parallel to the build plate.

`black_plastic_part_two_orientations.stl` contains two separate shells on one
plate: the original upright orientation and a second copy laid flat.
