import cv2
import math
import numpy as np

class getEllipse:
    def __init__(self,img):
        self.img = img

    def dispEllipse(self,ellipse,img):
        img = cv2.ellipse(img,ellipse,(0,255,0),2)
        cv2.imshow("ELLIPSE", img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    def findcnt(self,contours):
        L_ord, i_max = -1, -1
        for i,cnt in enumerate(contours):
            L = len(cnt)
            if L > L_ord:
                L_ord = L
                i_max = i
        return contours[i_max]

    def getEllipse(self):
        ret,thresh = cv2.threshold(self.img,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
        imgEdge,contours,hierarchy = cv2.findContours(thresh, cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
        cnt = self.findcnt(contours)
        ellipse = cv2.fitEllipse(cnt)
        #self.dispEllipse(ellipse,self.img)

        return ellipse

    def getCoodinate(self,ellipse, theta):
        (center_x, center_y), (major, minor), angle = ellipse
        rows, cols = self.img.shape
        pi = math.pi
        x = major / 2 * np.cos(theta)
        y = minor / 2 * np.sin(theta)
        xy = np.array([x, y])
        angle = (angle / 360) * 2 * pi
        rot = np.array([[np.cos(angle), np.sin(angle)],
                        [-np.sin(angle), np.cos(angle)]])
        rotated = np.dot(rot, xy)

        rotated[0] = rotated[0] + center_x
        rotated[1] = rotated[1] + (741 - center_y)

        return rotated