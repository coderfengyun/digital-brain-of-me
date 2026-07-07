# Solar Armor Hero Figurine

Stylized 3D-printable figurine inspired by a silver/red tokusatsu armored hero
with a sun chest crest. This is an original approximation for personal
printing/prototyping, not an exact replica of a licensed character.

## Files

- `generated/solar_armor_hero_figurine.stl` - printable STL, units in millimeters
- `generate_solar_armor_figurine.py` - procedural mesh generator

## Current Model

- Size: about `104 x 78 x 146.5 mm`
- Triangles: `5676`
- Structure: overlapping closed solids for slicer-friendly printing
- Features: round base, silver/red hero silhouette, helmet crest, eye plates,
  chest sun armor, shoulder armor, raised fists, wing-like forearm guards

## Regenerate

```bash
uv run labs/solar-armor-figurine/generate_solar_armor_figurine.py
```

## Print Notes

- Import the STL into Bambu Studio, PrusaSlicer, Cura, or OrcaSlicer.
- Use the slicer's repair/merge function if it reports multiple intersecting
  solids.
- Recommended first test: 0.2 mm layer height, 10-15% infill, tree supports on.
- The model includes a base, so it should stand without adding a raft.
- For resin printing, hollowing and drain holes should be added in the slicer.
