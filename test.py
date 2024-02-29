from multiprocessing import freeze_support
from test import video_test
from test_constants import TEST_VIDEO
import os
import matplotlib
import tkinter

#video_test.readTest(TEST_VIDEO)
#video_test.mtcnnTest(TEST_VIDEO, 1)
#video_test.haarTest(TEST_VIDEO, 2)
# video_test.imgFilterTest(TEST_VIDEO,1)
#video_test.trackingTest(TEST_VIDEO, 1)
#video_test.trackingTest2(TEST_VIDEO)
#video_test.sceneChangeTest(TEST_VIDEO,4)
#video_test.sceneChangeTest2(TEST_VIDEO, 1) 
#video_test.test1(TEST_VIDEO, 2)

# 도커 matplotlib 세팅
matplotlib.use('TkAgg') 

if __name__ == "__main__":
    freeze_support()
    #os.environ['QT_QPA_PLATFORM_PLUGIN_PATH'] = '/usr/local/lib/python3.9/site-packages/cv2/qt/plugins'
    os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
    #video_test.saveTest(TEST_VIDEO)
    #os.environ["CUDA_VISIBLE_DEVICES"] = "-1"
    video_test.multiProcessPlayTest(TEST_VIDEO)
    #video_test.kMeansTest("./test.npy")

    #video_test.singlePlayTest(TEST_VIDEO)