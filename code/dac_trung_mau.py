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

def getPixel(image):
    img = cv2.imread(image)
    # Chuyển đổi sang không gian màu HLS để phát hiện màu sắc và làm nhận diện được từng kênh màu
    hls = cv2.cvtColor(img, cv2.COLOR_BGR2HLS)

    # Phân đoạn các vùng ảnh có đặc tính màu sắc tương tự
    # giá trị màu thấp nhất trong phạm vi màu đỏ mà chúng ta muốn nhận dạng
    lower_red = np.array([0, 50, 50])
    # giá trị màu cao nhất trong phạm vi màu đỏ mà chúng ta muốn nhận dạng
    upper_red = np.array([10, 255, 255])
    # Kết quả của hàm cv2.inRange là một ảnh nhị phân (binary image) có cùng kích thước và định dạng như ảnh đầu vào. 
    # Trong ảnh nhị phân này, các điểm ảnh nằm trong phạm vi màu đỏ được gán giá trị 255 (trắng), 
    # trong khi các điểm ảnh nằm ngoài phạm vi màu đỏ được gán giá trị 0 (đen).
    mask_red = cv2.inRange(hls, lower_red, upper_red)

    lower_green = np.array([40, 50, 50])
    upper_green = np.array([70, 255, 255])
    mask_green = cv2.inRange(hls, lower_green, upper_green)

    lower_blue = np.array([100, 50, 50])
    upper_blue = np.array([130, 255, 255])
    mask_blue = cv2.inRange(hls, lower_blue, upper_blue)

    # Tính toán các chỉ số liên quan đến màu sắc của các vùng ảnh
    # đếm số lượng điểm ảnh khác 0(màu đỏ) trong ảnh nhị phân
    red_pixels = cv2.countNonZero(mask_red)
    green_pixels = cv2.countNonZero(mask_green)
    blue_pixels = cv2.countNonZero(mask_blue)

    cv2.waitKey(0)
    cv2.destroyAllWindows()

    return (red_pixels, green_pixels, blue_pixels)

def save(code_la, folder):
    listImage = getAllImage(folder)
    mycursor = mydb.cursor()
    sql = "INSERT INTO mau (code_la, red, green, blue) VALUES (%s, %s, %s, %s)"
    val = []
    for image in listImage:
        x=(code_la, getPixel(image)[0], getPixel(image)[1], getPixel(image)[2])
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