# CREDITS.md — SpectreBand / GhostNet

## Open Source Libraries

### trimesh
- URL: https://github.com/mikedh/trimesh
- License: MIT
- Usage: Mesh primitives, scene composition, GLTF export
- Version: 5.0.0

### plotly
- URL: https://github.com/plotly/plotly.py
- License: MIT
- Usage: Interactive HTML 3D visualization
- Version: 6.3.0

### matplotlib
- URL: https://github.com/matplotlib/matplotlib
- License: PSF-based
- Usage: Static 3D renders, Poly3DCollection
- Version: 3.10.0

### numpy
- URL: https://github.com/numpy/numpy
- License: BSD-3-Clause
- Usage: Array operations, vertex transformations
- Version: 2.2.0

## Code Patterns Borrowed

- trimesh Scene Graph composition and nodes_geometry iteration
- matplotlib Poly3DCollection vertex transformation pipeline
- plotly Mesh3d i/j/k face indexing

## Field Data

- Blitz Paintball Dacono: 5340 Summit Blvd, Dacono, CO 80514
- Satellite imagery: Google Earth (fair use survey)
- Measurements: Google Earth measurement tools

## License

Original code: MIT. Borrowed code retains original licenses (MIT/BSD-3-Clause).

### Top-Down Tactical Map Rendering
- Pattern: Military tactical map symbology (MIL-STD-2525)
- Pattern: Game minimap rendering (Counter-Strike radar style)
- Implementation: matplotlib patches, FancyBboxPatch, RegularPolygon
