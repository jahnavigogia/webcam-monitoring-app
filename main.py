import cv2
import time
import glob
import os
from emailing import send_email
from threading import Thread

video = cv2.VideoCapture(0)
time.sleep(1)

first_frame = None
status_list = []
count = 1


def clean_folder():
    print("Clean folder function started.")
    images = glob.glob("images/*.png")
    for image in images:
        os.remove(image)
    print("Clean folder function completed.")


while True:
    status = 0
    check, frame = video.read()

    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray_frame_gau = cv2.GaussianBlur(gray_frame, (21, 21), 0)

    if first_frame is None:
        first_frame = gray_frame
    delt = cv2.absdiff(first_frame, gray_frame_gau)
    thresh = cv2.threshold(delt, 70, 255, cv2.THRESH_BINARY)[1]
    dil = cv2.dilate(thresh, None, iterations=2)

    con, check = cv2.findContours(dil, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    for cont in con:
        if cv2.contourArea(cont)<5000:
            continue
        x, y, w, h = cv2.boundingRect(cont)
        rect = cv2.rectangle(frame, (x, y), (x+w, y+h), (177, 155, 0), 3)

        if rect.any():
            status = 1
            cv2.imwrite(f"images/{count}.png", frame)
            count = count + 1
            all_im = glob.glob("images/*.png")
            index = int(len(all_im)/2)
            im_obj = all_im[index]

    status_list.append(status)
    status_list = status_list[-2:]
    if status_list[0] == 1 and status_list[1] == 0:
        email_thread = Thread(target=send_email, args=(im_obj, ))
        clean_thread = Thread(target=clean_folder)
        email_thread.start()
        email_thread.daemon = True
        clean_thread.start()
        clean_thread.daemon = True

    print(status_list)
    cv2.imshow("My video", frame)

    key = cv2.waitKey(1)

    if key == ord("q"):
        break

video.release()
