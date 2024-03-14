#!/usr/bin/env python
import os
import re
import requests
from numpy import ndarray
from pathlib import Path
from rasterio.transform import from_bounds, AffineTransformer
from shapely.geometry import MultiPolygon
from src.lib.util.image import ImageUtil
from src.lib.util.mask import MaskUtil
from src.lib.util.shape import ShapeUtil
from src.lib.util.shapefile import EsriShapefileUtil


def clear_terminal():
    os.system('cls' if os.name == 'nt' else 'clear')


# Add static credentials here to bypass the login prompt
tc_username: str = ''
tc_password: str = ''

export_path: Path = Path('./export')

login_url: str = 'https://www.towercoverage.com/En-US/Home/Login'
multimaps_url: str = 'https://www.towercoverage.com/En-US/Home/MultiCoverageList'

token_regex: re.Pattern = re.compile(
    r'\s*<input name="__RequestVerificationToken" type="hidden" value="([0-9a-zA-Z_\-]+)" />\s*')

mm_link_regex: re.Pattern = re.compile(
    r'\s*<a href="/En-US/Dashboard/MultiCoverageViewOnly/([0-9]+)">([0-9a-zA-Z_\-\s]+)</a>\s*')

overlay_url_regex: re.Pattern = re.compile(
    r'(https://account\.towercoverage\.com/[0-9a-z]+/multicovs/[0-9a-z]+/[0-9_]+\.png)')

bounding_box_regex: re.Pattern = re.compile(
    r'\s*var imageBounds = new google\.maps\.LatLngBounds\(new google\.maps\.LatLng\( '
    + r'(-?[0-9]{1,3}\.[0-9]+),(-?[0-9]{1,3}\.[0-9]+)\), new google\.maps\.LatLng\( '
    + r'(-?[0-9]{1,3}\.[0-9]+),(-?[0-9]{1,3}\.[0-9]+)\)\);\s*')

headers: dict = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  + 'Chrome/121.0.0.0 Safari/537.36',
}

cookies: dict = {
    '.ASPXAUTH': '',
    '__RequestVerificationToken': '',
}

clear_terminal()

if tc_username is None or not str(tc_username).strip():
    tc_username = input('Please enter your Tower Coverage username: ')

if tc_password is None or not str(tc_password).strip():
    tc_password = input('Please enter your Tower Coverage password: ')

clear_terminal()

login_req = requests.get(login_url)

token_match = token_regex.search(login_req.text)

if token_match is None:
    print('Failed to find the login form verification token!')
    exit(1)

cookies['__RequestVerificationToken'] = token_match.group(1)

login_data: dict = {
    '__RequestVerificationToken': cookies['__RequestVerificationToken'],
    'Username': tc_username,
    'Password': tc_password,
    'RememberMe': 'false',
}

login_req = requests.post(login_url, headers=headers, cookies=dict(login_req.cookies), data=login_data,
                          allow_redirects=False)

cookies['.ASPXAUTH'] = login_req.cookies['.ASPXAUTH']

mm_content: str = requests.get(multimaps_url, cookies=cookies).text

mm_links = mm_link_regex.findall(mm_content, re.MULTILINE)

clear_terminal()

print('\nWhich multi-map would you like to export?\n')

index: int = 1
for multimap in mm_links:
    print(f'  {index}. {multimap[1]}\n')
    index += 1

mm_index: int = int(input('Please enter the number of the multi-map you would like to export: ')) - 1

if mm_index < 0 or mm_index >= len(mm_links):
    print('Invalid multi-map number!')
    exit(1)

mm_id: int = int(mm_links[mm_index][0])
mm_name: str = str(mm_links[mm_index][1]).strip()
mm_file: str = mm_name.replace(' ', '_')
raster_path: Path = export_path / f'raster-{mm_id}-{mm_file}.png'
shp_path: Path = export_path / f'{mm_file}-{mm_id}.shp'

# Create the export path if it doesn't already exist
if not export_path.exists():
    export_path.mkdir()

clear_terminal()

print(f'Exporting multi-map: {mm_name} ({mm_id})\n')

mm_url: str = f'https://www.towercoverage.com/En-Us/Dashboard/MultiCoverageViewOnly/{mm_id}'

page_content: str = requests.get(mm_url, cookies=cookies).text

overlay_match = overlay_url_regex.search(page_content, re.MULTILINE)
bounding_box_match = bounding_box_regex.search(page_content, re.MULTILINE)

if not overlay_match:
    print('Failed to find the overlay image URL!')
    exit(1)

if not bounding_box_match:
    print('Failed to find the bounding box information!')
    exit(1)

overlay_url: str = overlay_match.group(1)

print(f'Downloading overlay image: {overlay_url}\n')

image_req = requests.get(overlay_url, headers=headers, cookies=cookies)

if image_req.status_code != 200:
    print(f'Failed to download the overlay image: {overlay_url}')
    exit(1)

# Save the overlay image to a temporary file
with open(raster_path, 'wb') as raster_file:
    raster_file.write(image_req.content)

bound_south: float = float(bounding_box_match.group(1))
bound_west: float = float(bounding_box_match.group(2))
bound_north: float = float(bounding_box_match.group(3))
bound_east: float = float(bounding_box_match.group(4))

print('Loading overlay image meta...\n')

# Get source image meta
png_meta: tuple = ImageUtil.get_meta(str(raster_path))

# Setup CRS transformation
png_transformer: AffineTransformer = from_bounds(bound_west, bound_south, bound_east, bound_north, png_meta[0],
                                                 png_meta[1])

print('Creating binary mask from overlay image...\n')

# Create binary mask from source image's alpha channel
mask: ndarray = MaskUtil.create_mask_from_image_alpha(str(raster_path))

print('Creating polygon data from binary mask...\n')

# Create a set of polygons representing the shape of each isolated blob of alpha data from the mask
polygon: MultiPolygon = ShapeUtil.create_multipolygon_from_mask(mask, png_transformer)

print('Saving ESRI Shapefile...\n')

# Save the polygon data to an ESRI Shapefile
saved: bool = EsriShapefileUtil.create_from_multipolygon(str(shp_path), polygon)

archive_path: Path = shp_path.with_suffix('.zip')

if saved:
    print(f'ESRI Shapefile created successfully: {archive_path}\n')
else:
    print(f'ESRI Shapefile failed to save: {archive_path}\n')
