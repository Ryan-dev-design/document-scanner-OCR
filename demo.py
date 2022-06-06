#完成扫描工作
import cv2
import numpy as np
import os
from fpdf import FPDF
from scan import transform, scan
img_path = input("====please enter the directory name of the pictures====")
paper = input("====please type the paper size (Enter for A4) ====")
model = input("====please enter 0 for img2img and 1 for img2pdf====")
ocr = input("====please enter 1 if you need OCR (only available in img2pdf mode)====")
pdf = FPDF()
pics = os.listdir(img_path)
if model == '0':
        os.makedirs(img_path+'\\'+'scanned')
for pic in pics:
    img = cv2.imread(img_path+"\\"+pic)
    img_trans = transform(img,paper)
    img_scan = scan(img_trans)
    if model == '0':
        cv2.imwrite(img_path+'\\'+'scanned\\'+pic,img_scan)
    if model == '1':
        if ocr == '1':
            #TODO OCR
            pass
        else:
            #TODO 合并为pdf
            pass