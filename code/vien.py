# Import các thư viện cần thiết
import cv2
import numpy as np

# Đọc ảnh lá cây gốc và ảnh lá cây cần so sánh
img1 = cv2.imread('E:\\Hoc truc tuyen K8\\CSDLDPT\\BTL\\phanloailacay_v2\\code\\tia_to.jpg')
img2 = cv2.imread('E:\\Hoc truc tuyen K8\\CSDLDPT\\BTL\\phanloailacay_v2\\code\\kinh_gioi.jpg')

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
area1 = cv2.contourArea(approx1)
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
# Trong tập dữ liệu mẫu, khoảng cách giữa các đặc trưng của các lá cây khác nhau có trung bình khoảng 70 đến 80.
# (Điều này có thể được tính toán bằng cách lặp lại các bước xử lý ảnh và trích xuất đặc trưng với tất cả các lá cây 
# trong tập dữ liệu mẫu, sau đó tính toán khoảng cách giữa các đặc trưng của từng cặp lá cây và tính trung bình của 
# các khoảng cách này.)
# Vì vậy, nếu chúng ta chọn giá trị là 50, đây là một giá trị khá nhỏ so với giá trị trung bình. 
# Tuy nhiên, giá trị này có thể cho phép chúng ta nhận ra những lá cây giống nhau trong tập dữ liệu 
# mẫu mà khoảng cách giữa các đặc trưng của chúng nhỏ hơn trung bình.

# Nếu tập dữ liệu của chúng ta khác hoàn toàn so với tập dữ liệu mẫu, có thể sẽ cần điều chỉnh lại 
# giá trị này để phù hợp với tập dữ liệu mới.
if dist < 50:
    print(1, area1, perimeter1, aspect_ratio1)
    print('Hai lá cây giống nhau',dist)
    print(2, area2, perimeter2, aspect_ratio2)
else:
    print('Hai lá cây khác nhau',dist)

# Hiển thị ảnh và đa giác xấp xỉ
# cv2.drawContours(img1, [approx1], -1, (0, 255, 0), 2)
# cv2.drawContours(img2, [approx2], -1, (0, 255, 0), 2)
# cv2.imshow('Leaf 1', img1)
# cv2.imshow('Leaf 2', img2)
# cv2.waitKey(0)
# cv2.destroyAllWindows()