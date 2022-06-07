#完成扫描工作
from logging import exception
import cv2
import numpy as np
import os
import sys
import ocrmypdf
import shutil
from fpdf import FPDF
from .scan import transform, scan

def scanocr(img_path,dst_path,model,ocr):
    paper = ''
    # model = input("====please type Enter for img2img and 1 for img2pdf====")
    # ocr = input("====please enter 1 if you need OCR (only available in img2pdf mode)====")
    pdf = FPDF()
    pdf.set_auto_page_break(0)
    pics = os.listdir(img_path)
    if model =='1':
        os.makedirs(dst_path+"/scanned")
    for pic in pics:
        try:
            img = cv2.imread(img_path+"/"+pic)
            img_trans = transform(img,paper)
            img_scan = scan(img_trans)
        except:
            continue
        if model != '1':
            cv2.imwrite(dst_path+"/"+pic,img_scan)
        else:
            cv2.imwrite(dst_path+"/scanned/"+pic,img_scan)
        if model == '1':
                pdf.add_page()
                size =  (210,270)
                pdf.image(dst_path+'/scanned/'+pic,x=0,w=size[0],h=size[1])
    if model == '1':
        pdf.output(dst_path+"/merge.pdf")
        shutil.rmtree(dst_path+'/'+'scanned')
    if ocr =='1':
        ocrmypdf.ocr(dst_path+"/merge.pdf",dst_path+"/ocr.pdf",language="chi_sim+eng")
        os.remove(dst_path+"/merge.pdf")