from multiprocessing import freeze_support

from test import test 
from test_constants import TEST_PATH
import os


if __name__ == "__main__":
    freeze_support()

    os.environ['QT_QPA_PLATFORM_PLUGIN_PATH'] = '/usr/local/lib/python3.9/site-packages/cv2/qt/plugins'
    # os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
    #os.environ["CUDA_VISIBLE_DEVICES"] = "-1"
    
    test.imageTest(TEST_PATH)
    #test.guiTest("./view/ui/main.ui")

    #히스토그램 스트래칭
    #히스토그램 평활화
    # 이거 사용해보기기 vv
    # 넘바, 모조, 맵, 풀, joblib, tqdm 