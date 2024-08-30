import cv2
import numpy as np

# Bild einlesen
image = cv2.imread('calib_zed.png')

# Konvertiere das Bild in den HSV-Farbraum
hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

# Erhöhe die Sättigung in stark beleuchteten Bereichen
h, s, v = cv2.split(hsv_image)
s = cv2.equalizeHist(s)
v = cv2.equalizeHist(v)
hsv_image = cv2.merge([h, s, v])

# Konvertiere das Bild zurück in den BGR-Farbraum
image_corrected = cv2.cvtColor(hsv_image, cv2.COLOR_HSV2BGR)

# Fahre mit der Farbsegmentierung und Kantenerkennung fort
hsv_image_corrected = cv2.cvtColor(image_corrected, cv2.COLOR_BGR2HSV)

# Definiere die Farbbereiche für Rot
lower_red_1 = np.array([0, 50, 50])
upper_red_1 = np.array([10, 255, 255])

lower_red_2 = np.array([170, 50, 50])
upper_red_2 = np.array([180, 255, 255])

# Erstelle Masken für die roten Bereiche
mask1 = cv2.inRange(hsv_image_corrected, lower_red_1, upper_red_1)
mask2 = cv2.inRange(hsv_image_corrected, lower_red_2, upper_red_2)

# Kombiniere die Masken
red_mask = mask1 + mask2

# Verwende Canny-Kantenerkennung
gray_image_corrected = cv2.cvtColor(image_corrected, cv2.COLOR_BGR2GRAY)
edges = cv2.Canny(gray_image_corrected, 50, 150)

# Kombiniere die Kantenerkennung mit der Rot-Farbmaske
canny_red_mask = cv2.bitwise_and(red_mask, red_mask, mask=edges)

# Anwende die kombinierte Maske auf das Originalbild
red_result = cv2.bitwise_and(image_corrected, image_corrected, mask=canny_red_mask)

# Zeige das Ergebnis an
cv2.imshow('Red Areas with Shadow Compensation and Canny Edges', red_result)
cv2.waitKey(0)
cv2.destroyAllWindows()

