# Slim version Geoviews tile_sources.py
# Source: https://tinyurl.com/wznug9m

# CartoDB basemaps
CartoDark = 'https://cartodb-basemaps-4.global.ssl.fastly.net/dark_all/{Z}/{X}/{Y}.png'
CartoEco = 'http://3.api.cartocdn.com/base-eco/{Z}/{X}/{Y}.png'
CartoLight = 'https://cartodb-basemaps-4.global.ssl.fastly.net/light_all/{Z}/{X}/{Y}.png'
CartoMidnight = 'http://3.api.cartocdn.com/base-midnight/{Z}/{X}/{Y}.png'

# Stamen basemaps
StamenTerrain = 'http://tile.stamen.com/terrain/{Z}/{X}/{Y}.png'
StamenTerrainRetina = 'http://tile.stamen.com/terrain/{Z}/{X}/{Y}@2x.png'
StamenWatercolor = 'http://tile.stamen.com/watercolor/{Z}/{X}/{Y}.jpg'
StamenToner = 'http://tile.stamen.com/toner/{Z}/{X}/{Y}.png'
StamenTonerBackground = 'http://tile.stamen.com/toner-background/{Z}/{X}/{Y}.png'
StamenLabels = 'http://tile.stamen.com/toner-labels/{Z}/{X}/{Y}.png'

# Esri maps (see https://server.arcgisonline.com/arcgis/rest/services for the full list)
EsriImagery = 'https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{Z}/{Y}/{X}.jpg'
EsriNatGeo = 'https://server.arcgisonline.com/ArcGIS/rest/services/NatGeo_World_Map/MapServer/tile/{Z}/{Y}/{X}'
EsriUSATopo = 'https://server.arcgisonline.com/ArcGIS/rest/services/USA_Topo_Maps/MapServer/tile/{Z}/{Y}/{X}'
EsriTerrain = 'https://server.arcgisonline.com/ArcGIS/rest/services/World_Terrain_Base/MapServer/tile/{Z}/{Y}/{X}'
EsriReference = 'https://server.arcgisonline.com/ArcGIS/rest/services/Reference/World_Reference_Overlay/MapServer/tile/{Z}/{Y}/{X}'
EsriOceanBase = 'https://server.arcgisonline.com/ArcGIS/rest/services/Ocean/World_Ocean_Base/MapServer/tile/{Z}/{Y}/{X}'
EsriOceanReference = 'https://server.arcgisonline.com/ArcGIS/rest/services/Ocean/World_Ocean_Reference/MapServer/tile/{Z}/{Y}/{X}'

# Miscellaneous
OSM = 'https://c.tile.openstreetmap.org/{Z}/{X}/{Y}.png'
Wikipedia = 'https://maps.wikimedia.org/osm-intl/{Z}/{X}/{Y}@2x.png'
NLS = "https://nls-1.tileserver.com/5eF1a699E49r/{Z}/{X}/{Y}.jpg"
# NLS = "http://nls-3.tileserver.com/nls/{Z}/{X}/{Y}.jpg"


tile_sources = {k: v for k, v in locals().items() if isinstance(v, str) and not k.startswith('__')}

