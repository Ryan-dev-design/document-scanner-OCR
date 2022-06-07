import cv2
import numpy as np
def order_points(pts):
	rect = np.zeros((4, 2), dtype = "float32")
	s = pts.sum(axis = 1)
	rect[0] = pts[np.argmin(s)]
	rect[2] = pts[np.argmax(s)]
	diff = np.diff(pts, axis = 1)
	rect[1] = pts[np.argmin(diff)]
	rect[3] = pts[np.argmax(diff)]
	return rect

def scan(doc):
    doc_gray = cv2.cvtColor(doc,cv2.COLOR_BGR2GRAY)
    doc_thresh = cv2.adaptiveThreshold(doc_gray,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY,5,8)
    rectKernel = cv2.getStructuringElement(cv2.MORPH_RECT, (2, 2))
    kernel = np.ones((2,2),np.uint8)
    doc_close = cv2.morphologyEx(doc_thresh, cv2.MORPH_CLOSE, rectKernel)
    doc_erode = cv2.erode(doc_close,kernel)
    return doc_erode
def getpaper(paper):
    if paper == 'a4':
        return np.array(((0,0),(2099,0),(2099,2969),(0,2969)),np.float32)
    if paper == 'b5':
        return np.array(((0,0),(1819,0),(1819,2569),(1819,2569)),np.float32)
def transform(img,paper):
    if paper == "":
        paper = "a4"
    img_gray = cv2.equalizeHist(cv2.cvtColor(img,cv2.COLOR_BGR2GRAY))
    img_blur = cv2.GaussianBlur(img_gray,(55,55),1)
    thresh,img_thresh = cv2.threshold(img_blur,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
    kernel = np.ones((10,10),np.uint8)
    rectKernel = cv2.getStructuringElement(cv2.MORPH_RECT, (15, 15))
    img_erode = cv2.erode(img_thresh,kernel)
    edges = cv2.Canny(img_erode,100,200)
    kernel = np.ones((4,4),np.uint8)
    rectKernel = cv2.getStructuringElement(cv2.MORPH_RECT, (15, 15))
    edges_close = cv2.morphologyEx(edges, cv2.MORPH_CLOSE, rectKernel)
    edges_dilate = cv2.dilate(edges_close, kernel, iterations=3)
    contours, hierarchy =cv2.findContours(edges_dilate.copy(),cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    #按照面积排序,从大到小
    cnts = sorted(contours, key=cv2.contourArea, reverse=True)
    for c in cnts:
        # 计算轮廓周长,作为精确度的基准
        peri = cv2.arcLength(c, True)
        #轮廓近似
        # c表示输入的点集，epsilon表示从原始轮廓到近似轮廓的最大距离，它是一个准确度参数
        e=0.1
        approx = cv2.approxPolyDP(c, epsilon=e*peri, closed=True)

        # 确定检测到的是四边形,否则可能识别到了更大的轮廓
        if len(approx) == 4:
            screenCnt = approx.sum(1)
            break
    dst = getpaper(paper)
    screenCnt = order_points(screenCnt)
    M = cv2.getPerspectiveTransform(screenCnt,dst)
    doc = cv2.warpPerspective(img,M,tuple(int(x) for x in dst[2,:]))
    return doc