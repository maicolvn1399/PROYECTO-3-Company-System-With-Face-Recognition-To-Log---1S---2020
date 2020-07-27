import face_recognition
import cv2
import numpy as np

#get a reference to the webcam
video_capture = cv2.VideoCapture(0)

#load a picture and learn how to recognize it
actor_image = face_recognition.load_image_file("jake_gyllenhaal.jpg")
actor_face_encoding = face_recognition.face_encodings(actor_image)[0]

#load a second picture and learn how to recognize it
bill_gates_image = face_recognition.load_image_file("bill_gates.jpg")
bill_gates_face_encodings = face_recognition.face_encodings(bill_gates_image)[0]

#load a third picture and learn how to recognize it
michael_image = face_recognition.load_image_file("michaelv.jpg")
michael_face_encodings = face_recognition.face_encodings(michael_image)[0]

#create lists of known face encodings and their names

known_face_encodings = [actor_face_encoding,bill_gates_face_encodings,michael_face_encodings]
known_face_names = ["Jake Gyllenhaal","Bill Gates","Michael"]

#Initialize variables
face_locations = []
face_encodings = []
face_names = []

process_this_frame = True

while True:
    #grab a single frame of the video
    ret,frame = video_capture.read()

    #resize a frame to 1/4 size for faster recognition processing
    small_frame = cv2.resize(frame,(0,0),fx=0.25,fy=0.25)

    #convert the image from BGR(openCV) to RGB color(face_recognition)
    rbg_small_frame = small_frame[:,:,::-1]

    #only process every other frame of video to save time
    if process_this_frame:

        #find all the faces and face encodings in the curren frame of the video
        face_locations = face_recognition.face_locations(rbg_small_frame)
        face_encodings = face_recognition.face_encodings(rbg_small_frame,face_locations)

        face_names = []
        for face_encoding in face_encodings:
            #see if the face is a math for the known faces
            matches = face_recognition.compare_faces(known_face_encodings,face_encoding)
            face = "Unknown"

            face_distances = face_recognition.face_distance(known_face_encodings,face_encoding)
            best_match_index = np.argmin(face_distances)
            if matches[best_match_index]:
                name = known_face_names[best_match_index]

            face_names.append(name)

    process_this_frame = not process_this_frame

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
video_capture.release()
cv2.destroyAllWindows()
