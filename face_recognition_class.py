import face_recognition
import cv2
import numpy as np
import time
import tkinter
from tkinter import messagebox
import os
import glob
from pathlib import Path




#Initialize variables
face_locations = []
face_encodings = []
face_names = []

class FaceRecognition:
    def __init__(self):
        #get a reference to the webcam
        self.person_image = []
        self.known_person_encodings = []
        self.known_person_names = []
        self.process_this_frame = True


    def Recognize(self):
        video_capture = cv2.VideoCapture(0)
        for subdir, dirs, files in os.walk(r'C:\Users\Michael\Desktop\PROYECTO 3 - Company System With Face Recognition To Log - 1S - 2020\PROYECTO-3-Company-System-With-Face-Recognition-To-Log---1S---2020'):
            for filename in files:
                filepath = subdir + os.sep + filename

                if filepath.endswith(".jpg"):
                    print(filename)
                    self.person_image += [face_recognition.load_image_file(filename)]
                    self.known_person_names += [filename.replace(".jpg","").replace("_"," ").capitalize()]

        for pic in self.person_image:
            self.known_person_encodings += [face_recognition.face_encodings(pic)[0]]
            print("Encondings Done")

        while True:
            #grab a single frame of the video
            ret,frame = video_capture.read()

            #resize a frame to 1/4 size for faster recognition processing
            small_frame = cv2.resize(frame,(0,0),fx=0.25,fy=0.25)

            #convert the image from BGR(openCV) to RGB color(face_recognition)
            rbg_small_frame = small_frame[:,:,::-1]

            #only process every other frame of video to save time
            if self.process_this_frame:

                #find all the faces and face encodings in the curren frame of the video
                face_locations = face_recognition.face_locations(rbg_small_frame)
                face_encodings = face_recognition.face_encodings(rbg_small_frame,face_locations)

                face_names = []
                for face_encoding in face_encodings:
                    #see if the face is a math for the known faces
                    matches = face_recognition.compare_faces(self.known_person_encodings,face_encoding)
                    face = "Unknown"

                    face_distances = face_recognition.face_distance(self.known_person_encodings,face_encoding)
                    best_match_index = np.argmin(face_distances)
                    if matches[best_match_index]:
                        name = self.known_person_names[best_match_index]
                    else:
                        time.sleep(1)
                        root = tkinter.Tk()
                        root.withdraw()
                        tkinter.messagebox.showwarning("You're not registered","You can't be recognized, you need to register as a new user")
                        root.destroy()
                        video_capture.release()
                        cv2.destroyAllWindows()
                    face_names.append(name)

            self.process_this_frame = not self.process_this_frame

            #display the results
            for (top,right,bottom,left), name in zip(face_locations,face_names):
                #scale back up face locations since the frame we detected in was scaled to 1/4 size
                top *= 4
                right *= 4
                bottom *= 4
                left *= 4

                #draw a box around the face
                cv2.rectangle(frame,(left,top),(right,bottom),(0,0,255),2)

                #draw a label with a name below the face
                cv2.rectangle(frame,(left,bottom-35),(right,bottom),(0,0,255),cv2.FILLED)
                font = cv2.FONT_HERSHEY_DUPLEX
                cv2.putText(frame,name,(left+6,bottom-6),font,1.0,(255,255,255),1)

            #display the resulting image
            cv2.imshow('Video',frame)

            #Hit "q" on the keyboard to quit
            if cv2.waitKey(1) == 0xFF == ord("q"):
                break

        #release handle to the webcam
        self.video_capture.release()
        cv2.destroyAllWindows()


