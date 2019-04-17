#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# =============================================================================
#       Description about this file here
#       Developers : Venkat Sai Krishna, 
#                   Vishruth Y S, 
#                   Sujay Biradar
# =============================================================================
#       Copyright (C) 2019  *Developers* 
# 
#       This program is free software: you can redistribute it and/or modify
#       it under the terms of the GNU General Public License as published by
#       the Free Software Foundation, either version 3 of the License, or
#       (at your option) any later version.
# 
#       This program is distributed in the hope that it will be useful,
#       but WITHOUT ANY WARRANTY; without even the implied warranty of
#       MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#       GNU General Public License for more details.
# 
#       You should have received a copy of the GNU General Public License
#       along with this program.  If not, see <https://www.gnu.org/licenses/>.
# =============================================================================

# =============================================================================
#       Removing the above copyright notice from the code is a direct breach 
#       of GNU's GPL v3.0 . If you have modified this code or developed 
#       any feature, feel free to append your name to the copyright name list.
#
#       This code is part of the repo https://github.com/vishruthys/VidGUI
# =============================================================================


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
        
    
