import cv2


def take_screenshot ():
    cam = cv2.VideoCapture(0)
    cv2.namedWindow("screen capture")

    img_counter =0
    while(True):
        ret,frame = cam.read()
        if not ret:
            print("failed to grab frame")
            break
        cv2.imshow("test",frame)
        k = cv2.waitKey(1)
    # when escape key is hit
        if k%256 == 27:
            print("escape hit")
            break
    # when space bar is hit
        elif k%256 == 32 :
            img_name = "opencv_frame_{}.png".format(img_counter)
            cv2.imwrite(img_name,frame)
            print("screenshot taken")
            img_counter+=1

    cam.release()
    cv2.destroyAllWindows()
