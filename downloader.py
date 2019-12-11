import os
import argparse
import json
import urllib.request as ur
from urllib.error import URLError

from typing import Callable, Iterable, Union
from functools import partial
from pathlib import Path

import time
from decimal import Decimal
import tqdm
from PIL import Image

from tileGeoTransfer import *  # getTileFromGeo & getGeoFromTile
import tile_sources as ts
from utils import makedir, snake2camel


def checkBlankImg_ggl(filename):
    '''
	input type: file path
	return type: Boolean
	'''
    im = Image.open(filename)  # Can be many different formats.
    pix = im.load()

    # print(im.size
    pixel_values = list(im.getdata())

    # RGB channel
    if min(pixel_values) == max(pixel_values):
        return True

    return False


def checkBlankImg_nls(filename):
    '''
	input type: file path
	return type: Boolean
	'''
    im = Image.open(filename)
    pix = im.load()

    # print(im.size
    pixel_values = list(im.getdata())
    zipped = zip(pixel_values)

    # RGB channel
    if min(zipped[0][0]) == max(zipped[0][0]) \
            and min(zipped[1][0]) == max(zipped[1][0]) \
            and min(zipped[2][0]) == max(zipped[2][0]):
        return True

    return False


def store_4Geo_Boundary(lnglat_path: str, x, y, z):
    f = open(lnglat_path, "w+")

    # bottom right
    lat, lng = getGeoFromTile(x, y, z)
    f.write("%f %f\n" % (lat, lng))

    # bottom left
    lat, lng = getGeoFromTile(x + 1, y, z)
    f.write("%f %f\n" % (lat, lng))

    # top right
    lat, lng = getGeoFromTile(x, y + 1, z)
    f.write("%f %f\n" % (lat, lng))

    # top left
    lat, lng = getGeoFromTile(x + 1, y + 1, z)
    f.write("%f %f\n" % (lat, lng))

    f.close()


def getImgFromUrl(out_dir: Union[str, Path], url: str, x, y, z):
    checkBlankImg_fn = checkBlankImg_nls if 'nls' in url else checkBlankImg_ggl
    req = ur.Request(url)
    try:
        urlobj = ur.urlopen(req)
    except URLError as e:
        if hasattr(e, 'reason'):
            print('We failed to reach a server.')
            print('Reason: ', e.reason)
        elif hasattr(e, 'code'):
            print('The server couldn\'t fulfill the request.')
            print('Error code: ', e.code)
        print("F", x, y, z)
        return

    out_dir = makedir(out_dir)
    if urlobj.getcode() == 200:
        out_fn = out_dir / f"{x}_{y}_{z}.png"

        try:
            ur.urlretrieve(url, str(out_fn))
        except URLError as e:
            if hasattr(e, 'reason'):
                print('We failed to reach a server.')
                print('Reason: ', e.reason)
            elif hasattr(e, 'code'):
                print('The server couldn\'t fulfill the request.')
                print('Error code: ', e.code)
            print("F", x, y, z)
            return

        # Check if the image is blank, i.e: sea, plain grass
        if checkBlankImg_fn(out_fn):  # or checkBlankImg_ggl(out_fn):
            if out_fn.exists():
                out_fn.unlink()
                print("Deleted: ", x, y, z)
            else:
                print(out_fn, " does not exist. Nothing to do.")
        else:
            lnglat_dir = out_dir / "lnglat/"
            if not lnglat_dir.exists():
                lnglat_dir.mkdir()

            lnglat_path = lnglat_dir / f"{x}_{y}_{z}.txt"
            store_4Geo_Boundary(str(lnglat_path), x, y, z)

            print("Success: ", x, y, z, getGeoFromTile(x, y, z))
    else:
        print("Fail: ", x, y, z)


def downlod_tiles_by_xyz(out_dir: Union[str, Path], url_base: str,
                         x_start, x_end, y_start, y_end, z):
    out_dir = makedir(out_dir)

    for x in range(x_start, x_end + 1):
        for y in range(y_start, y_end + 1):
            print(x, y)
            url_tile = url_base.format(X=x, Y=y, Z=z)
            getImgFromUrl(out_dir, url_tile, x, y, z)
            time.sleep(0.005)

def download_tiles_by_lnglat(out_dir: Union[str, Path], url_base: str,
                             start_long, end_long, start_lat, end_lat, zoom):
    x0, y0, z = getTileFromGeo(start_lat, start_long, zoom)
    x1, y1, z = getTileFromGeo(start_lat, end_long, zoom)
    x2, y2, z = getTileFromGeo(end_lat, start_long, zoom)
    x3, y3, z = getTileFromGeo(end_lat, end_long, zoom)

    start_x = min(x0, x1, x2, x3)
    end_x = max(x0, x1, x2, x3)
    start_y = min(y0, y1, y2, y3)
    end_y = max(y0, y1, y2, y3)

    print('Downloading...', start_x, end_x, start_y, end_y)
    downlod_tiles_by_xyz(out_dir, url_base, start_x, end_x, start_y, end_y, z)

