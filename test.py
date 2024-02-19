from multiprocessing import freeze_support
from test import video_test
from test_constants import TEST_VIDEO

#video_test.readTest(TEST_VIDEO)
#video_test.mtcnnTest(TEST_VIDEO, 1)
#video_test.haarTest(TEST_VIDEO, 2)
# video_test.imgFilterTest(TEST_VIDEO,1)
#video_test.trackingTest(TEST_VIDEO, 1)
#video_test.trackingTest2(TEST_VIDEO)
#video_test.sceneChangeTest(TEST_VIDEO,4)
#video_test.sceneChangeTest2(TEST_VIDEO, 1) 
#video_test.test1(TEST_VIDEO, 2)

if __name__ == "__main__":
    freeze_support()
    video_test.multiProcessPlayTest(TEST_VIDEO)