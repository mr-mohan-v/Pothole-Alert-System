import cv2 as cv
import time
import os
import gps_module as gps
import thingspeak

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
cap = cv.VideoCapture("test.mp4")
#cap = cv.VideoCapture(0)
cap.set(3,1280)
cap.set(4,720)
width  = cap.get(3)
height = cap.get(4)
print(width, height)

#defining initial values for some parameters in the script
starting_time = time.time()
frame_counter = 0
i = 0
b=0
last_lat = last_lng =0
print("Starting loop")
#detection loop
while True:
    ret, frame = cap.read()
    frame_counter += 1
    if ret == False:
        break
    #analysis the stream with detection model
    classes, scores, boxes = model1.detect(frame, confThreshold=0.6, nmsThreshold=0.4)
    for (classid, score, box) in zip(classes, scores, boxes):
        label = "pothole"
        x, y, w, h = box
        recarea = w*h
        area = width*height
        #drawing detection boxes on frame for detected potholes and saving coordinates txt and photo
        if(len(scores)!=0 and scores[0]>=0.5):
            if((recarea/area)<=0.1 and box[1]<600):
                cv.rectangle(frame, (x, y), (x + w, y + h), (0,255,0), 1)
                cv.putText(frame, str(int(scores[0]*100)) + "% " + label, (box[0], box[1]-10),cv.FONT_HERSHEY_COMPLEX, 0.5, (255,0,0), 1)
                print("Pothole detected")
                lat, lng =  gps.get_gps()
                if last_lat != lat and last_lng != lng:
                    last_lat = lat
                    last_lng = lng
                    thingspeak.upload_cloud(last_lat,last_lng)
                    print(last_lat,last_lng,"\n")
                i=i+1
    #writing fps on frame
    endingTime = time.time() - starting_time
    fps = frame_counter/endingTime
    cv.putText(frame, f'FPS: {fps}', (20, 50),
               cv.FONT_HERSHEY_COMPLEX, 0.7, (0, 255, 0), 2)
    #showing result
    cv.imshow('frame', frame)
    key = cv.waitKey(1)
    if key == ord('q'):
        break
#end
cap.release()
cv.destroyAllWindows()
