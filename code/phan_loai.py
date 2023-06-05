import cv2
import numpy as np
import os
import mysql.connector

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="admin",
  database="la_cay"
)

image = 'E:\Hoc truc tuyen K8\CSDLDPT\BTL\phanloailacay_v2\code/tia_to_1.png'

def getDacTrungMau(image):
    img = cv2.imread(image)
    # Chuyển đổi sang không gian màu HLS
    hls = cv2.cvtColor(img, cv2.COLOR_BGR2HLS)

    # Phân đoạn các vùng ảnh có đặc tính màu sắc tương tự
    lower_red = np.array([0, 50, 50])
    upper_red = np.array([10, 255, 255])
    mask_red = cv2.inRange(hls, lower_red, upper_red)

    lower_green = np.array([40, 50, 50])
    upper_green = np.array([70, 255, 255])
    mask_green = cv2.inRange(hls, lower_green, upper_green)

    lower_blue = np.array([100, 50, 50])
    upper_blue = np.array([130, 255, 255])
    mask_blue = cv2.inRange(hls, lower_blue, upper_blue)

    # Tính toán các chỉ số liên quan đến màu sắc của các vùng ảnh
    red_pixels = cv2.countNonZero(mask_red)
    green_pixels = cv2.countNonZero(mask_green)
    blue_pixels = cv2.countNonZero(mask_blue)

    cv2.waitKey(0)
    cv2.destroyAllWindows()

    return (red_pixels, green_pixels, blue_pixels)

def getDacTrungVien(image):
    img = cv2.imread(image)

    # Chuyển ảnh sang đen trắng và làm mịn để loại bỏ nhiễu
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5, 5), 0)

    # Sử dụng phương pháp Canny để phát hiện biên
    edges = cv2.Canny(blur, 100, 200)

    # Tìm các đường viền và xác định đa giác xấp xỉ
    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    approx = cv2.approxPolyDP(contours[0], 0.01 * cv2.arcLength(contours[0], True), True)

    # Tính toán các đặc trưng hình học của đa giác
    # Diện tích
    area = cv2.contourArea(approx)
    # Chu vi
    perimeter = cv2.arcLength(approx, True)
    x, y, w, h = cv2.boundingRect(approx)
    # tỉ lệ khung hình bằng chiều rộng chia chiều cao
    aspect_ratio = float(w) / h

    return (area,perimeter,aspect_ratio)

def duDoanMau(image):
    listDistanceMau = []

    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM mau")
    listMau = mycursor.fetchall()
    for x in listMau:
        listDistanceMau.append(np.sqrt((getDacTrungMau(image)[0] - int(x[2]))**2 + 
                                       (getDacTrungMau(image)[1] - int(x[3]))**2 + 
                                       (getDacTrungMau(image)[2] - int(x[4]))**2))
    return (listMau[listDistanceMau.index(min(listDistanceMau))][1], min(listDistanceMau))

def duDoanVien(image):
    listDistanceVien = []

    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM vien")
    listVien = mycursor.fetchall()
    for x in listVien:
        listDistanceVien.append(np.sqrt((getDacTrungVien(image)[0] - float(x[2]))**2 + 
                                       (getDacTrungVien(image)[1] - float(x[3]))**2 + 
                                       (getDacTrungVien(image)[2] - float(x[4]))**2))
    return (listVien[listDistanceVien.index(min(listDistanceVien))][1], min(listDistanceVien))

def getNameLaByCode(code):
    mycursor = mydb.cursor()
    mycursor.execute(f"SELECT * FROM la where code = '{code}'")
    listLa = mycursor.fetchall()

    return listLa[0][2]

laByMau = duDoanMau(image)
laByVien = duDoanVien(image)

if laByMau[0] != laByVien[0] :
    if laByMau[1] > laByVien[1]:
        print(f"Dự đoán đây là lá {getNameLaByCode(laByMau[0])}")
    elif laByMau[1] < laByVien[1]:
        print(f"Dự đoán đây là lá {getNameLaByCode(laByVien[0])}")
    else: print(f"Dự đoán đây là lá {getNameLaByCode(laByVien[0])}")
else: print(f"Dự đoán đây là lá {getNameLaByCode(laByVien[0])}")