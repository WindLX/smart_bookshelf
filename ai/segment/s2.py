import cv2
import numpy as np
from imutils.object_detection import non_max_suppression

# 读取图像
image = cv2.imread('./50.jpg', 1)
image = image[900: 2100, 500: 5000]
image = cv2.resize(image, None, fx=0.5, fy=0.5, interpolation = cv2.INTER_CUBIC)

# 加载EAST模型
net = cv2.dnn.readNet('frozen_east_text_detection.pb')

# 获取输入图像的尺寸和比例因子，以便在下一步进行尺度归一化
(h, w) = image.shape[:2]
newW = 320
newH = 320
rW = w / float(newW)
rH = h / float(newH)

# 构建一个blob（二进制大对象），用于将图像输入到网络中进行预测
blob = cv2.dnn.blobFromImage(image, 1.0, (newW, newH), (123.68, 116.78, 103.94), swapRB=True, crop=False)

# 将blob输入到网络中进行预测，并获取输出层名称
net.setInput(blob)
outputLayers = ["feature_fusion/Conv_7/Sigmoid", "feature_fusion/concat_3"]

# 进行文本检测
(scores, geometry) = net.forward(outputLayers)
# geometry = geometry[0]
# print(geometry.shape)
# scores = scores[0]
# 对scores进行阈值处理，以得到二值图像
(minConfidence, maxOverlap) = (1e-10, 0.3)
rects = []
confidences = []
for y in range(0, scores.shape[0]):
    scoresData = scores[y]
    x0 = geometry[:, 0, y]
    x1 = geometry[:, 1, y]
    x2 = geometry[:, 2, y]
    x3 = geometry[:, 3, y]
    angles = geometry[0, 4, y]

    for i in range(0, scoresData.shape[1]):
        # if scoresData[0, i] < minConfidence:
            # continue

        (offsetX, offsetY) = (i * 4.0, y * 4.0)

        angle = angles[i]
        cos = np.cos(angle)
        sin = np.sin(angle)

        h = x0[0, i] + x2[0, i]
        w = x1[0, i] + x3[0, i]

        endX = int(offsetX + (cos * x1[0, i]) + (sin * x2[0, i]))
        endY = int(offsetY - (sin * x1[0, i]) + (cos * x2[0, i]))
        startX = int(endX - w)
        startY = int(endY - h)

        rects.append((startX, startY, endX, endY))
        confidences.append(scoresData[0, i])

# 应用非极大值抑制算法（NMS）来去除重叠的边界框
boxes = non_max_suppression(np.array(rects), probs=confidences, overlapThresh=maxOverlap)

# 循环遍历每个边界框，并在原始图像中切割出书脊并用矩形框标记
for (startX, startY, endX, endY) in boxes:
    # 将坐标进行尺度还原
    startX = int(startX * rW)
    startY = int(startY * rH)
    endX = int(endX * rW)
    endY = int(endY * rH)
    
    # 切割出书脊并用矩形框标记
    book_spine = image[startY:endY, startX:endX]
    cv2.rectangle(image, (startX, startY), (endX, endY), (0, 0, 255), 2)

cv2.imshow('Book Spines', image)
cv2.waitKey(0)
cv2.destroyAllWindows()

