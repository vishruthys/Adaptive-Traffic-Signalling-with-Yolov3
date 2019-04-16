#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Mar 23 04:13:56 2019

@author: sujay
"""

def density_5(c0,c1,c2,c3,c4,wi): #to include auto
    wt=[1,0.5,4,5,0.75]#weight preset
    den=(c0*wt[0]+c1*wt[1]+c2*wt[2]+c3*wt[3]+c4*wt[4])/wi
    return den

def density_4(vehicle_count, width):
    wt = [1,0.5,4,5]#weight preset

    density = (vehicle_count[0]*wt[0]+
               vehicle_count[1]*wt[1]+
               vehicle_count[2]*wt[2]+
               vehicle_count[3]*wt[3])/(width)
    
    return density

def initial(density,l,preset_time):
    total_density = 0
    for i in range(len(density)):
        total_density += density[i]
#    print("total density ",total_den)
    for i in range(len(density)):
        if(l==i):
            it = density[i]/total_density
            break
        else:
            continue
        
    tt=it*(0.75*preset_time)
    if(tt<15):
        tt=15
        
    return tt

def extension(density,l,extn_count,prev_time,preset_time):#iteration 
    total_density = 0
    for i in range(len(density)):
        total_density += density[i]
    
    for i in range(len(density)):
        if(l==i):
            it = density[i]
            break
        else:
            continue
    
    ex=(3*it)/(total_density-it)
    
    print()
    print("ex ratio",ex)
    print()

    if (ex>=0.9 and extn_count==1):
        ex=0.075*preset_time*ex
        if(ex<=10):
            ext=10
        elif (ex>0.5*prev_time):
            ext=0.5*prev_time
        else:
            ext=ex
        return ext
    
    elif(ex<0.9 and extn_count==1):
        ext=0
        return ext
    elif(ex>=1.8 and extn_count==2):
        ex=0.0375*preset_time*ex
        if(ex<=10):
            ext=10
        elif (ex>0.25*prev_time):
            ext=0.25*prev_time
        else:
            ext=ex
        return ext
    else:
        ext=0
        return ext
        
    
   

	
	
"""
    if(ex>=0.9):
        if(extn_count==1):
            ex=0.075*preset_time*ex
            if(ex<=10):
                ext=10
            elif (ex>0.5*prev_time):
                ext=0.5*prev_time
            else:
                ext=ex
        else:
            ex=0.0375*preset_time*ex
            if(ex<=10):
                ext=10
            elif (ex>0.25*prev_time):
                ext=0.25*prev_time
            else:
                ext=ex
        return ext
    else:
        return 0
"""
        
