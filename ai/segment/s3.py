import cv2
import numpy as np

# 加载EAST模型
net = cv2.dnn.readNet("frozen_east_text_detection.pb")

# 设置输入图像尺寸
width = 320
height = 320

# 加载测试图像
image = cv2.imread('./50.jpg', 1)
image = image[900: 2100, 500: 5000]
image = cv2.resize(image, None, fx=0.5, fy=0.5, interpolation = cv2.INTER_CUBIC)

width = image.shape[0]
height = image.shape[1]

# 预处理图像
blob = cv2.dnn.blobFromImage(image, 1.0, (width, height), (123.68, 116.78, 103.94), swapRB=True, crop=False)

# 设置模型输入
net.setInput(blob)

# 获取输出层名称
layerNames = [
    "feature_fusion/Conv_7/Sigmoid",
    "feature_fusion/concat_3"
]

# 运行模型
scores, geometry = net.forward(layerNames)

# 获取图像宽度和高度
H, W = image.shape[:2]

# 解析模型输出
rectangles = []
confidences = []

for y in range(0, H):
    scoresData = scores[0, 0, y]
    x0, x1, x2, x3 = (geometry[0, 0, y], geometry[0, 1, y], geometry[0, 2, y], geometry[0, 3, y])

    for i in range(0, W):
        if scoresData[i] < 0.5:
            continue

        offset = i * 4
        rectX = int(x0[offset] * i + x1[offset] * y + x2[offset])
        rectY = int(x0[offset + 1] * i + x1[offset + 1] * y + x2[offset + 1])
        rectW = int(x0[offset + 2] * i + x1[offset + 2] * y + x2[offset + 2])
        rectH = int(x0[offset + 3] * i + x1[offset + 3] * y + x2[offset + 3] * 0.4)

        rectangles.append((rectX, rectY, rectW, rectH))
        confidences.append(scoresData[i])

# 应用非最大抑制
indices = cv2.dnn.NMSBoxes(rectangles, confidences, 0.5, 0.3)

# 在原始图像上绘制边界框
for i in indices:
    i = i[0]
    box = rectangles[i]
    startX = max(0, box[0])
    startY = max(0, box[1])
    endX = min(W, box[0] + box[2])
    endY = min(H, box[1] + box[3])
    cv2.rectangle(image, (startX, startY), (endX, endY), (0, 255, 0), 2)

# 显示结果
cv2.imshow("Text Detection", image)
cv2.waitKey(0)
cv2.destroyAllWindows()
