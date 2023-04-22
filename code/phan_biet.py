import cv2
import numpy as np
import os

image = 'E:\Hoc truc tuyen K8\CSDLDPT\BTL\phanloailacay_v2\code/test.jpg'

def getAllImage(folder):
    listPath = []
    for root, dirs, files in os.walk(f'E:\Hoc truc tuyen K8\CSDLDPT\BTL\phanloailacay_v2\la/{folder}'):
        for file in files:
            p=os.path.join(root,file)
            listPath.append(p)
    return listPath

def getDistance2Image(image1, image2):
    # Đọc ảnh lá cây gốc và ảnh lá cây cần so sánh
    img1 = cv2.imread(image1)
    img2 = cv2.imread(image2)

    # Chuyển ảnh sang đen trắng và làm mịn để loại bỏ nhiễu
    gray1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
    gray2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)
    blur1 = cv2.GaussianBlur(gray1, (5, 5), 0)
    blur2 = cv2.GaussianBlur(gray2, (5, 5), 0)

    # Sử dụng phương pháp Canny để phát hiện biên
    edges1 = cv2.Canny(blur1, 100, 200)
    edges2 = cv2.Canny(blur2, 100, 200)

    # Tìm các đường viền và xác định đa giác xấp xỉ
    contours1, _ = cv2.findContours(edges1, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contours2, _ = cv2.findContours(edges2, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    approx1 = cv2.approxPolyDP(contours1[0], 0.01 * cv2.arcLength(contours1[0], True), True)
    approx2 = cv2.approxPolyDP(contours2[0], 0.01 * cv2.arcLength(contours2[0], True), True)

    # Tính toán các đặc trưng hình học của đa giác
    # Diện tích
    area1 = cv2.contourArea(approx1)
    # Chu vi
    perimeter1 = cv2.arcLength(approx1, True)
    x1, y1, w1, h1 = cv2.boundingRect(approx1)
    # tỉ lệ khung hình bằng chiều rộng chia chiều cao
    aspect_ratio1 = float(w1) / h1 

    area2 = cv2.contourArea(approx2)
    perimeter2 = cv2.arcLength(approx2, True)
    x2, y2, w2, h2 = cv2.boundingRect(approx2)
    aspect_ratio2 = float(w2) / h2

    # So sánh đặc trưng
    # Dựa vào các đặc trưng như: diện tích, chu vi, tỉ lệ khung hình, tính toán khoảng cách giữa 2 lá cây
    # Khoảng cách giữa hai lá cây được tính bằng cách tính khoảng cách Euclidean (hay còn gọi là khoảng cách Euclid) 
    # giữa các giá trị đặc trưng của chúng

    # Giá trị của khoảng cách dist sẽ cho ta biết mức độ khác biệt giữa hai lá cây về các đặc trưng đã chọn. 
    # Nếu giá trị của khoảng cách dist nhỏ hơn một giá trị ngưỡng (ở đây là 50), chúng ta có thể kết luận rằng hai lá cây 
    # có các đặc trưng tương đồng và có thể là cùng một loại cây hoặc các loại cây có quan hệ gần gũi với nhau.
    dist = np.sqrt((area1 - area2)**2 + (perimeter1 - perimeter2)**2 + (aspect_ratio1 - aspect_ratio2)**2)
    return dist

def getDistanceFolder(folder):
    listImage = getAllImage(folder)
    count = 0
    total = 0
    for image in listImage:
        for img in listImage:
            count += 1
            total += getDistance2Image(image, img)
    return total/count
                
def getMinDistance():
    listDistance = []
    listDistance.append(getDistanceFolder('bac_ha_socola'))
    listDistance.append(getDistanceFolder('diep_ca'))
    listDistance.append(getDistanceFolder('hung_chanh'))
    listDistance.append(getDistanceFolder('hung_lui'))
    listDistance.append(getDistanceFolder('hung_que'))
    listDistance.append(getDistanceFolder('kinh_gioi'))
    listDistance.append(getDistanceFolder('la_not'))
    listDistance.append(getDistanceFolder('ngo'))
    listDistance.append(getDistanceFolder('rau_ram'))
    listDistance.append(getDistanceFolder('tia_to'))

    return min(listDistance)

# dist = getMinDistance()
dist = 77

def getDistance(img, folder):
    listImage = getAllImage(folder)
    listDistance = []
    for image in listImage:
        listDistance.append(getDistance2Image(img, image))

    return min(listDistance)

def du_doan(img):
    lst = []
    lst.append(getDistance(img,'bac_ha_socola'))
    lst.append(getDistance(img,'diep_ca'))
    lst.append(getDistance(img,'hung_chanh'))
    lst.append(getDistance(img,'hung_lui'))
    lst.append(getDistance(img,'hung_que'))
    lst.append(getDistance(img,'kinh_gioi'))
    lst.append(getDistance(img,'la_not'))
    lst.append(getDistance(img,'ngo'))
    lst.append(getDistance(img,'rau_ram'))
    lst.append(getDistance(img,'tia_to'))

    lstLa = ['Bạc hà', 'Diếp cá', 'Húng chanh', 'Húng lũi', 'Húng quế', 'Kinh giới', 'Lá lốt', 
             'Lá Ngò', 'Rau răm', 'Tía tô']

    print(f'Dự đoán đây là lá {lstLa[lst.index(min(lst))]}')

du_doan(image)