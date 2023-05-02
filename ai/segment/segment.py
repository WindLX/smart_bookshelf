import cv2 as cv
import numpy as np
img = cv.imread('./50.jpg', 1)
img = img[900: 2100, 500: 5000]
img = cv.resize(img, None, fx=0.5, fy=0.5, interpolation = cv.INTER_CUBIC)

kernel = np.ones((4,4),np.float32) / 16
img = cv.filter2D(img, -1, kernel)

b = img.copy()
b[:, :, 1:] = 0

g = img.copy()
g[:, :, 0::2] = 0

r = img.copy()
r[:, :, 0:2] = 0

b = cv.filter2D(b, -1, kernel)
r = cv.filter2D(r, -1, kernel)

img = b + g + r

gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

k1 = np.array([
    [0, -1, 0],
    [-1, 4, -1],
    [0, -1, 0]
])
edges_1 = cv.filter2D(gray, -1, k1)

_, edges_1 = cv.threshold(edges_1, 10, 255, cv.THRESH_BINARY)

edges_2 = cv.Canny(gray, 10, 150, apertureSize = 3)

e = edges_1 + edges_2
edges = edges_1 + edges_2

open = cv.morphologyEx(edges, cv.MORPH_OPEN, kernel)
close = cv.morphologyEx(edges, cv.MORPH_CLOSE, kernel)

edges -= close
edges -= open

k_3 = np.ones((3, 3), np.float32)
k_4 = np.ones((4, 4), np.float32)
# edges = cv.dilate(edges, k_3, iterations=3)
# edges = cv.erode(edges, k_4, iterations=1)

k_5 = np.array([[0, 1, 0],
                [1, -4, 0],
                [0, 1, 0]])
edges = cv.filter2D(edges, -1, kernel)

_, edges = cv.threshold(edges, 50, 255, cv.THRESH_BINARY)

edges = cv.erode(edges, k_3, iterations=1)

lines = cv.HoughLinesP(edges, 1, 1 * np.pi / 180, 5, minLineLength=10, maxLineGap=1)
# lines = cv.HoughLines(edges, 1, 1 * np.pi / 180, 250)
# for line in lines:
#     rho, theta = line[0]
#     fi_1 = (theta <= 2 * np.pi / 180 and theta >= 0)
#     fi_2 = (theta <= np.pi and theta >= 178 * np.pi / 180)
#     if fi_1 or fi_2:
#         a = np.cos(theta)
#         b = np.sin(theta)
#         x0 = a * rho
#         y0 = b * rho
#         x1 = int(x0 + 1000 * (-b))
#         y1 = int(y0 + 1000 * (a))
#         x2 = int(x0 - 1000 * (-b))
#         y2 = int(y0 - 1000 * (a))
#         cv.line(img, (x1, y1), (x2, y2), (0, 0, 255), 2)

p_list = []
l_list = []

if lines is not None:
    for line in lines:
        x1, y1, x2, y2 = line[0]
        angle = np.arcsin((y2 - y1) / np.sqrt((y2 - y1) ** 2 + (x2 - x1) ** 2))
        if (angle >= -np.pi / 180 * 92 and angle <= -np.pi / 180 * 90) or (angle <= np.pi / 180 * 92 and angle >= np.pi / 180 * 90):
            p_list.append((x1, y1, x2, y2))
            # print(p_list[-1])
            # cv.line(img, (x1, y1), (x2, y2), (0, 0, 255), 2)
            
for idx, p in enumerate(p_list):
    t = (p[0] - p[2]) / (p[1] - p[3])
    h = p[0] - t * p[1]
    if len(l_list) > 1:
        (t_0, h_0) = l_list[-1]
        if int(t_0) == 0:
            l_list.append((int(t), int(h)))
    else:
        l_list.append((int(t), int(h)))

l_list = list(set(l_list))
l_list = sorted(l_list, key=lambda l: l[1])

idx = 0
while(True):
    if idx < len(l_list) - 1:
        if abs(l_list[idx][1] - l_list[idx + 1][1]) < 20:
            l_list.remove(l_list[idx + 1])
        else:
            idx += 1
    else:
        break

for l in l_list:
    y1 = 0
    x1 = l[0] * y1 + l[1]
    y2 = 1000
    x2 = l[0] * y2 + l[1]
    print(l)
    # print((x1, y1), (x2, y2))
    cv.line(img, (int(x1), int(y1)), (int(x2), int(y2)), (0, 0, 255), 2)
# cv.imshow("img", b_edges)
cv.imshow("img", e)
# cv.imshow("img", img)
cv.waitKey(0)
cv.destroyAllWindows()
