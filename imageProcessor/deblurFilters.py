from scipy.signal import wiener
from skimage.restoration import denoise_tv_chambolle
import numpy as np

#얘는 노이즈 제거.. 디블러 알고리즘 아님..
def wienerFiltering(img):
    temp = img / 255.0
    return np.clip(np.dstack((
        wiener(temp[:,:,0]),
        wiener(temp[:,:,1]),
        wiener(temp[:,:,2])
    )) * 255.0, 0, 255).astype(np.uint8)


#
# Richardson-Lucy Deconvolution 알고리즘
# 얘는 블러커널이 필요함. 이는 트래킹 알고리즘으로 어느 정도 구현 가능할 듯. 대부분의 물체가 동일한 방향으로 왜곡이 있다면
#확률적으로 이 알고리즘을 사용하게 하면 될 듯 일단 보류. 과하다 현재로써는
#

#
# Blind Deconvolution 알고리즘
# 얘는 블러커널이 필요없음. 단 추정치가 필요함 이를 바탕으로 디블러하는거임. 이 추정치를 트래킹 알고리즘과 결합하면 좋을 듯
#
#

#얘는 디블러 알고리즘 아님 노이즈 제거
def TotalVariationDeblurringFiltering(img):
    return denoise_tv_chambolle(img, weight=0.01, channel_axis=2)