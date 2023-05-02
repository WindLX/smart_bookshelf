import cv2
import numpy as np

img = cv2.imread('./50.jpg', 1)
img = img[900: 2100, 500: 5000]
img = cv2.resize(img, None, fx=0.5, fy=0.5, interpolation = cv2.INTER_CUBIC)

gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
ret = np.zeros_like(gray)

# def CornerHarris(gray, ret):
#     gray_lpl1 = np.float32(gray)

#     block_size = 2  # 角点检测窗口大小
#     aperture_size = 11  # Sobel算子大小
#     k = 0.012  # Harris角点检测参数
#     thresh = 0.3  # 角点响应值的阈值

#     # 计算Harris角点响应值
#     dst = cv2.cornerHarris(gray_lpl1, block_size, aperture_size, k)

#     # 归一化响应值
#     dst_norm = cv2.normalize(dst, None, alpha=0, beta=255, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_32F)

#     # 选取角点
#     ret[dst_norm > thresh * dst_norm.max()] = [255]

#     # 转换图像格式，方便显示
#     ret = np.uint8(ret)

#     return gray*0.2 + cv2.bitwise_not(ret)*0.4

# CornerHarris(gray, ret)

edge = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 13, -2)

rect_1 = cv2.getStructuringElement(cv2.MORPH_RECT, (edge.shape[0] // 80, 1))
rect_2 = cv2.getStructuringElement(cv2.MORPH_RECT, (25, 1))
rect_3 = cv2.getStructuringElement(cv2.MORPH_RECT, (9, 1))
rect_4 = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 1))

# MORPH_OPEN操作
hough = cv2.morphologyEx(edge, cv2.MORPH_OPEN, rect_1.reshape(-1))
# MORPH_CLOSE操作
hough = cv2.morphologyEx(hough, cv2.MORPH_CLOSE, rect_2.reshape(-1))
# MORPH_OPEN操作
hough = cv2.morphologyEx(hough, cv2.MORPH_OPEN, rect_3.reshape(-1), iterations=3)
# MORPH_OPEN操作
hough = cv2.morphologyEx(hough, cv2.MORPH_OPEN, rect_4.reshape(-1), iterations=30)

lines = cv2.HoughLinesP(hough, 1, 1 * np.pi / 180, 100, minLineLength=150, maxLineGap=0)

# for line in lines:
#     x1, y1 ,x2, y2 = line[0]
#     cv2.line(img, (x1, y1), (x2, y2), 255, 1)
    
# 计算直线的倾斜角度
def line_angle(line):
    x1, y1, x2, y2 = line[0]
    return np.arctan2(y2 - y1, x2 - x1) * 180 / np.pi

# 将直线按照从上到下的顺序排序
def sort_lines(lines):
    midpoints = [(line[0][0] + line[0][2]) / 2 for line in lines]
    return [line for _, line in sorted(zip(midpoints, lines), key=lambda x: x[0])]

def crop_regions(img, lines):
    sorted_lines = sort_lines(lines)
    regions = []
    for i in range(len(sorted_lines) - 1):
        line1 = sorted_lines[i]
        line2 = sorted_lines[i + 1]
        # angle1 = line_angle(line1)
        # angle2 = line_angle(line2)
        # if abs(angle1 - angle2) < 5 and abs(angle1) > 45:
        x1, _, x2, _ = line1[0]
        x3, _, x4,_ = line2[0]
        pt1 = (min(x1, x3), 0)
        pt2 = (max(x2, x4), 1000)
        region = img[pt1[1]:pt2[1], pt1[0]:pt2[0]]
        regions.append(region)
    return regions

regions = crop_regions(img, lines)

for i, region in enumerate(regions):
    if region.shape[0] <= 10 or region.shape[1] <= 15:
        continue
    print(region.shape)
    cv2.imshow(f'Region {i}', region)
print(len(list(filter(lambda x: not(x.shape[0] <= 10 or x.shape[1] <= 15), regions))))
# cv2.imshow("img", img)
cv2.waitKey(0)
cv2.destroyAllWindows()