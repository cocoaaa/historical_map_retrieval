# Slim version Geoviews tile_sources.py
# Source: https://tinyurl.com/wznug9m
from typing import List
from abc import ABC, abstractmethod
# CartoDB basemaps
# Options: light_all, light_all_lowercase, light_nolabels, light_only_labels, similarly for Dark
CartoDark = 'https://cartodb-basemaps-4.global.ssl.fastly.net/dark_all/{Z}/{X}/{Y}.png'
CartoDarkNoLabels = 'https://cartodb-basemaps-4.global.ssl.fastly.net/dark_nolabels/{Z}/{X}/{Y}.png'

CartoLight = 'https://cartodb-basemaps-4.global.ssl.fastly.net/light_all/{Z}/{X}/{Y}.png'
CartoLightNoLabels = 'https://cartodb-basemaps-4.global.ssl.fastly.net/light_nolabels/{Z}/{X}/{Y}.png'

CartoVoyagerNoLabels = 'https://cartodb-basemaps-4.global.ssl.fastly.net/rastertiles/voyager_nolabels/{Z}/{X}/{Y}.png'

CartoMidnight = 'http://3.api.cartocdn.com/base-midnight/{Z}/{X}/{Y}.png'
CartoEco = 'http://3.api.cartocdn.com/base-eco/{Z}/{X}/{Y}.png'


# Stamen basemaps
StamenTerrain = 'http://tile.stamen.com/terrain/{Z}/{X}/{Y}.png'
StamenTerrainRetina = 'http://tile.stamen.com/terrain/{Z}/{X}/{Y}@2x.png'
StamenTerrainLines = 'http://tile.stamen.com/terrain-lines/{Z}/{X}/{Y}.png'
StamenTerrainBackground = 'http://tile.stamen.com/terrain-background/{Z}/{X}/{Y}.png'

StamenWatercolor = 'http://tile.stamen.com/watercolor/{Z}/{X}/{Y}.jpg'

StamenToner = 'http://tile.stamen.com/toner/{Z}/{X}/{Y}.png'
StamenTonerLines = 'http://tile.stamen.com/toner-lines/{Z}/{X}/{Y}.png'
StamenTonerBackground = 'http://tile.stamen.com/toner-background/{Z}/{X}/{Y}.png'

StamenLabels = 'http://tile.stamen.com/toner-labels/{Z}/{X}/{Y}.png'


# Esri maps (see https://server.arcgisonline.com/arcgis/rest/services for the full list)
EsriImagery = 'https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{Z}/{Y}/{X}.jpg'
EsriNatGeo = 'https://server.arcgisonline.com/ArcGIS/rest/services/NatGeo_World_Map/MapServer/tile/{Z}/{Y}/{X}'
EsriWorldTopo = 'https://server.arcgisonline.com/ArcGIS/rest/services/World_Topo_Map/MapServer/tile/{Z}/{Y}/{X}'
EsriUSATopo = 'https://server.arcgisonline.com/ArcGIS/rest/services/USA_Topo_Maps/MapServer/tile/{Z}/{Y}/{X}'
EsriTerrain = 'https://server.arcgisonline.com/ArcGIS/rest/services/World_Terrain_Base/MapServer/tile/{Z}/{Y}/{X}'
EsriReference = 'https://server.arcgisonline.com/ArcGIS/rest/services/Reference/World_Reference_Overlay/MapServer/tile/{Z}/{Y}/{X}'
EsriOceanBase = 'https://server.arcgisonline.com/ArcGIS/rest/services/Ocean/World_Ocean_Base/MapServer/tile/{Z}/{Y}/{X}'
EsriOceanReference = 'https://server.arcgisonline.com/ArcGIS/rest/services/Ocean/World_Ocean_Reference/MapServer/tile/{Z}/{Y}/{X}'


# Geoportail France
GeoportailParcels = 'https://wxs.ign.fr/choisirgeoportail/geoportail/wmts?REQUEST=GetTile&SERVICE=WMTS&VERSION=1.0.0&STYLE=bdparcellaire&TILEMATRIXSET=PM&FORMAT=image/png&LAYER=CADASTRALPARCELS.PARCELS&TILEMATRIX={Z}&TILEROW={Y}&TILECOL={X}'


# Miscellaneous
OSMDefault = 'https://tiles.wmflabs.org/osm-no-labels/{Z}/{X}/{Y}.png' #'https://c.tile.openstreetmap.org/{Z}/{X}/{Y}.png'
Wikipedia = 'https://maps.wikimedia.org/osm-intl/{Z}/{X}/{Y}@2x.png'
NLSDefault = "https://nls-1.tileserver.com/5eF1a699E49r/{Z}/{X}/{Y}.jpg"
# NLS = "http://nlcas-3.tileserver.com/nls/{Z}/{X}/{Y}.jpg"
MtbmapDefault = 'http://tile.mtbmap.cz/mtbmap_tiles/{Z}/{X}/{Y}.png'

tile_sources = {k: v for k, v in locals().items() if isinstance(v, str) and not k.startswith('__')}

## todo: put them into class
class TileSource(ABC):
    name = None
    styles = None
    @classmethod
    @abstractmethod
    def check_styles(cls, styles: List[str]):
        "Check if all styles in the list `styles` are proper styles for the tile source"
        pass


class Stamen(TileSource):
    name = 'Stamen'
    styles = ['toner', 'toner_background', 'toner_lines',
              'terrain', 'terrain_background', 'terrain_lines',
              'watercolor',
              'labels']

    # todo: urls
    # terrain = 'http://...'


class Esri(TileSource):
    styles = ['imagery', 'nat_geo', 'world_topo', 'usa_topo', 'terrain', 'reference', 'ocean_base', 'ocean_reference' ]
    name = 'Esri'


class Carto(TileSource):
    name = 'Carto'
    styles = ['dark', 'dark_no_labels', 'light', 'light_no_labels', 'voyager_no_labels', 'eco', 'midnight']


class OSM(TileSource):
    name = 'OSM'
    styles = ['default']



class NLS(TileSource):
    name = 'NLS'
    styles = ['default']

class Mtbmap(TileSource):
    name = 'Mtbmap'
    styles = ['default']

