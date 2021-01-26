# Yolov3 교통사고 감지 모델 기반 flask 서버


## Getting started

#### Conda 가상환경 

```bash
# Tensorflow CPU
conda env create -f conda-cpu.yml
conda activate yolov3-cpu

# Tensorflow GPU
conda env create -f conda-gpu.yml
conda activate yolov3-gpu
```

#### Pip 패키지 설치

```bash
# TensorFlow CPU
pip install -r requirements.txt

# TensorFlow GPU
pip install -r requirements-gpu.txt
```

### pretrained weights 다운로드

For Windows:
You can download the yolov3 weights by clicking [here](https://pjreddie.com/media/files/yolov3.weights) and yolov3-tiny [here](https://pjreddie.com/media/files/yolov3-tiny.weights) then save them to the weights folder.

### Custom trained weights

미리 훈련시킨 가중치를 활용하여 진행한다.(교통사고 감지 - 정면 충돌 위주)
data/labels 폴더에 자신의 .names 파일을 추가하고 미리 훈련된 가중치 파일을 가중치 폴더에 넣는다.
Add your custom weights file to weights folder and your custom .names file into data/labels folder.
  
### Saving your yolov3 weights as a TensorFlow model.TensorFlow 모델로 yolov3 가중치를 저장

'load_weights.py'파일을 통해 가중치를 로드하면 .ckpt 모델로 변환된다.
```
# yolov3
python load_weights.py

# yolov3-tiny
python load_weights.py --weights ./weights/yolov3-tiny.weights --output ./weights/yolov3-tiny.tf --tiny
```
### 사고 영상 실행
'detect_video.py'파일을 통해 실행 가능하다.
```bash
명령어 python detect_video.py --video data/video/car_accident.mp4
```
data/video/ 폴더 안에 있는 mp4파일들로 실행가능하다.
![캡처](https://user-images.githubusercontent.com/64147798/105882257-ca20ef80-6048-11eb-8b58-946c28d23e43.PNG){: width="400" height="400"}
![캡처1](https://user-images.githubusercontent.com/64147798/105882306-d73dde80-6048-11eb-99c1-79ba8e72cce8.PNG){: width="400" height="400"}

#### 사고 감지 시 이미지 저장
\output 폴더 안에 사고 감지 시 이미지가 저장된다.


## Acknowledgments
* [Yolov3 Object Detection with Flask and Tensorflow 2.0](https://github.com/theAIGuysCode/Object-Detection-API)
* [Yolov3 TensorFlow 2 Amazing Implementation](https://github.com/zzh8829/yolov3-tf2)
* [Another Yolov3 TensorFlow 2](https://github.com/heartkilla/yolo-v3)
* [Yolo v3 official paper](https://arxiv.org/abs/1804.02767)
* [A Tensorflow Slim implementation](https://github.com/mystic123/tensorflow-yolo-v3)
