# Black plastic part

Parametric reconstruction from four reference photos.

- outer diameter: 8 mm
- axial inner diameter: 6 mm
- transverse hole diameter: 3 mm
- length: 12.5 mm
- internal rectangular relief width: 2 mm

Generate the printable mesh with:

```bash
uv run generate_model.py
```

The output is `black_plastic_part.stl` in this directory. Print one test piece
before producing multiples; holes in FDM prints often need 0.1–0.3 mm clearance
depending on the printer and filament.
