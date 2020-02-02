#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Oct 19 09:57:38 2019

@author: Lukas Graf

@purpose: processes the Sentinel-2 data for the selected study area covering the
	  2017 growing period in order to demonstrate and validate the OBIA4RTM
	  software tool
"""
from OBIA4RTM.processing_api import API
import pandas as pd


# Google Earth Engine will be used for pre-processing the Sentinel-2 imagery
use_gee = True
# create a new API instance to handle the processing
api = API(use_gee)
# set the tablenames accordingly to allow OBIA4RTM to store the results in the
# PostgreSQL/PostGIS backend database
api.set_tablenames()

# setup the parameters controlling the preprocessing:
# this includes the acquisition dates as well as the geometry of the field
# parcels for which the inversion should be conducted and the way the
# atmospherical correction algorithm should be carried out

# the geometry of the bounding box in which the field parcels are located
# in lat/lon coordinates in decimal degrees
geom = [[11.652010083396522,48.24900906966563],
        [11.745054408435749,48.24667656534854],
        [11.748327321488217,48.31192435113173],
        [11.655723673233638,48.314324706548085],
        [11.652010083396522,48.24900906966563]]

# the acquisition dates were previously determined using Google Earth Engine
# searching for available Sentinel-2 scenes in 2017 covering the vegetation
# period which had a cloud coverage less than 20 percent
# the acquisition dates are stored in a ASCII-file and are read from it
filepath = r'../Acqui_Dates/acquisition_dates'
df = pd.read_csv(filepath, sep=":", header=None)
acqui_dates = df[[1]] # extract the acquisition dates

# Shapefile with the field parcel boundaries
shp = r'../Fields/2017_Multiply_Sample_Area.shp'

# Option for cloud masking and shadow detection after atmospherical correction
# -> use method provided by Sam Murphy (Option = 2)
option = 2

# empty dict for storing the retrieved scene ids from the imagery
mapping = dict()

# loop over the acquisition dates to pre-process the images and extract the
# spectra
for ii in range(acqui_dates.shape[0]):
    # get the current acquisition date ('YYYY-MM-DD')
    acqui_date = acqui_dates.iloc[ii].values[0].strip()
    # call gee_preprocessing -> returns scene_id from Sentinel-2 imagery
    scene_id = api.do_gee_preprocessing(geom,
                                        acqui_date,
                                        option,
                                        shp)
    mapping.update({scene_id : acqui_date})

# as a next step, the inversion can be conducted using the derived spectra
# NOTE: this might be also be done in directly in the previous loop instead
# of constructing a new loop ...:

# use the best 10 solutions (mean)
num_best_solutions = 10
# do the inversion for the LUT classes 0 (bare soil) 1 (maize silage) and 2 (winter wheat)
luc_classes = [0, 1, 2]
for ii in range(acqui_dates.shape[0]):
    # get scene id
    scene_id = next(iter( mapping.items() ))[0]
    # get an instance of the inversion interface provided by processing API
    # and run it; return the inverted spectra
    status = api.do_inversion(scene_id, num_best_solutions, luc_classes,
                     return_specs=True)
