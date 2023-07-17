import cv2 as cv
import time
import os
import gps_module as gps
import thingspeak

from imutils.video import WebcamVideoStream
import imutils

# import the necessary packages
from threading import Thread
import cv2
class WebcamVideoStream:
    def __init__(self, src=0):
        # initialize the video camera stream and read the first frame
        # from the stream
        self.stream = cv.VideoCapture(src)
        (self.grabbed, self.frame) = self.stream.read()
        # initialize the variable used to indicate if the thread should
        # be stopped
        self.stopped = False
    def start(self):
        # start the thread to read frames from the video stream
        Thread(target=self.update, args=()).start()
        return self
    def update(self):
        # keep looping infinitely until the thread is stopped
        while True:
            # if the thread indicator variable is set, stop the thread
            if self.stopped:
                return
            # otherwise, read the next frame from the stream
            (self.grabbed, self.frame) = self.stream.read()
    def read(self):
        # return the frame most recently read
        return self.frame
    def stop(self):
        # indicate that the thread should be stopped
        self.stopped = True
        
        
result_path = '/home/r7/Documents/project-pothole-detection/'

#importing model weights and config file
net1 = cv.dnn.readNet('project_files/yolov4_tiny.weights', 'project_files/yolov4_tiny.cfg')
print("imported model weights and config")
#defining the model parameters
model1 = cv.dnn_DetectionModel(net1)
model1.setInputParams(size=(216, 216), scale=1/255, swapRB=True)
print("defined model parameters")
#defining the video source (0 for camera or file name for video)
print("starting camera")
#cap = cv.VideoCapture("test.mp4")
#cap = cv.VideoCapture(0)
vs = WebcamVideoStream(src=0).start()

last_lat = last_lng =0
print("Starting loop")
#detection loop
while True:
    frame = vs.read()
    frame = imutils.resize(frame, width=400)
    
    #analysis the stream with detection model
    classes, scores, boxes = model1.detect(frame, confThreshold=0.6, nmsThreshold=0.4)
    for (classid, score, box) in zip(classes, scores, boxes):
        label = "pothole"
        x, y, w, h = box
        #drawing detection boxes on frame for detected potholes and saving coordinates txt and photo
        if(len(scores)!=0 and scores[0]>=0.5):
            if(box[1]<600):
                cv.rectangle(frame, (x, y), (x + w, y + h), (0,255,0), 1)
                cv.putText(frame, str(int(scores[0]*100)) + "% " + label, (box[0], box[1]-10),cv.FONT_HERSHEY_COMPLEX, 0.5, (255,0,0), 1)
                print("Pothole detected")
                lat, lng =  gps.get_gps()
                if last_lat != lat and last_lng != lng:
                    last_lat = lat
                    last_lng = lng
                    thingspeak.upload_cloud(last_lat,last_lng)
                    print(last_lat,last_lng,"\n")
    cv.imshow('frame', frame)
    key = cv.waitKey(1)
    if key == ord('q'):
        break
#end
cap.release()
cv.destroyAllWindows()
