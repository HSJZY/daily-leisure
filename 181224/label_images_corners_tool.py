#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec 18 19:22:42 2018

@author: jiang
"""
import cv2
import numpy as np
from copy import deepcopy
import os

def order_marker_contour(contour):
    # sort this contour to the form as follow
    #   1....4
    #   .    .
    #   2....3
    if not isinstance(contour,list):
        contour=contour.tolist()
    contour=sorted(contour,key=lambda x:(x[0]),reverse=False)
    for index,corner_points in enumerate(contour):
        if len(corner_points)==1:
            contour[index]=corner_points[0]
    
    point_1_2=contour[:2]
    point_3_4=contour[2:]
    points=[]
    if point_1_2[0][1]<point_1_2[1][1]:
        points.append((point_1_2[0][0],point_1_2[0][1]))
        points.append((point_1_2[1][0],point_1_2[1][1]))
    else:
        points.append((point_1_2[1][0],point_1_2[1][1]))
        points.append((point_1_2[0][0],point_1_2[0][1]))
    if point_3_4[0][1]>point_3_4[1][1]:
        points.append((point_3_4[0][0],point_3_4[0][1]))
        points.append((point_3_4[1][0],point_3_4[1][1]))
    else:
        points.append((point_3_4[1][0],point_3_4[1][1]))
        points.append((point_3_4[0][0],point_3_4[0][1]))
    return np.array(points,dtype = "double")
    
def mark_plate(img):
    def get_click_x_y(event,x,y,flag,param):
        if event==cv2.EVENT_LBUTTONDOWN:
            cur_point=param[0]
            param[1][cur_point%4][0],param[1][cur_point%4][1]=x,y
            param[0]+=1
            print("x,y",x,y)
            cv2.circle(img,(x,y),10,(0,255,0),-1)
    img_cp=deepcopy(img)
    while(1):
        img=deepcopy(img_cp)
        cur_point=0
        points=[[-1,-1] for i in range(4)]
        param_cur=[cur_point,points]
        cv2.namedWindow('image',cv2.WINDOW_NORMAL)
        cv2.setMouseCallback('image', get_click_x_y,param=param_cur)
        key=-1
        while(1):
            cv2.imshow("image",img)
            key=cv2.waitKey(20)
            if param_cur[0]>=5:
                key=ord('q')
            if key!=-1 and param_cur[0]==4:
                break
            if key==ord('q'):
                break
        if key==ord('q'):
            print("已放弃当前标注，请重新标注该图片")
            continue
        points=order_marker_contour(points)
        print("points:",points)
        cv2.imshow("image",img)
        key=cv2.waitKey(0)
        cv2.destroyAllWindows()
        return points
def mark_images_of_directory(dir_path):
    file_names=os.listdir(dir_path)
    label_path='./labels'
    if not os.path.exists(label_path):
        os.mkdir(label_path)
    for filename in file_names:
        prefix_name=filename.split('.')[0]
        if len(filename.split('.'))==0:
            continue        
        img=cv2.imread(dir_path+'/'+filename)
        points=mark_plate(img)
        np.save(label_path+'/'+prefix_name,points)
def test():
#    img=cv2.imread('./test_img_1.jpg')
#    points=mark_plate(img)
#    print("points:",points)    
    dir_path='./images'
    mark_images_of_directory(dir_path)
if __name__=="__main__":
    test()
