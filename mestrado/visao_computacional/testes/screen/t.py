import mss
import cv2
import numpy as np

with mss.mss() as sct:
    monitor = sct.monitors[1]  # tela principal
    while True:
        img = np.array(sct.grab(monitor))
        cv2.imshow("Screen Capture", img)
        if cv2.waitKey(1) == ord("q"):
            break
cv2.destroyAllWindows()
