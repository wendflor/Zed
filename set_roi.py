import cv2
import numpy as np

def set_roi_manually(img):
    r = cv2.selectROI(img)
    imcrop = img[int(r[1]):int(r[1]+r[3]), int(r[0]):int(r[0]+r[2])]
    key = ''
    while key != 113:
        cv2.imshow("Image", imcrop)
        key = cv2.waitKey(1)

    cv2.destroyAllWindows()
    return r

def segment_red_color(hsv_image):
    """
    img: it gets an image in HSV format
    """    
    lower_red_1 = np.array([0, 50, 50])
    upper_red_1 = np.array([10, 255, 255])

    lower_red_2 = np.array([170, 50, 50])
    upper_red_2 = np.array([180, 255, 255])

    # Sehr helle rote Bereiche
    lower_bright_red = np.array([0, 50, 200])
    upper_bright_red = np.array([10, 255, 255])

    # Masken erstellen
    mask1 = cv2.inRange(hsv_image, lower_red_1, upper_red_1)
    mask2 = cv2.inRange(hsv_image, lower_red_2, upper_red_2)
    mask3 = cv2.inRange(hsv_image, lower_bright_red, upper_bright_red)

# Alle Masken kombinieren
    frame_threshold = mask1 + mask2 + mask3


    # Ergebnis anzeigen
    #frame_threshold = cv2.bitwise_and(image, image, mask=red_mask)

    return frame_threshold

if __name__ == "__main__":
    img = cv2.imread("calib_zed.png")
    rgb_image = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    hsvImage = cv2.cvtColor(rgb_image, cv2.COLOR_RGB2HSV)
    color_masked_image = segment_red_color(hsvImage)
    cv2.imshow('Red Areas', color_masked_image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    #roi=set_roi_manually(img)
    #print(roi)
        
   