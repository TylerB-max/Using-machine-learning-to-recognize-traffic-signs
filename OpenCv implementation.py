#!/usr/bin/env python
# coding: utf-8

# In[1]:


import cv2
import time
import datetime
#Email/text alert

import smtplib
from email.message import EmailMessage


# In[2]:


#Email and text alerts
def Email_Alert(subject, body, to):

    msg = EmailMessage()
    msg.set_content(body)
    msg['subject'] = subject
    msg['to'] = to
    

    user = "tbonner.tb3@gmail.com"
    msg['from']= user
    password = "csygmjqyyjmukbyj"

    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(user, password)
    server.send_message(msg)
    server.quit()

if __name__=='__main__':
    Email_Alert("Hey", "you cant stop the rain!", "tjbonner@aggies.ncat.edu")
    Email_Alert("Hey","We got action! Bogie in the trap!", "8502067571@vtext.com")


# In[3]:


import cv2
import time
import datetime

cap = cv2.VideoCapture(0)

face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
body_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_fullbody.xml")

detection = False
detect_stopped_time = None
timer_started = False 
SECONDS_TO_RECORD_AFTER_DETECTION = 5

frame_size = (int(cap.get(3)), int(cap.get(4)))
fourcc = cv2.VideoWriter_fourcc(*"mp4v")


while True:
    _, frame = cap.read()
    
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    bodies = face_cascade.detectMultiScale(gray, 1.3, 5)
    out = cv2.VideoWriter("Video.mp4", fourcc, 20, frame_size)
    
    if len(faces) + len(bodies) > 0:
        if detection:
            timer_started = False
        else:
            detection = True
            current_time = datetime.datetime.now().strftime("%d-%m-%Y-%H-%M-%S")
            out = cv2.VideoWriter(f"{current_time}.mp4", fourcc, 20, frame_size)
            print("Started Recording")
    elif detection:
        if timer_started:
            if time.time() - detect_stopped_time >= SECONDS_TO_RECORD_AFTER_DETECTION:
                detection = False
                timer_started = False
                out.release()
                Email_Alert("Security Breach", "Some one has entered your space", "tjbonner@aggies.ncat.edu")
                Email_Alert("Hey","We got action, Bogie in the trap!!", "8502067571@vtext.com")
                print("Stop Recording")
        else:
            timer_started = True
            detect_stopped_time = time.time()
            
    if detection:
        out.write(frame)
    
    #for (x, y, width, height) in faces:
        #cv2.rectangle(frame, (x, y,), (x + width, y + height), (255, 0, 0), 3)
    
    cv2.imshow("Camera", frame)
    
    
    
    if cv2.waitKey(1) == ord('q'):
        break
        

out.release()      
cap.release()
cv2.destroyAllWindows()


# In[ ]:





# In[ ]:




