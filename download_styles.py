from downloader import download_selected_styles as dl
import downloader
import argparse
import pdb

if __name__ == "__main__":
    # Argument parser
    parser = argparse.ArgumentParser()
    parser.add_argument("-b","--bboxes", required=True, type=str,
                        help="<Required> Path to a json file with (key:value) as (cityname:bbox) in lat,lng")
    parser.add_argument("-s", "--styles", required=True, type=str,
                        help="<Required> Path to a json file that specified selected map styles (and its tile server name). Uses (key:value) of (tile_server:[list of styles])")
    parser.add_argument("-o", "--out", help="<Optional> Path to the output root folder. Default: ./tmp",
                        type=str, default='./tmp')

    args = parser.parse_args()
    bbox_json = args.bboxes
    styles_json = args.styles
    out_dir_root = args.out

    pdb.set_trace()

    # Download maptiles for the bboxes specified in `bbox_json` file, with the styles specified in `selction_json` file
    # and save images to `{out_dir_root}/{city}/{style}` folders

    dl(bbox_json, styles_json, out_dir_root)
