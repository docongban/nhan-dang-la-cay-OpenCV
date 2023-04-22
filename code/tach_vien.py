import cv2

# Đọc ảnh và chuyển sang ảnh xám
img = cv2.imread('E:\\Hoc truc tuyen K8\\CSDLDPT\\BTL\\phanloailacay_v2\\code\\test2.jpg')
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# Làm mờ ảnh để giảm nhiễu
blur = cv2.GaussianBlur(gray, (5,5), 0)

# Phát hiện biên của vật thể
edged = cv2.Canny(blur, 30, 150)

# Tìm các contour trong ảnh
contours, hierarchy = cv2.findContours(edged, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
for contour in contours:
    area = cv2.contourArea(contour)
    perimeter = cv2.arcLength(contour, True)
    # Tính các đặc trưng khác nếu cần
    # ...
    # Thêm các đặc trưng vào cơ sở dữ liệu
    sql = "INSERT INTO contours (area, perimeter) VALUES (%s, %s)"
    val = (area, perimeter)
    print(val)
# Vẽ contour lên ảnh gốc
cv2.drawContours(img, contours, -1, (0,255,0), 2)

# Hiển thị kết quả
cv2.imshow('image', img)
cv2.waitKey(0)
cv2.destroyAllWindows()
