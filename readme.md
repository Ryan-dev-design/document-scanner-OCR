# Scan and OCR

## 依赖

```
opencv = 4.5.4
pyqt5 = 5.15.6 
python = 3.8.12 
pytesseract = 0.3.9 
ocrmypdf = 13.4.7
```

此外,需要下载安装tesseract(包括中文识别)

windows安装教程(http://www.juzicode.com/image-tesseract-ocr5-install-on-windows/)

macOS安装教程(https://cloud.tencent.com/developer/article/1699411)

## 功能描述

基于opencv进行文档照片处理,并使用tesseract, ocrmypdf为扫描得到的pdf增加可复制的OCR层.

可以选择输出图片,原始pdf或可复制的pdf.

## 启动

在目录中运行`python main.py`即可启动图形界面.
