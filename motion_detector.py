import cv2, time, pandas
from datetime import datetime

first_frame = None
status_list = [None,None]
times = []
dataframe = pandas.DataFrame(columns=["Start","End"])
#trigger the camera
video_reader = cv2.VideoCapture(0)

while True:

    #read the 1st frame
    check, frame = video_reader.read()

    #no motion in current frame
    status = 0

    #converting color frame into gray image/frame
    gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)

    gray= cv2.GaussianBlur(gray,(21,21),0)

    if first_frame is None:
        first_frame = gray
        continue
    
    delta_frame = cv2.absdiff(first_frame,gray)

    thresh_frame = cv2.threshold(delta_frame,30,255,cv2.THRESH_BINARY)[1]

    thresh_frame = cv2.dilate(thresh_frame, None, iterations=2)

    #IF get two white are then two 2 cnts
    (cnts,_) = cv2.findContours(thresh_frame.copy(),cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    #only want area greater than 1000 pixel

    for counter in cnts:
        #10000 is 100/100 pixel
        if cv2.contourArea(counter) < 10000:
            continue
        status = 1
        
        (w,x,y,z) = cv2.boundingRect(counter)
        cv2.rectangle(frame, (w,x), (w,y), (0,255,0),3)

    status_list.append(status)

    if status_list[-1] == 1 and status_list[-2] == 0:
        times.append(datetime.now())
    if status_list[-1] == 0 and status_list[-2] == 1:
        times.append(datetime.now())
    #time.sleep(5)

    #it shows the first frame of the video
    cv2.imshow("Gray Image",gray)
    cv2.imshow("Delta Frame",delta_frame)
    cv2.imshow("Threshold Frame",thresh_frame)
    cv2.imshow("color Frame",frame)

    key = cv2.waitKey(1)
    #print(gray)
    #print(delta_frame)

    if key == ord('q'):
        if status == 1:
            times.append(datetime.now())
        break

print(status_list)
print(times)

for values in range(0,len(times),2):
    #
    df=df.append({"Start":times[values],"End":times[values + 1]},ignore_index =True)

df.tocsv("Times.csv")

video_reader.release()
cv2.destroyAllWindows()