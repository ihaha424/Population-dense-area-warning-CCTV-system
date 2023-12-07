# Population-dense-area-warning-CCTV-system


인구 밀집시 탐지해주는 CCTV

# 개발 동기
작년 이태원 참사를 동기로 CCTV에서 인구 밀집도를 파악하고 경고를 할 수 있는 기능이 있으면 좋을 것 같다는 생각을 기반으로 만들게 됨.

# Structure

![image](https://github.com/ihaha424/Population-dense-area-warning-CCTV-system/assets/70957529/33bd01df-a254-44da-84a8-85b8bd695d24)
우선 라즈베리파이 환경에서 파이카메라를 통해 실시간 스트리밍 영상을 api통신을 통해 메인 서버로 통신
이후 플라스크 서버에서 받은 영상을 토대로 opencv와 yolo를 사용해 사람들을 탐지하고 탐지된 영상을 스트리링 서버로 출력
이 중 사람의 수를 탐지하여 군중으로 분류되거나 입력된 개체수를 넘을 경우 스트리밍 서버에 경고 표시
동시에 라즈베리 파이에 값을 보내서 블루투스통신을 이용해 스피커에서 경고음을 출력


## Raspi_code
raspi_code는 라즈베리 파이에 설치 후 필요한 모듈 설치
서버 주소 입력 후 사용가능

### 실행 방법
```
python streaming_to_server.py
```

## Server
server코드는 서버 컴퓨터에 설치 후 필요한 모듈 설치
yolov3다운도 필요

### 실행 방법
```
python flask_yolo4.py
```

# Demo

### Image
![image](https://github.com/ihaha424/Population-dense-area-warning-CCTV-system/assets/70957529/daceed1b-9d2b-4184-83a2-e44b17630638)

### Video
https://youtube.com/shorts/mQFFy-0LzXo
