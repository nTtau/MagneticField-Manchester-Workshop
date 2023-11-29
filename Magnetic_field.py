from MagCoil import MagCoil
from Loop_CoilFields import loop_field
from TF_CoilFields import TF_field
from FieldVis import field_map
from grid_val_gen import grid_gen
import numpy as np
from numpy import linspace
from pylab import *
from mayavi import mlab as MLab
from pylab import *
from CurrentCollection import CurrentCollection
from Meshtricate import Meshtricate
import MultiProcMagCalc
import multiprocessing as mp
import multiprocessing
import logging
import csv

PyFECONS_MAIN = "/home/ssharpe/PyFECONS_REFACTOR/PyFECONS"
points_list_path = PyFECONS_MAIN + "/Geometries/data/geometry_data/toroidal/points_list"
coil_data_path = PyFECONS_MAIN + "/Geometries/pf_coils.csv"
TF_datafile_path = PyFECONS_MAIN + "/data/geometry_data/toroidal/TF_vals.csv"
TF_coords_dir = PyFECONS_MAIN + "/Geometries/data/geometry_data/toroidal"

#Runs full magnetic field code for Toroidal geometry
print("Generating sampling grid") 
#grid_gen("Torus",points_list_path)
print("PF FIELD CALCULATING")
#loop_field("Torus",coil_data_path)
print("TF FIELD CALCULATING") 
#TF_field(12,TF_datafile_path,TF_coords_dir)
print("Total field and mapping") 
field_map("Torus",coil_data_path,TF_coords_dir)
