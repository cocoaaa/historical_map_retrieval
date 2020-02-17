# Todo
## StamenTiles dataset generation
- [ ] Combine TerrainLines and TerrainBackground by simple overlapping: inputs are a maptile of TerrainLines style and a maptile of TerrainBackground; output is a maptile of overlapped image
- [ ] Download OSM maptiles without labels
    - Note: this may require rendering our own maps from OSM data. Not a priority.
---
# Dataset generating progress
## 2020-02-17 (Mon)
 - EsriWorldTopo server often fails (or does not have a map data) for shanghai. So, skip `EsriWorldTopo` and move onto downloading the rest of maptiles
 - CartoVoyagerNoLabels get stuck for Khartoum.  For now, skip `CartoVoyagerNoLabels` and move onto the rest
 


    
