from MagCoil import MagCoil
from CurrentFilament import CurrentFilament
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

def grid_gen(geom_type,points_list_path):


#Set total number of coils used

#Read in coil specs 

    if geom_type =="Cylinder": 

       filename = open("grid_vals.csv", 'w')
       # file = csv.DictReader(filename)
       

    elif geom_type =="Torus": 

        dx=0.5
        dy=0.5
        dz=0.5 

        val_file =open("grid_vals.csv", 'w')
        
        print("generating grid file")

        x_max = -100.0 
        y_max = -100.0
        x_min = 100.0 
        y_min = 100.0

        with open(points_list_path) as f:
            cf = csv.reader(f)
            for row in cf:
               # print(row[0],row[1])
                x=float(row[0])
                y=float(row[1])

                if x > x_max: 
                    x_max = x
                    x_min = -x_max
                else: 
                    x_max = x_max 
                    x_min = x_min

                if y > y_max: 
                    y_max = y
                    y_min = -y_max
                else: 
                    y_max = y_max 
                    y_min = y_min
   
        print ( "Final max values: ", x_max, x_min,y_max, y_min)

        x_max_final = int(x_max+1)
        x_min_final = int(( x_min)-1)
        y_max_final = int(y_max +1)
        y_min_final = int(y_min-1)
        z_max_final = x_max_final 
        z_min_final = x_min_final
      
        print ( "Final range: ", x_max_final, x_min_final,y_max_final, y_min_final,z_max_final, z_min_final)  

        print("x_min,x_max,dx,y_min,y_max,dy,z_min,z_max,dz" , file=val_file)
        print (x_min_final,",",x_max_final,",",dx,",",y_min_final,",",y_max_final,",",dy,",",z_min_final,",",z_max_final,",",dz,file=val_file)
    
    #x_min_str,x_max_str,dx_str,y_min_str,y_max_str,dy_str,z_min_str,z_max_str,dz_str = row[:9]



 









