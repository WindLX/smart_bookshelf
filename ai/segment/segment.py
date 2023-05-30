import cv2
import numpy as np
from sklearn.cluster import KMeans

img = cv2.imread('../pic/4.jpg', 1)
# img = img[900: 2100, 500: 5000]
img = img[700: 2800, 0: 5000]
img = cv2.resize(img, None, fx=0.5, fy=0.5, interpolation = cv2.INTER_CUBIC)

gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
ret = np.zeros_like(gray)

edge = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 13, -2)

rect_1 = cv2.getStructuringElement(cv2.MORPH_RECT, (edge.shape[0] // 50, 1))
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

lines = cv2.HoughLinesP(hough, 1, 1 * np.pi / 180, 100, minLineLength=150, maxLineGap=10)

white = np.zeros_like(gray)

for line in lines:
    x1, y1 ,x2, y2 = line[0]
    cv2.line(white, (x1, y1), (x2, y2), 255, 1)

# 计算直线的倾斜角度
def line_angle(line):
    x1, y1, x2, y2 = line[0]
    return np.arctan2(y2 - y1, x2 - x1) * 180 / np.pi

# 将直线按照从上到下的顺序排序
def sort_lines(lines):
    midpoints = [(line[0][0] + line[0][2]) / 2 for line in lines]
    return [line for _, line in sorted(zip(midpoints, lines), key=lambda x: x[0])]

###########

def crop_regions(img, lines):
    sorted_lines = sort_lines(lines)
    regions = []
    i = 0
    while i < len(sorted_lines) - 1: 
        (pt1, pt2, delta_index) = judge_width(i, sorted_lines, 1)
        i += delta_index
        region = img[pt1[1]:pt2[1], pt1[0]:pt2[0]]
        regions.append(region)
    return regions

def judge_width(i, sorted_lines, delta_index):
    line1 = sorted_lines[i]
    if i + delta_index < len(sorted_lines):
        line2 = sorted_lines[i + delta_index]
    else:
        x1, _, x2, _ = line1[0]
        pt1 = (min(x1, x2), 0)
        pt2 = (max(x1, x2), 1000)
        return (pt1, pt2, delta_index)
    x1, _, x2, _ = line1[0]
    x3, _, x4,_ = line2[0]
    pt1 = (min(x1, x2), 0)
    pt2 = (max(x3, x4), 1000)
    if pt2[0] - pt1[0] <= 15:
        if i + delta_index < len(sorted_lines):
            delta_index += 1
            return judge_width(i, sorted_lines, delta_index)
        else:
            return (pt1, pt2, delta_index)
    else:
        return (pt1, pt2, delta_index)

###########

regions = crop_regions(img, lines)

for i, region in enumerate(regions):
    if region.shape[0] <= 10 or region.shape[1] <= 15:
        continue
    print(region.shape)
    # cv2.imshow(f'Region {i}', region)
    cv2.imwrite(f'./segment/temp/region_{i}.jpg', region)
print(len(list(filter(lambda x: not(x.shape[0] <= 10 or x.shape[1] <= 15), regions))))
# cv2.imshow("img", img)
# cv2.imshow("white", white)
# cv2.waitKey(0)
# cv2.destroyAllWindows()