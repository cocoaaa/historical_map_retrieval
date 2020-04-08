from downloader import download_selected_styles as dl
import downloader
import argparse
import pdb

if __name__ == "__main__":
    """ 
    Example Usage:
    ```bash
    python download_styles.py -b "./locations/paris.json" -s "./selected_styles.json" -o "./temp"
    or, 
    
    On Remote server (eg. arya)
    1. Change to a proper conda env
    conda activate geo_env
    2. Run the download script
    nohup python download_styles.py -b "./locations/vegas.json" -s "./selected_styles.json" -o "/data/hayley/maptiles"
    or, 
    nohup python download_styles.py -b "./locations/locations.json" -s "./styles/osm_styles.json" -o "/data/hayley/maptiles"
    
    To overwrite the zoom level in location.json file, pass the -z argument to CLI:
    nohup python download_styles.py -b "./locations/paris.json" -s "./styles/selected_styles_all.json" -o "/data/hayley/maptiles" -z 12 &

    """
    # Argument parser
    parser = argparse.ArgumentParser()
    parser.add_argument("-b","--bboxes", required=True, type=str,
                        help="<Required> Path to a json file with (key:value) as (cityname:bbox) in lat,lng")
    parser.add_argument("-s", "--styles", required=True, type=str,
                        help="<Required> Path to a json file that specified selected map styles (and its tile server name). Uses (key:value) of (tile_server:[list of styles])")
    parser.add_argument("-z", "--zoom", type=int, default=None,
                        help="<Optional> Zoom level to overwrite the `z` values in *all* location json files.")
    parser.add_argument("-o", "--out", help="<Optional> Path to the output root folder. Default: ./tmp",
                        type=str, default='./tmp')

    args = parser.parse_args()
    bbox_json = args.bboxes
    styles_json = args.styles
    out_dir_root = args.out
    z = args.zoom

    # Download maptiles for the bboxes specified in `bbox_json` file, with the styles specified in `selction_json` file
    # and save images to `{out_dir_root}/{city}/{style}` folders
    overwrites = {"z": z}
    dl(bbox_json, styles_json, out_dir_root, overwrites)
