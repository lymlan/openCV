import cv2
import argparse
import numpy as np

def main():

    H_min = 0
    S_min = 0
    V_min = 120
    H_max = 1280
    S_max = 255
    V_max = 720

    camera = cv2.VideoCapture("test_orange.mp4")
    size = (int(camera.get(cv2.CAP_PROP_FRAME_WIDTH)), int(camera.get(cv2.CAP_PROP_FRAME_HEIGHT)))
    fourcc = cv2.VideoWriter_fourcc(*'DIVX')  # 'x264' doesn't work
    out = cv2.VideoWriter('./videos/001_output.mp4',fourcc, 29.0, size, False)  
    while True:
        ret, image = camera.read()
        if ret == False: 
            break
        frame_to_thresh = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        image[image < 20] = 0

        image_red = np.array(image[:,:,2], dtype='float64')
        quick_fix = np.ones((1280, 720), dtype='float64')
        image_red += quick_fix
        image_blue = np.array(image[:,:,0], dtype='float64')
        image_green = np.array(image[:,:,1], dtype='float64')


        image_adjusted = image_red / (image_red + image_blue + image_green)

        low = 0.6 * np.ones((1280, 720), dtype='float64')
        high = 0.9 * np.ones((1280, 720), dtype='float64')
        thresh = cv2.inRange(image_adjusted, low, high)

        im2, contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)


        cv2.drawContours(image, contours, -1, (0,255,0), 3)
     #   cv2.drawContours(thresh, contours, -1, (0,1.2,0), 3) Some error to do with colouring, probably because of the normalisation of the colours...

        for c in contours:
            # compute the center of the contour            
            M = cv2.moments(c)
            if M["m10"] ==0:
                cX = 0
                cY = 0
            else:
                cX = int(M["m10"] / M["m00"])
                cY = int(M["m01"] / M["m00"])
    
            # draw the contour and center of the shape on the image
                cv2.drawContours(image, [c], -1, (0, 255, 0), 2)
                cv2.circle(image, (cX, cY), 7, (255, 255, 255), -1)
                cv2.putText(image, "center", (cX - 20, cY - 20),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
            

       # cv2.imshow("Tracking", thresh)
      #  cv2.imshow("adjusted", image_adjusted)
        cv2.imshow("Original", image) # original image with contours drawn on
    #    cv2.imshow("Thresh", thresh)
        out.write(image)
        #  cv2.imshow("Mask", mask)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    camera.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    main()
