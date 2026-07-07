# Arc Solis Armor Full Figurine

Fan-made 3D-printable full-body figurine based on the visual language of
Ultraman Arc Solis Armor / 亚刻奥特曼灼日装甲: red/silver suit, raised fists,
large orange-gold flame armor, sunburst chest plate, oversized shoulder guards,
and segmented forearm wing armor.

## Files

- `generated/arc_solar_armor_full_figurine.stl` - current printable STL, units in millimeters
- `generated/solar_armor_hero_figurine.stl` - older generic solar-armor draft
- `generate_solar_armor_figurine.py` - procedural mesh generator

## Current Model

- Size: about `114 x 78 x 149 mm`
- Triangles: `5892`
- Structure: overlapping closed solids for slicer-friendly printing
- Features: round base, Arc-style helmet crest, eye plates, sunburst chest
  armor, flame-like chest petals, oversized curved shoulder armor, raised
  fists, segmented forearm wing guards, red suit relief stripes

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