def download_tiles_from_cities(locations_fn: str, tile_source_name:str, styles: Iterable[str], out_dir_root: Union[str,Path]):
    out_dir_root = makedir(out_dir_root)

    with open(locations_fn) as f:
        city_geos = json.load(f)
    print(list(city_geos.keys()))

    for city, geo in tqdm.tqdm(city_geos.items(), desc='city-loop'):
        # if city in ['paris', 'khartoum']:
        #     continue
        xmin, xmax, ymin, ymax = geo['xmin'], geo['xmax'], geo['ymin'], geo['ymax']
        z = geo.get('z', 15)

        print('=' * 80)
        print('Started ', city)
        for style in tqdm.tqdm(styles, desc=f'style-loop'):


            print('Started style: ', city, style)
            ts_name = f'{tile_source_name}{snake2camel(style)}'
            url_base = ts.tile_sources[ts_name]
            print(f'style: {ts_name}, \nurl_base: {url_base}')

            out_dir = Path(out_dir_root) / city / ts_name
            out_dir = makedir(out_dir)
            download_tiles_by_lnglat(out_dir, url_base, xmin, xmax, ymin, ymax, z)
            print(f'Done {style}\n')
        print(f'Done {city}\n\n')


def download_stamen_styles(locations_fn: str, styles: Iterable[str], out_dir_root: Union[str,Path]):
    """
	styles = ['toner', 'toner_background', 'terrain', 'watercolor']

	:param locations_fn: path to the json file with city_name:bbox_dictionary
	:param styles:
	:param out_dir_root:
	:return:
	"""
    for style in styles:
        assert style.lower() in ['toner', 'toner_background', 'terrain', 'watercolor'], f'{style} is not a valid style name'
    tile_source_name = 'Stamen'
    download_tiles_from_cities(locations_fn, tile_source_name, styles, out_dir_root)


def download_esri_styles(locations_fn: str, styles: Iterable[str], out_dir_root: Union[str,Path]):
    for style in styles:
        assert style.lower() in ['imagery', 'nat_geo', 'terrain', 'reference', 'ocean_base', 'ocean_reference' ], f'{style} is not a valid style name'
    tile_source_name = 'Esri'
    download_tiles_from_cities(locations_fn, tile_source_name, styles, out_dir_root)

def download_carto_styles(locations_fn: str, styles: Iterable[str], out_dir_root: Union[str,Path]):
    for style in styles:
        assert style.lower() in ['dark', 'light', 'eco', 'midnight'], f'{style} is not a valid style name'
    tile_source_name = 'Carto'
    download_tiles_from_cities(locations_fn, tile_source_name, styles, out_dir_root)

def download_osm(locations_fn: str, out_dir_root: str):
    out_dir_root = makedir(out_dir_root)

    with open(locations_fn) as f:
        city_geos = json.load(f)
    print(list(city_geos.keys()))

    for city, geo in tqdm.tqdm(city_geos.items(), desc='city-loop'):
        if city in ['paris', 'khartoum']:
            continue
        xmin, xmax, ymin, ymax = geo['xmin'], geo['xmax'], geo['ymin'], geo['ymax']
        z = geo.get('z', 15)

        print('=' * 80)
        print('Started ', city)
        out_dir = Path(out_dir_root) / city
        out_dir = makedir(out_dir)

        url_base = ts.tile_sources['OSM']
        download_tiles_by_lnglat(out_dir, url_base, xmin, xmax, ymin, ymax, z)
        print(f'Done {city}\n\n')

def download_nls(locations_fn: str, out_dir_root: str, z=16):
    out_dir_root = makedir(out_dir_root)

    with open(locations_fn) as f:
        city_geos = json.load(f)
    print(list(city_geos.keys()))

    for city, geo in tqdm.tqdm(city_geos.items(), desc='city-loop'):
        xmin, xmax, ymin, ymax = geo['xmin'], geo['xmax'], geo['ymin'], geo['ymax']
        z = geo.get('z', z)

        print('=' * 80)
        print('Started ', city)
        out_dir = Path(out_dir_root) / city
        out_dir = makedir(out_dir)

        url_base = ts.tile_sources['NLS']
        download_tiles_by_lnglat(out_dir, url_base, xmin, xmax, ymin, ymax, z)
        print(f'Done {city}\n\n')


if __name__ == "__main__":
    # Argument parser
    parser = argparse.ArgumentParser()
    parser.add_argument("bbox_json", type=str,
                        help="Path to a json file with cityname:bbox in lat,lng")
    parser.add_argument("-ts", "--tile-server", required=True, type=str,
                        help="name of the tile server. Options: stamen, esri, carto, osm, nls")
    parser.add_argument("-o", "--out", help="Path to the output root folder. Default: ./tmp",
                        type=str, default='./tmp')

    args = parser.parse_args()
    bbox_json = args.bbox_json
    tile_server = args.tile_server
    out_dir = args.out

    # Handle downloading from the specified tile server
    if tile_server == 'stamen':
        styles = ['toner_background', 'terrain', 'watercolor']
        download_stamen_styles(bbox_json, styles, out_dir)

    elif tile_server == 'esri':
        styles = ['imagery']#, 'nat_geo', 'terrain']
        download_esri_styles(bbox_json, styles, out_dir)

    elif tile_server == 'carto':
        styles = ['light']#['dark', 'light']
        download_carto_styles(bbox_json, styles, out_dir)

    elif tile_server == 'osm':
        download_osm(bbox_json, out_dir)

    elif tile_server == 'nls':
        download_nls(bbox_json, out_dir)




# xmin, xmax, ymin, ymax = 52.0100, 52.0500, -1.0000, -0.9500
