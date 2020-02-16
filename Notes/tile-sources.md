
# List
- [trailnotes](https://www.trailnotes.org/FetchMap/TileServeSource.html#default)
- [josm](https://josm.openstreetmap.de/wiki/ImageryCompareIgnores)
- [NYPL Map Warper](http://maps.nypl.org/warper/maps/geosearch?show_warped=1)
- [Historical & contemporary map/images]()   
- [CartoDB](https://github.com/CartoDB/CartoDB-basemaps): offers no-label basemaps
    ![](../images/50229bf3.png)

# Multiple map side-by-side comparison
-   [bbbike](https://mc.bbbike.org/mc/) 
    ![bbbike-map-compare](../images/bbbike-compare.png)
    
# Online gui to get maptile (x,y,z) from (lat, long) interactively
- [geofabrik](https://tools.geofabrik.de/calc/)

# Gui to check which layers are available
- [osmlab](https://osmlab.github.io/editor-layer-index/): it contains almost all 
maptile servers you would ever need, including historical maps
    - try searching "1854" or "NLS" for historical map searches
    - ![](../images/446154ce.png)
    ![](../images/4639a144.png)
    
- [Leaflet Providers Preview](https://tinyurl.com/kvnhknw)
    - This gives quick previews on the map tiles whose urls we can get from the list below $\Downarrow$ 
    - List of map tile server urls provided by Leaflet.js: [link](https://github.com/leaflet-extras/leaflet-providers/blob/master/leaflet-providers.js)
        - Search for, eg. "{z}/{x}/{y}", or "label"
        - URL that offer no-label maptiles
        
- CartoDB: 
```js
            {url: 'https://{s}.basemaps.cartocdn.com/{variant}/{z}/{x}/{y}{r}.png',
			options: {
				attribution: '{attribution.OpenStreetMap} &copy; <a href="https://carto.com/attributions">CARTO</a>',
				subdomains: 'abcd',
				maxZoom: 19,
				variant: 'light_all'
			},
			variants: {
				Positron: 'light_all',
				PositronNoLabels: 'light_nolabels',
				PositronOnlyLabels: 'light_only_labels',
				DarkMatter: 'dark_all',
				DarkMatterNoLabels: 'dark_nolabels',
				DarkMatterOnlyLabels: 'dark_only_labels',
				Voyager: 'rastertiles/voyager',
				VoyagerNoLabels: 'rastertiles/voyager_nolabels',
				VoyagerOnlyLabels: 'rastertiles/voyager_only_labels',
				VoyagerLabelsUnder: 'rastertiles/voyager_labels_under'
			}}
```
 - GeoportailFranceignMaps:
            
```js
            var GeoportailFrance_ignMaps = L.tileLayer('https://wxs.ign.fr/{apikey}/geoportail/wmts?REQUEST=GetTile&SERVICE=WMTS&VERSION=1.0.0&STYLE={style}&TILEMATRIXSET=PM&FORMAT={format}&LAYER=GEOGRAPHICALGRIDSYSTEMS.MAPS&TILEMATRIX={z}&TILEROW={y}&TILECOL={x}', {
	attribution: '<a target="_blank" href="https://www.geoportail.gouv.fr/">Geoportail France</a>',
	bounds: [[-75, -180], [81, 180]],
	minZoom: 2,
	maxZoom: 18,
	apikey: 'choisirgeoportail',
	format: 'image/jpeg',
	style: 'normal'
});
```