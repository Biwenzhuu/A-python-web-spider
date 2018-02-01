import csv
import pandas as pd
from PIL import Image


a = pd.read_csv("labels.csv")
b = pd.read_csv("frame_meta.csv")
ab = pd.merge(a,b)
ab.to_csv('merge1.csv',index=True)

reader0 = csv.reader(open("merge2.csv"))
reader1 =csv.reader(open("merge2.csv"))

index_img1 ={}
index_coor1 ={}
index_img1 = {column[0]:
                    column[8] for column in reader0}
del index_img1['']
print(index_img1)
#mapping img with index, example: {'0': 'frames/1_0.jpg'}


index_coor1 = {column[0]:
                   [column[4], column[5], column[6]]for column in reader1}
del index_coor1['']
print(index_coor1)
#mapping box's coor with index, example {'0': ['668', '1408', '72']}

        #print(index_coor1[key1][0])

for key1 in index_coor1:
        boxlist = []
        x0 = int(index_coor1[key1][0], 0) - int(index_coor1[key1][2], 0)
        y0 = int(index_coor1[key1][1], 0) - int(index_coor1[key1][2], 0)
        x1 = int(index_coor1[key1][0], 0) + int(index_coor1[key1][2], 0)
        y1 = int(index_coor1[key1][1], 0) + int(index_coor1[key1][2], 0)
        print(x0, y0, x1, y1)

box = (x0, y0, x1, y1)

boxlist.append(box)
print(boxlist)

for key in index_img1:
    #print(index_img1[key])
        image = Image.open('/Users/biwen/PycharmProjects/untitled14/keras_test/frames/'+ index_img1[key])
for key1 in index_coor1:

 cropped_image = image.crop(box)
 cropped_image.save('/Users/biwen/PycharmProjects/untitled14/keras_test/crop_pic/'+key1+'.jpg')
