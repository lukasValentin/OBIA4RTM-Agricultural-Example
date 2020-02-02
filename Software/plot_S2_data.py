#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Oct 20 07:21:46 2019

@author: Lukas Graf

Copyright by Lukas Graf (2019)
"""
import os
from OBIA4RTM.processing_api import API
from OBIA4RTM.configurations.connect_db import connect_db, close_db_connection
from pandas.plotting import register_matplotlib_converters
import matplotlib.pyplot as plt


# set up an API instance and connect to the OBIA4RTM backend database
api = API(use_gee=False)    # in this case it doesn't matter if GEE is used or not

# get the tablenames where the results are stored
api.set_tablenames()
obj_spec_table = api.tablenames[2]  # table with object spectra


# define various types of function to access and visualize data from the database
def plot_single_spectrum(field_id, acqui_date, obj_spec_table):
    """
    function to plot a single spectrum for a specific field on a specific data
    """
    con, cursor = connect_db()  # open database connection
    # determine which sensor was used and get the according bands
    # get the scene id first and use this to query the bands
    query = "SELECT scene_id FROM {0} WHERE "\
            "object_id = {1} AND acquisition_date = '{2}';".format(
                    obj_spec_table,
                    field_id,
                    acqui_date)
    cursor.execute(query)
    scene_id = cursor.fetchone()[0]
    # the sensor is denoted in the first three characters of the scene id
    sensor = scene_id[0:3]
    # now query the band centers (nm) from the metadata table in the public schema
    query = "SELECT central_wvl FROM public.s2_bands WHERE sensor = '{}' "\
            "ORDER BY central_wvl;".format(
                    sensor)
    cursor.execute(query)
    wvl = cursor.fetchall()
    # unpack the returned tuples into a list
    wvl = [x[0] for x in wvl]
    # get the reflectance values in percentage
    query = "SELECT B2, B3, B4, B5, B6, B7, B8A, B11, B12 FROM {0} WHERE "\
            "object_id = {1} AND acquisition_date = '{2}';".format(
                    obj_spec_table,
                    field_id,
                    acqui_date)
    cursor.execute(query)
    spectrum = cursor.fetchall()[0]
    # unpack the returned tuples into a list
    spectrum = [x for x in spectrum]
    # plot the spectrum
    f = plt.figure()
    ax = f.add_subplot(111)
    ax.plot(wvl, spectrum)
    ax.set_title("ID = {0}, '{1}'".format(field_id, acqui_date))
    ax.set_xlabel("Wavelength (nm)")
    ax.set_ylabel("Surface Reflectance (%)")
    plt.show()
    # close the db connection
    close_db_connection(con, cursor)


def plot_ndvi_timeseries(start_date, end_date, object_id, object_table,
                         save_path):
    """
    plot NDVI time series from a specific field provided in the database
    """
    con, cursor = connect_db()  # open database connection
    # gnenerate the sql database query
    sql = "select acquisition_date, (B8A-B4)/(B8A+B4) as NDVI "\
          "from {0} where acquisition_date between '{1}' and '{2}' "\
          "and object_id = {3} order by acquisition_date;".format(
                  object_table,
                  start_date,
                  end_date,
                  object_id)
    cursor.execute(sql)
    res = cursor.fetchall()
    # convert tubles to list
    dates = [x[0] for x in res]     # dates of image acquisition
    ndvi = [x[1] for x in res]      # NDVI values
    f = plt.figure(dpi=200,figsize=(10,10))
    register_matplotlib_converters()
    ax = f.add_subplot(111)
    ax.plot(dates, ndvi)
    ax.set_title("NDVI timeseries of Field with ID: {0}".format(object_id))
    ax.set_xlabel("Date (YYYY-MM-DD)")
    ax.set_ylabel("NDVI (-)")
    plt.xticks(rotation=45)
    ax.set_ylim(0.,1.)
    plt.show()
    save_path = save_path + os.sep + "ndvi_" + str(object_id) + ".png"
    f.savefig(save_path)
    close_db_connection(con, cursor)
#










