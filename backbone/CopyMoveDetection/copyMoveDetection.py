import numpy as np
from sklearn.cluster import DBSCAN
from PIL import Image
import cv2
# https://medium.com/analytics-vidhya/copy-move-forgery-detection-using-sift-and-dbscan-clustering-4a179c36293e

class Detect(object):
    
    def __init__(self, file_name):
        self.image = cv2.imread(file_name)
        self.cmforgerypath = file_name.split('.')[0] + '_copyMove' + '.png'     
    
    def siftDetector(self):
        sift = cv2.SIFT_create()
        gray= cv2.cvtColor(self.image,cv2.COLOR_BGR2GRAY) 
        self.key_points,self.descriptors = sift.detectAndCompute(gray, None)
        return self.key_points,self.descriptors
    
    def showSiftFeatures(self):
        gray_image=cv2.cvtColor(self.image,cv2.COLOR_BGR2GRAY)
        sift_image=cv2.drawKeypoints(self.image,self.key_points,self.image.copy())
        return sift_image    
    
    def locateForgery(self,eps=40,min_sample=2):
        clusters=DBSCAN(eps=eps, min_samples=min_sample).fit(self.descriptors)
        size=np.unique(clusters.labels_).shape[0]-1
        forgery=self.image.copy()
        if (size==0) and (np.unique(clusters.labels_)[0]==-1):
            print('No Copy-Move Found!!')
            Image.fromarray(forgery).save(self.cmforgerypath)
            return None
        if size==0:
            size=1
        cluster_list= [[] for i in range(size)]
        for idx in range(len(self.key_points)):
            if clusters.labels_[idx]!=-1:
                cluster_list[clusters.labels_[idx]].append((int(self.key_points[idx].pt[0]),int(self.key_points[idx].pt[1])))
        for points in cluster_list:
            if len(points)>1:
                for idx1 in range(1,len(points)):
                    cv2.line(forgery,points[0],points[idx1],(255,0,0),2)
        
        
        Image.fromarray(forgery).save(self.cmforgerypath)

        return forgery

