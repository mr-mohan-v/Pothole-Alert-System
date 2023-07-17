import cv2 as cv
import time
import os
import gps_module as gps

from Adafruit_IO import Client,Feed
import time 

ADAFRUIT_IO_USERNAME = "pothole_detection"
ADAFRUIT_IO_KEY = "aio_cUMI34A0tzG4B908z5K2qXlW7WGA"

aio  = Client(ADAFRUIT_IO_USERNAME,ADAFRUIT_IO_KEY)
lat_feed = aio.feeds('gps.lat')
lon_feed = aio.feeds('gps.lon')


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
last_coordinates = ''
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
                cv.imwrite(os.path.join(result_path,'pothole'+str(i)+'.jpg'), frame)
                coordinates =  gps.get_gps()
                if last_coordinates != coordinates:
                    last_coordinates = coordinates
                    aio.send(lat_feed.key , coordinates[0:10])
                    aio.send(lon_feed.key , coordinates[14:24])
                    print(coordinates+"\n")
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
