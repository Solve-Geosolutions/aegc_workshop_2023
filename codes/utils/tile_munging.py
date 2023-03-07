import pandas as pd
pd.options.mode.chained_assignment = None  # default='warn'

def pixel_counts(row_px: int, tile_px: int, tile_meta: pd.DataFrame, no_tiles: int)-> pd.DataFrame:
    """get pixel lengths along core and add cols to tile_meta

    Args:
        row_px (int): image pixel count for row
        tile_px (int): image pixel count for square tile
        df (pd.DataFrame): tile metadata df
        no_tiles (int): number of tiles generated per row

    Returns:
        pd.DataFrame: tile_meta with pixel_from and pixel_to lengths and row pixel proportions
    """
    row_px_x = row_px
    tile_px_x = tile_px
    row_px_prop = tile_px_x / row_px_x # get proportion of pixels along row for each tile

    # append pixel counts to tile data
    tile_meta['pixel_from'] = [i*row_px_prop for i in range(no_tiles)]
    tile_meta['pixel_to'] = [(i+1)*row_px_prop for i in range(no_tiles)]

    for category in ["empty_tray", "coherent_rock", "incoherent_rock", "core_block", "undetected_region"]:
        tile_meta[category] = 0
    
    return tile_meta, row_px_prop


def add_tile_proportions(tile_meta: pd.DataFrame, row_meta: pd.DataFrame, row_px_prop: float)-> pd.DataFrame:
    """Iterate through tiles and calc proportion of classes in each

    Args:
        tile_meta (pd.DataFrame): cut tile metadata df
        row_meta (pd.DataFrame): row metadata df from platform
        row_px_prop (float): proportion of each tile to the whole row

    Returns:
        pd.DataFrame: tile metadata df with proportion cols filled
    """
    # loop through tiles
    for i, tile in tile_meta.iterrows():
        row_tofrom = row_meta[(row_meta.pixel_to>=tile.pixel_from) & (row_meta.pixel_from<tile.pixel_to)] # find all row data within the tile's coverage
        row_tofrom['pixel_width'] = 0 # set up a width column for calculating proportions
        # check if there is only one category within the tile
        if len(row_tofrom) == 1:
            category = row_tofrom.classification.values[0]
            tile_meta[category].iloc[i] = 1
        else:
            for j, category in row_tofrom.reset_index().iterrows():
                # cut first from value to tile from
                if row_tofrom['pixel_from'].iloc[j] < tile.pixel_from:
                    row_tofrom['pixel_from'].iloc[j] = tile.pixel_from
                # cut last to value to tile to
                if row_tofrom['pixel_to'].iloc[j] > tile.pixel_to:
                    row_tofrom['pixel_to'].iloc[j] = tile.pixel_to
            # calculate the width of each category within the tile
            row_tofrom['pixel_width'] = row_tofrom['pixel_to'] - row_tofrom['pixel_from']
            # sum the widths from each category and divide by tile size
            prop_empty = row_tofrom[row_tofrom.classification == 'empty_tray'].pixel_width.sum()/row_px_prop
            prop_coherent = row_tofrom[row_tofrom.classification == 'coherent_rock'].pixel_width.sum()/row_px_prop
            prop_incoherent = row_tofrom[row_tofrom.classification == 'incoherent_rock'].pixel_width.sum()/row_px_prop
            prop_block = row_tofrom[row_tofrom.classification == 'core_block'].pixel_width.sum()/row_px_prop
            prop_undetected = row_tofrom[row_tofrom.classification == 'undetected_region'].pixel_width.sum()/row_px_prop
            # assign to tile dataframe
            tile_meta['empty_tray'].iloc[i] = prop_empty
            tile_meta['coherent_rock'].iloc[i] = prop_coherent
            tile_meta['incoherent_rock'].iloc[i] = prop_incoherent
            tile_meta['core_block'].iloc[i] = prop_block
            tile_meta['undetected_region'].iloc[i] = prop_undetected
     
    return tile_meta

