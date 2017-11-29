# coding=utf-8
from osgeo import gdal
from gdalconst import *
import cv2
import math

inputBitNum = 8
outputBitNum = 16
bands = []
maxNums = []
band_data = []

root = raw_input("影像所在路径(e.g. E:\\)：\n")
root = root + "\\"
name = raw_input("影像名称(e.g. 1.tif)：\n")

# 以只读方式打开遥感影像
dataset = gdal.Open(root + name, GA_ReadOnly)

print "\n影像打开成功！\n"

# 输出影像信息
print '影像信息:'
print '影像类型:', dataset.GetDriver().ShortName
print '影像描述:', dataset.GetDescription()
print '影像包含波段数:', dataset.RasterCount
print "\n"

for i in range(dataset.RasterCount):
    bands.append(dataset.GetRasterBand(i + 1))

for i in range(dataset.RasterCount):
    print "波段", (i + 1).__str__(), ":"
    print "影像宽：", bands[i].XSize
    print "影像高：", bands[i].XSize
    print '数据类型:', bands[i].DataType
    print '影像最小最大值:', bands[i].ComputeRasterMinMax()
    print "-------------------------------"

    maxNums.append(bands[i].ComputeRasterMinMax()[1])

inputBitNum = int(math.ceil(math.log(max(maxNums), 2)))
print "读取影像位数：", inputBitNum

outputBitNum = raw_input("设置输出影像位数(2的整数次方)：\n")

for i in range(dataset.RasterCount):
    band_data.append(bands[i].ReadAsArray(0, 0, bands[i].XSize, bands[i].YSize))

if int(outputBitNum) < int(inputBitNum):
    param = int(pow(2, inputBitNum) / pow(2, int(outputBitNum)))
    for i in range(dataset.RasterCount):
        band_data[i] = band_data[i] / param
else:
    param = int(pow(2, int(outputBitNum)) / pow(2, inputBitNum))
    for i in range(dataset.RasterCount):
        band_data[i] = band_data[i] * param

print "波段信息:"
for i in range(dataset.RasterCount):
    print "[", i.__str__(), "]:band", (i + 1).__str__()

output_bands = raw_input(
    "指定输出图像的RGB波段顺序（逗号隔开，波段序号小于" + dataset.RasterCount.__str__() + "，如2,1,0）。若输出单波段灰度图，输入一个数字即可。：\n")

band_num = output_bands.split(",")

if int(outputBitNum) < int(inputBitNum):
    if band_num.__len__() < 3:
        datagray = band_data[int(band_num[0])]
        cv2.imwrite(root + name.split(".")[0] + "_" + band_num[0] + ".jpg", datagray)
        print "保存成功！路径： " + root + name.split(".")[0] + "_" + band_num[0] + ".jpg"
    else:
        datagray = cv2.merge([band_data[int(band_num[0])], band_data[int(band_num[1])], band_data[int(band_num[2])]])
        cv2.imwrite(root + name.split(".")[0] + ".jpg", datagray)
        print "保存成功！路径： " + root + name.split(".")[0] + ".jpg"
else:
    if band_num.__len__() < 3:
        datagray = band_data[int(band_num[0])]
        cv2.imwrite(root + name.split(".")[0] + "_" + band_num[0] + ".png", datagray)
        print "保存成功！路径： " + root + name.split(".")[0] + "_" + band_num[0] + ".png"
    else:
        datagray = cv2.merge([band_data[int(band_num[0])], band_data[int(band_num[1])], band_data[int(band_num[2])]])
        cv2.imwrite(root + name.split(".")[0] + ".png", datagray)
        print "保存成功！路径： " + root + name.split(".")[0] + ".png"
