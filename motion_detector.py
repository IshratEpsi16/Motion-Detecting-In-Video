import cv2, time, pandas        #using pandas to create data frame to store the starting and ending time of an object when it appears
from datetime import datetime   #importing datetime class from datetime library

first_frame = None              #none is an emtpy value which we assign to a variable to store the variable so that later we can use it
status_list = [None,None]       #if we don't write None, we will not able to find object.Cause it is impossible to find any value in an empty list
times = []

df = pandas.DataFrame(columns=["Start","End"])    #storing start and end time
video = cv2.VideoCapture(0)

while True:
    check, frame = video.read()
    status = 0                                    #0 indicates no motion in the current frame or camera
    gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY) #if you want black & white then use this line
    gray = cv2.GaussianBlur(gray,(21,21),0)       # it makes the image blur to remove noise. (21,21) is height and width of blur
    if first_frame is None:
        first_frame = gray                        # it represents the first frame of the video which we capture in the first iteration of the loop
        continue                                  #continue begining of the loop and go to the next iteration
    
    delta_frame = cv2.absdiff(first_frame,gray)   # difference between first frame and current frame
    thresh_frame = cv2.threshold(delta_frame,30,255,cv2.THRESH_BINARY)[1] #if the differnce of first and current frame values is more than 30 then it is white(255) and if less than 30 then black.
                                                                          #[1] first item of tuple as threshold returns tuple
    thresh_frame = cv2.dilate(thresh_frame,None,iterations=2)             #dilate increases the white region in the image 
    
    #contour of image
    (cnts,_) = cv2.findContours(thresh_frame.copy(),cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)  #cnts,_ is called contour
    for contour in cnts:
        if cv2.contourArea(contour) < 10000:                                                    # is contour less than 10000 px then goes to the next contour
            continue
        status = 1                                          #it means we get an object
        (x,y,w,h) = cv2.boundingRect(contour)               #(x,y,w,h) are cordinates
        cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),3)    #if greater or equal t0 10000 it will draw a rectangle.(0,255,0) is color of rectangle which is green
    status_list.append(status)
    
    #slicing which means list item will start from-2 index to the last index
    status_list=status_list[-2:]    
    #we want to store the time between [0,1] and [1,0]
    if status_list[-1] == 1 and status_list[-2] == 0:   
        times.append(datetime.now())
    if status_list[-1] == 0 and status_list[-2] == 1:
        times.append(datetime.now())    #dateime will record the time of each frame

    #showing images or say motion images
    cv2.imshow("Gray Frame",gray)
    cv2.imshow("Delta frame",delta_frame)
    cv2.imshow("Thresh frame",thresh_frame)
    cv2.imshow("Color Frame",frame)
    key=cv2.waitKey(1)   
    #to break the while loop entering z
    if key == ord('z'):   
        if status == 1:
            times.append(datetime.now())
        break

#if there is no motion object on the camera it will remain 0,if something apperas on it it will 1.[0,0,1,1,0] no motion,motion,no motion
print(status_list)
print(times)

for i in range(0,len(times),2): #it will iterate from 0 to length of list and step 2
    df = df.append({"Start":times[i],"End":times[i+1]},ignore_index=True)
df.to_csv("Times.csv")          #exporting the data frame to a CSV,shows us the starting and ending time

video.release()
cv2.destroyAllWindows()


