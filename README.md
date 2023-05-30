# SmartBookShelf

## Ai

书架图片识别主要由三个模块构成：

1. segment 使用 opencv 对书架原始照片进行处理，获取分割后的的书脊图片
2. ocr 使用 PaddleOCR 对书脊图片进行文字识别
3. character_match 使用 CNN 对形近字进行模糊匹配
4. sentence_match 通过相似度矩阵计算两个句子的相似程度

## Core

单片机运行核心逻辑代码