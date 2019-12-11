import os
import json
import urllib.request as ur
from urllib.error import  URLError

from typing import Callable, Iterable, Union
from functools import partial
from pathlib import Path

import time
from decimal import Decimal
import tqdm
from PIL import Image

from tileGeoTransfer import * # getTileFromGeo & getGeoFromTile
from maptile_urls import get_stamen_url
from utils import makedir

def checkBlankImg_ggl(filename):
	'''
	input type: file path
	return type: Boolean
	'''
	im = Image.open(filename) # Can be many different formats.
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


def store_4Geo_Boundary(lnglat_path:str , x, y, z):
	f = open(lnglat_path,"w+")

	# bottom right
	lat, lng = getGeoFromTile(x, y, z)
	f.write("%f %f\n"%(lat, lng))

	# bottom left
	lat, lng = getGeoFromTile(x + 1, y, z)
	f.write("%f %f\n"%(lat, lng))

	# top right
	lat, lng = getGeoFromTile(x, y + 1, z)
	f.write("%f %f\n"%(lat, lng))

	# top left
	lat, lng = getGeoFromTile(x + 1, y + 1, z)
	f.write("%f %f\n"%(lat, lng))

	f.close()


def getImgFromUrl(out_dir: Union[str, Path], url:str, x, y, z):
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
		if checkBlankImg_ggl(out_fn): #or checkBlankImg_ggl(out_fn):
			if out_fn.exists():
				out_fn.unlink()
				print("Deleted: ", x, y, z)
			else:
				print(out_fn, " does not exist. Nothing to do.")
		else:
			lnglat_dir = out_dir/ "lnglat/"
			if not lnglat_dir.exists():
				lnglat_dir.mkdir()

			lnglat_path = lnglat_dir/ f"{x}_{y}_{z}.txt"
			store_4Geo_Boundary(str(lnglat_path), x, y, z)

			print("Success: ", x, y, z, getGeoFromTile(x, y, z))
	else:
		print("Fail: ", x, y, z)



def downlod_tiles_by_xyz(out_dir: Union[str, Path], url_base_fn: Callable,
						 x_start, x_end, y_start, y_end, z):
	out_dir = makedir(out_dir)

	for x in range(x_start, x_end + 1):
		for y in range(y_start, y_end + 1):
			print(x, y)
			url_tile = url_base_fn(x=x, y=y, z=z)
			getImgFromUrl(out_dir, url_tile, x, y, z)
			time.sleep(0.005)


def download_bbox(out_dir: Union[str, Path], url_base_fn: Callable,
				  start_long, end_long, start_lat, end_lat,  zoom):

	x0, y0, z = getTileFromGeo(start_lat, start_long, zoom)
	x1, y1, z = getTileFromGeo(start_lat, end_long, zoom)
	x2, y2, z = getTileFromGeo(end_lat, start_long, zoom)
	x3, y3, z = getTileFromGeo(end_lat, end_long, zoom)

	start_x = min(x0, x1, x2, x3)
	end_x = max(x0, x1, x2, x3)
	start_y = min(y0, y1, y2, y3)
	end_y = max(y0, y1, y2, y3)

	print('Downloading...', start_x, end_x, start_y, end_y)
	downlod_tiles_by_xyz(out_dir, url_base_fn, start_x, end_x, start_y, end_y, z)


def download_stamen(locations_fn:str , styles: Iterable[str], out_dir_root: str):
	"""
	styles = ['toner', 'terrain', 'watercolor']

	:param locations_fn:
	:param styles:
	:param out_dir_root:
	:return:
	"""

	out_dir_root = makedir(out_dir_root)
	with open(locations_fn) as f:
		city_geos = json.load(f)
	print(list(city_geos.keys()))
	for city, geo in tqdm.tqdm(city_geos.items(), desc='city-loop'):
		if city in ['paris', 'khartoum']:
			continue
		xmin, xmax, ymin, ymax = geo['xmin'], geo['xmax'], geo['ymin'], geo['ymax']
		z = geo.get('z', 15)

		print('='*80)
		print('Started ', city)
		for style in tqdm.tqdm(styles, desc=f'style-loop'):
			out_dir = Path(out_dir_root) / city/ style
			out_dir = makedir(out_dir)

			print('Started style: ', city, style)
			url_base_fn = partial(get_stamen_url, style=style)
			download_bbox(out_dir, url_base_fn, xmin, xmax, ymin, ymax, z)
			print(f'Done {style}\n')

		# Google maps

		# NL
		print(f'Done {city}\n\n')



if __name__ == "__main__":
	styles = ['toner','terrain', 'watercolor']
	download_stamen('./locations.json', styles, './temp')







'''
# xmin, xmax, ymin, ymax = 52.0100, 52.0500, -1.0000, -0.9500

F 32697 21647 16
F 32698 21498 16
F 32698 21499 16
success:  32698 21500 16 (52.49615953109709, -0.384521484375)
success:  32698 21501 16 (52.49281508540495, -0.384521484375)
success:  32698 21502 16 (52.48947038534305, -0.384521484375)
F 32698 21503 16
Traceback (most recent call last):
  File "/Users/tresgrand/Documents/Python/retrieveMap/downloader.py", line 146, in <module>
    getBoundary(52.0000, 52.5000, -1.0000, 1.0000, 16)
  File "/Users/tresgrand/Documents/Python/retrieveMap/downloader.py", line 141, in getBoundary
    retrieveMap_byxyz(start_x, end_x, start_y, end_y, z)
  File "/Users/tresgrand/Documents/Python/retrieveMap/downloader.py", line 123, in retrieveMap_byxyz
    getImgFromUrl(url_osm_map, url_nls_map, stored_directory, x, y, z)
  File "/Users/tresgrand/Documents/Python/retrieveMap/downloader.py", line 90, in getImgFromUrl
    if checkBlankImg_nls(name_nls) or checkBlankImg_ggl(name_ggl):
  File "/Users/tresgrand/Documents/Python/retrieveMap/downloader.py", line 17, in checkBlankImg_ggl
    im = Image.open(filename) # Can be many different formats.
  File "/usr/local/lib/python2.7/site-packages/PIL/Image.py", line 2256, in open
    % (filename if filename else fp))
IOError: cannot identify image file 'folder_16/osm_32698_21504_16.jpg'
[Finished in 21593.4s with exit code 1]
[shell_cmd: python -u "/Users/tresgrand/Documents/Python/retrieveMap/downloader.py"]
[dir: /Users/tresgrand/Documents/Python/retrieveMap]
[path: /Library/Frameworks/Python.framework/Versions/3.5/bin:/usr/local/opt/python/libexec/bin:/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin:/opt/X11/bin:/Users/tresgrand/apache-maven-3.5.3/bin]
'''

