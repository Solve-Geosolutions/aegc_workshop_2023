![Datarock](assets/datarock_logo_2_rect.jpeg)


# Lithology Analysis Using Computer Vision

This repository holds the code for unsupervised analysis of 14 diamond drill hole completed between 2015-2014 to assess the mineral prospectivity of the GRV. A SwAV SSL model is trained on the images of these drill holes. Output features of the SSL model for each tile are used to analyse their lithology.  This code is implemented using FastAI library.

The designed pipeline includes: 
1. Training a SSL model on cropped tiles from the drill hole images
2. Saving the learned feature embeddings by the trained SSL model for each tile 
3. Applying UMAP on the feature embeddings to reduce their dimensionality to three dimensions 
4. Clustering the UMAP features and showing the clustered tiles 


## Outputs

The output files are as follows: 

1. ```data/processed/all_tiles.csv```: Holds filenames and paths for each coherent tile in the dataset.
2. ```outputs/litho_resnet50_SWAV_256hs_256ps_128bs_0.0001lr_300epochs_123seed_best.pth```: Holds the learned weights for the SwAV model.
3. ```features.pkl```: Contrains the learned feature embedding by the SwAV model for each tile in the dataset.
4. ```features_litho.pkl```: Contrains the learned feature embedding by the SwAV model for each tile in the dataset together with their assigned lithology label.

# How to run

The developed pipeline is composed of seven steps. Each step is implemented in a separate notebook file. The notebook files and their functions are explained below:

1. ```tile_image.ipynb```: This file will crop the image into tiles and saves some statistics about them an excelsheet. 
2. ```select_coherent_tiles.ipynb```: This file will select and save the coherent tiles in a new repository.
3. ```list_images.ipynb```: This file will save name of the coherent tile files in an excelsheet. 
4. ```ssl.ipynb``` This file will apply augmentation on the input tiles and train a SWAV model on the augmented tiles.
5. ```get_embeddings.ipynb```: This file will get embeddings from the trained SwAV model for each tile and saves the embeddings in a pickel file. 
6. ```concat_lithology.ipynb```: This file will find the lithology name for tiles with available lithology label and saves them together with the tile information and SSL features in a pickle file.
7. ```cluster_tiles.ipynb```: This file will reduce the dimension of the SSL features and clusters them. 

## Environments
The following libraries are required:

* fastai = 2.5.4
* self-supervised = 1.0.4
* albumentations = 1.2.1
* rapids = 22.02.00
* opencv = 4.6.0
* matplotlib
* skimage
* sklearn
* rasterio
* numpy
* PIL
* pandas
* tqdm

Multiple conflicts were found between the Rapids, FastAi and Albumentations libraries when we tried to install them in one virtual environment. Therefore, we created **two virtual environments**: one environment holds FastAi, Albumentations libraries and one environment holds the Rapids library. Each notebook will need only one out of the two virtual environments to be able to run. To install Rapids library, follow this [link](https://rapids.ai/start.html#get-rapids). 

## Data

You can download the data using the dvc. First set up the dvc remote to retrieve the data. DVC remote location is stored in settings.yaml file. Use following command to retrieve the data

``` 
dvc remote add -d aegc_workshop_2023 s3://applied-science-dvc/aegc_workshop_2023
```
