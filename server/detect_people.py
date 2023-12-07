import cv2
import numpy as np

def floor_detection(image):
    # 이미지를 그레이스케일로 변환
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # 가우시안 블러 적용
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)

    # 캐니 에지 검출
    edges = cv2.Canny(blurred, 50, 150)

    # 허프 변환을 사용하여 직선 탐지
    lines = cv2.HoughLines(edges, 1, np.pi / 180, threshold=100)

    # 감지된 직선 그리기
    for line in lines:
        rho, theta = line[0]
        a = np.cos(theta)
        b = np.sin(theta)
        x0 = a * rho
        y0 = b * rho
        x1 = int(x0 + 1000 * (-b))
        y1 = int(y0 + 1000 * (a))
        x2 = int(x0 - 1000 * (-b))
        y2 = int(y0 - 1000 * (a))
        cv2.line(image, (x1, y1), (x2, y2), (0, 0, 255), 2)


def count_people(frame, net):
    # # 이미지 읽기
    img_array = np.array(frame)
    image = cv2.cvtColor(img_array, cv2.COLOR_RGB2BGR)

    height, width, _ = image.shape

    # 이미지를 모델 입력에 맞게 전처리
    blob = cv2.dnn.blobFromImage(image, 0.00392, (416, 416), (0, 0, 0), True, crop=False)
    net.setInput(blob)

    # 모델 실행
    outs = net.forward(net.getUnconnectedOutLayersNames())

    # 감지된 객체의 정보를 저장할 리스트
    people = []

    # 감지된 객체를 반복하여 사람인 경우 저장
    for out in outs:
        for detection in out:
            scores = detection[5:]
            class_id = np.argmax(scores)
            confidence = scores[class_id]
            if confidence > 0.5 and class_id == 0:  # class_id 0은 사람을 나타냄
                # print(detection)
                center_x = int(detection[0] * width)
                center_y = int(detection[1] * height)
                w = int(detection[2] * width)
                h = int(detection[3] * height)
                x = int(center_x - w / 2)
                y = int(center_y - h / 2)
                people.append((x, y, w, h, confidence))
    #바닥탐지
    #floor_detection(image)
    
    # print(people)
    # NumPy 배열로 변환
    people = np.array(people)

    # Non-Maximum Suppression 적용
    if len(people) > 0:
        indices = cv2.dnn.NMSBoxes(people[:, :4], people[:, 4], 0.5, 0.4)
        people_num = len(indices)
        # 감지된 사람 수 출력
        #print(f"인파(인원) 수: {people_num}")
        area = []
        # 이미지에 감지된 사람을 사각형으로 표시
        for i in indices:
            i = int(i)
            x, y, w, h = people[i, :4]
            cv2.rectangle(image, (int(x), int(y)), (int(x+w), int(y+h)), (255, 0, 0), 2)
            area.append(w*h)
        average = sum(area) / len(area)
        max_area = max(area)
        #군중 감지시 위험 표시
        if (average * 2 < max_area):
            print("Warning\n")
            # flag -1 - 위험
            return (image, -1)
        return (image, people_num)
    else:
        return (image, 0)