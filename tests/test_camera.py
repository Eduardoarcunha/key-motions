import cv2 as cv
import unittest

CAM=0

class TestCamera(unittest.TestCase):
    def test_camera_open(self):
        cam = cv.VideoCapture(CAM)
        self.assertTrue(cam.isOpened(), "The camera could not be opened.")
        cam.release()

if __name__ == "__main__":
    unittest.main()