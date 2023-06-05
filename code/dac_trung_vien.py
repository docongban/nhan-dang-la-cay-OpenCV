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

def getAllImage(folder):
    listPath = []
    for root, dirs, files in os.walk(f'E:\Hoc truc tuyen K8\CSDLDPT\BTL\phanloailacay_v2\la_cay/{folder}'):
        for file in files:
            p=os.path.join(root,file)
            listPath.append(p)
    return listPath

def get_dac_trung(image):
    img = cv2.imread(image)

    # Chuyển ảnh sang đen trắng và làm mịn để loại bỏ nhiễu
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # kích thước kernel (5, 5)(làm mờ 1 cách vừa phải, càng to thì càng mờ) và 
    # giá trị sigma (độ lệch chuẩn) là 0 (xác định mức độ phân tán của giá trị pixel trong kernel)
    # Giá trị sigma càng lớn, mức độ làm mờ càng cao. 
    # Khi giá trị sigma là 0, bộ lọc Gaussian trở thành một bộ lọc trung bình (average filter) và không có sự phân tán nào
    blur = cv2.GaussianBlur(gray, (5, 5), 0)

    # Sử dụng phương pháp Canny để phát hiện biên
    #  là một ảnh nhị phân, trong đó các điểm trên cạnh được đánh dấu là trắng (giá trị 255), 
    # trong khi các điểm không phải cạnh được đánh dấu là đen (giá trị 0). 
    edges = cv2.Canny(blur, 100, 200)

    # Tìm các đường viền và xác định đa giác xấp xỉ
    # chỉ lấy đường viền ngoài cùng
    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    # một tham số epsilon (0.01 lần chiều dài cung đường viền), xác định xem đường viền có đóng hay không
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

def save(name, folder):
    listImage = getAllImage(folder)
    mycursor = mydb.cursor()
    sql = "INSERT INTO vien (code_la, area, perimeter, aspect_ratio) VALUES (%s, %s, %s, %s)"
    val = []
    for image in listImage:
        x=(name, get_dac_trung(image)[0], get_dac_trung(image)[1], get_dac_trung(image)[2])
        print(x)
        val.append(x)
    mycursor.executemany(sql, val)
    mydb.commit()

save('bac_ha', 'bac_ha')
save('hung_chanh', 'hung_chanh')
save('hung_lui', 'hung_lui')
save('hung_que', 'hung_que')
save('kinh_gioi', 'kinh_gioi')
save('la_lot', 'la_lot')
save('la_mo', 'la_mo')
save('rau_diep_ca', 'rau_diep_ca')
save('rau_ram', 'rau_ram')
save('tia_to', 'tia_to')