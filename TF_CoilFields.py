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

def TF_field(coil_num,TF_datafile_path,TF_coords_dir): 
    
#Read in grid values
    grid_file = open('grid_vals.csv','r')  
    file2 = csv.DictReader(grid_file)

    for row in csv.reader(grid_file):
        x_min_str,x_max_str,dx_str,y_min_str,y_max_str,dy_str,z_min_str,z_max_str,dz_str = row[:9]


    dx=float(dx_str)
    dy=float(dy_str)
    dz=float(dz_str)

    x_min = float(x_min_str) 
    x_max = float(x_max_str)
    y_min = float(y_min_str)
    y_max = float(y_max_str)
    z_min = float(z_min_str)
    z_max = float(z_max_str)

    x_points=1+((x_max-x_min)/dx)
    y_points=1+((y_max-y_min)/dy)
    z_points=1+((z_max-z_min)/dz)

    coords_total = int((x_points)*(y_points)*(z_points))
    print('coords_total =',coords_total)

    print(x_min,x_max,dx,y_min,y_max,dy,z_min,z_max,dz)

 
# creating empty lists to write to later
    Coil_num_str = []
    N_str = []
    I_str= []

    coil_counter =0

    
    TF_val_file = open(TF_datafile_path,'r')  
    file3 = csv.DictReader(TF_val_file)

    for col in file3:

        #count number of coils
        coil_counter=coil_counter+1

        #Read in values
        Coil_num_str.append(col['coil_num'])
        N_str.append(col['N'])
        I_str.append(col['I (A)'])

    #Create correct size arrays to store info about each coil
    N = np.zeros(coil_num)
    I= np.zeros(coil_num)

# convert to correct type (integer/float)
    count=0

    total_field=np.zeros((coords_total,6))

    while count<= coil_num-1:
   
        N[count]=int(N_str[count]) 
        I[count]=float(I_str[count])
       # print(Coil_num_str[count],N[count],I[count])

        count=count+1

    print ("All coils identified")

#set coil loops

    coil_count=1

    while coil_count <= coil_num:

        count=0

        #print(coil_count,count)

        file3_name=TF_coords_dir + "/TF_" + str(coil_count) + ".csv"
        #print(file3_name)

        TF_coords= open(file3_name, "r")
        file3 = csv.DictReader(TF_coords)

        TF_x_str = []
        TF_y_str = []
        TF_z_str = []
        #print("length : ",len(TF_x_str),len(TF_y_str),len(TF_z_str))

        tot_point=0 

        for col in file3:

                #Read in values
            TF_x_str.append(col['x'])
            TF_y_str.append(col['y'])
            TF_z_str.append(col['z'])
            tot_point=tot_point+1
            
        coords = np.zeros((tot_point,3))
        #print("total points= : ", tot_point)

        while count <= tot_point-1: 
      
           # print("count= ",count)
            coords[count,0]=float(TF_x_str[count])
            coords[count,1]=float(TF_y_str[count])
            coords[count,2]=float(TF_z_str[count])
            
            count=count+1
       
        #print(coords)

        #Calculate field from this loop
     

        #print(N[coil_count-1]*I[coil_count-1])
        c1=CurrentFilament(coords,N[coil_count-1]*I[coil_count-1])
        
        
        l=c1.length()

        #print("Coil, ", coil_count, "length = ",l)
        #print(coil_count)

        centre=np.zeros((1,3))
        point_coords=np.zeros((1,3))
 
        x_current=x_min 
        y_current=y_min
        z_current=z_min

        point_num=0

        field_array=np.zeros((coords_total,6))
 
        while x_current <= x_max:

                y_current = y_min

                while y_current <= y_max:

                        z_current = z_min
        
                        while z_current <= z_max: 

                           # print(point_num)

                                point_coords[0,0]=centre[0,0]+x_current
                                point_coords[0,1]=centre[0,1]+y_current
                                point_coords[0,2]=centre[0,2]+z_current
                  
                                Bnet=c1.B(point_coords)
                                #print("coords and field") 
                                #print(point_coords[0,0],point_coords[0,1],point_coords[0,2],Bnet[0,0],Bnet[0,1],Bnet[0,2])

                                field_array[point_num,0] = point_coords[0,0]
                                field_array[point_num,1] = point_coords[0,1]
                                field_array[point_num,2] = point_coords[0,2]
                                field_array[point_num,3] = Bnet[0,0]
                                field_array[point_num,4] = Bnet[0,1]
                                field_array[point_num,5] = Bnet[0,2]

                                point_num=point_num+1
                                z_current = z_current+dz


                        y_current=y_current+dz

                x_current = x_current + dz

        #Coordinates

        total_field[:,0] = field_array[:,0]
        total_field[:,1] = field_array[:,1]
        total_field[:,2] = field_array[:,2]

        #Magnetic field 
        total_field[:,3] = total_field[:,3]+field_array[:,3]
        total_field[:,4] = total_field[:,4]+field_array[:,4]
        total_field[:,5] = total_field[:,5]+field_array[:,5]

        print("Coil = ",coil_count,field_array[coords_total-1,:])
        print("Total so far : Coil = ",coil_count,total_field[coords_total-1,:])

      #  print(total_field[coords_total-1,:])
        #print(N[coil_count-1]*I[coil_count-1])

        coil_count=coil_count+1

    count=0

    B_file= open("TF_B.csv", "w")
    print("x,y,z,Bx,By,Bz,Bmag",file=B_file)

    while count<=coords_total-1: 

        print(total_field[count,0],",",total_field[count,1],",",total_field[count,2],",",total_field[count,3],",",total_field[count,4],",",total_field[count,5],file=B_file)
        #print(N[coil_count-1]*I[coil_count-1])
        count=count+1

   # print ("Centre point: ",x_centre,y_centre)




        

    











