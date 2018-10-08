# Write this script at Text Editor in Blender

import bpy
import cv2
import numpy as np
import pprint
import math
from blendfig import getEllipse as el

def Map(val, old_min, old_max, new_min, new_max):
    return ((val - old_min) / (old_max - old_min)) * (new_max - new_min) + new_min

def main():
    S  = bpy.context.scene
    S.tool_settings.grease_pencil_source = 'OBJECT'

    if not S.grease_pencil:
        a = [ a for a in bpy.context.screen.areas if a.type == 'VIEW_3D' ][0]

        bpy.ops.gpencil.data_add( override )

    gp = S.grease_pencil

    if gp.layers:
        gpl = gp.layers[0]
    else:
        gpl = gp.layers.new('gpll', set_active = True )

    if gpl.frames:
        fr = gpl.active_frame
    else:
        fr = gpl.frames.new(1) 

    str = fr.strokes.new()
    str.draw_mode = '3DSPACE'

    strokeLength = 500 

    str.points.add(count = strokeLength )
        
    img = cv2.imread(r"Analysis image PATH (PNG file)", 0)
    row,col = img.shape
    
    origin = (0,0,0)
    x_len = 10
    y_len = 10
    
    ellipse1 = el.getEllipse(img)
    el_data = ellipse1.getEllipse()
    pi = math.pi
    theta = np.arange(0,2*pi+0.1,0.1)
    X = []
    Y = []
    for i,ang in enumerate(theta):
        x,y = ellipse1.getCoodinate(el_data,ang)
        X.append(Map(x,0,row,0,x_len)+origin[0]-0.5)
        Y.append(Map(y,0,col,0,y_len)+origin[1]-2.5)
    X = np.array(X)
    Y = np.array(Y)
    Z = [5 for th in range(len(X))]
    
    ellipse_coords = list(zip(Y,Z,X))

    points = str.points
    
    for k, coord in enumerate(ellipse_coords):
        points[k].co = coord
    
if __name__ == '__main__':
    main()