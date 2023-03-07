import numpy as np
import pandas as pd
from PIL import Image
from pathlib import Path
import uuid
from utils.tile_munging import pixel_counts, add_tile_proportions


def cut_row_to_squares(image_file:str|Path, # numpy array of image
                       path_out:str|Path="", # output location
                       hole_id:str="", # hole_id
                       box_id:int=None, # box id
                       row_id:int=None, # row id
                       depth_from:float=None, # depth from of row
                       depth_to:float=None, # depth to of row
                       cutoff_top:float=0.15, # percentage cut off from top
                       cutoff_bottom:float=0.15, # percentage cut off from bottom
                       overlap:float=0.0, # percentage overlap
                      use_middle_depth:bool=False): # use middle depth between 2 consecutive squares
    
    "Cut row into squares with overlap and cut off top/bottom option"
    # cut off top, bottom
    image_file = Path(image_file)
    np_img = np.array(Image.open(str(image_file)))
    np_img = np_img[int(cutoff_top*np_img.shape[0]):int((1-cutoff_bottom)*np_img.shape[0]),]
    # get pixel_length of the img
    pixel_length = np_img.shape[0]
    # get pixel pixel_length of depth
    length = (np_img.shape[0]/np_img.shape[1])*(depth_to-depth_from)
    pixel_start = 0
    square_start = depth_from
    path_out = Path(path_out)
    # track square number in row
    i = 0
    # initiate dataframe
    new_df = pd.DataFrame()
    while True:
        if (pixel_start+pixel_length) >= np_img.shape[1]:
            break
        # save image 
        save_file = path_out/f"{image_file.stem}_{i}{image_file.suffix}"
        im = Image.fromarray(np_img[:,pixel_start:pixel_start+pixel_length,:])
        im.save(save_file, quality=95)
        square_from = round(square_start,6)
        if use_middle_depth:
            square_to = round((square_start+length*(1-overlap/2)),6)
        else:
            square_to = round(square_start+length,6)
        if i == 0:
            new_df = pd.concat([new_df,pd.DataFrame(data={
                "hole_id":[hole_id],
                "tile_filename":[save_file.name],
                "square_uuid": [uuid.uuid4()],
                "square_from":[square_from],
                "square_to":[square_to],
                "row_from": [depth_from],
                "row_to": [depth_to]
            })],ignore_index=True)
            pixel_start += int(pixel_length*(1-overlap))
            if use_middle_depth:
                square_start = square_start+length*(1-overlap/2.)
            else:
                square_start = square_start+length*(1-overlap)
            i += 1
        else:
            new_df = pd.concat([new_df,pd.DataFrame(data={
                "hole_id":[hole_id],
                "tile_filename":[save_file.name],
                "square_uuid": [uuid.uuid4()],
                "square_from":[square_from],
                "square_to":[square_to],
                "row_from": [depth_from],
                "row_to": [depth_to]
            })],ignore_index=True)
            pixel_start += int(pixel_length*(1-overlap))
            square_start = square_start+length*(1-overlap)
            i += 1

    # return row and tile x pixel length, no tiles and depth of cut squares
    return np_img.shape[0], np_img.shape[1], new_df, i


def run_tile_process(hole_path: str, processed_path: str, row_meta_file: str)-> None:
    """run hole tile cutter and tile classification munging and return depth dataframe

    Args:
        hole_path (str): _description_
        processed_path (str): _description_
        row_meta (str): _description_
    """
    # load row classification csv
    print(row_meta_file)
    #row_meta = pd.read_csv(row_meta_file)
    
    # create list of row uuid's to select from
    '''row_uuid = row_meta.row_uuid.unique()
   
    # initialize depth dataframe
    df_depth = pd.DataFrame()
    hole_id = hole_path.name
    fnames = sorted(get_image_files(hole_path))
    for x, fn in enumerate(fnames):
        # create folder if not exists
        if not (processed_path/hole_id).exists():
            (processed_path/hole_id).mkdir(parents=True)
        # where to save squares
        target_file = processed_path/hole_id
        # extract depth_from depth_to from filename
        d_str = fn.stem.split("-")[-5]
        try:
            depth_to = float(d_str.split("_")[-1])
            depth_from = float(d_str.split("_")[-2])
        except:
            try:
                depth_to = float(d_str.split("_")[-2])
                depth_from = float(d_str.split("_")[-3])
            except:
                depth_to = float(d_str.split("_")[3])
                depth_from = float(d_str.split("_")[2])

        box_id = fn.stem.split("-")[-3]
        row_id = fn.stem.split("-")[-1]

        
        # swap if depth_from > depth_to
        if depth_from > depth_to:
            d_tempt = depth_to
            depth_to = depth_from
            depth_from = d_tempt
            
        tile_x, row_x, df_, no_tiles = cut_row_to_squares(image_file=fn, path_out=target_file, hole_id=hole_id,box_id=box_id, row_id=row_id, depth_from=depth_from, depth_to=depth_to)
        
        #row_meta_row = row_meta[row_meta.row_uuid == row_uuid[x]]
        # run functions to calculate class proportions in tiles
        df_, row_px_prop = pixel_counts(row_x, tile_x, df_, no_tiles)
        #df_ = add_tile_proportions(df_, row_meta_row, row_px_prop)
        #df_['row_uuid'] = row_uuid[x]
        # concat depth extracted from each squares
        df_depth = pd.concat([df_depth, df_],ignore_index=True)

    # save depth dataframe of hole hole_id 
    df_depth.to_csv(processed_path/f"tile_meta_{hole_id}.csv",index=False)

    #return  tile_x, row_x, no_tiles'''


def get_image_files(hole_path):
    """parse a folder and return all jpg images"""
    # create an empty list to store the files with .jpg extension
    jpg_files = []

    # loop through all the files in the folder
    for file in hole_path.iterdir():
        # check if the file has a .jpg extension
        if file.suffix == ".jpg":
            # add the file to the list
            jpg_files.append(file)

    # return the list of .jpg files
    return jpg_files


