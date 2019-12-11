urlbase_osm = "https://b.tile.openstreetmap.org/%d/%d/%d.png"
urlbase_nls = "https://nls-1.tileserver.com/5eF1a699E49r/%d/%d/%d.jpg"

# http://nls-3.tileserver.com/nls/{z}/{x}/{y}.jpg
def get_stamen_url(style:str , x:int , y:int , z:int ):
    suffix = 'jpg'
    if style == 'toner':
        suffix = 'png'
    return f"http://tile.stamen.com/{style}/{z}/{x}/{y}.{suffix}"
