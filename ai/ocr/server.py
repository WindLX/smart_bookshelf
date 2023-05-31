from flask import Flask, request
import os
from config import config
from segment import Segmenter
from ocr import OCRer

app = Flask(__name__)
app.response_class.charset = 'utf-8'

@app.route('/ocr', methods=['POST'])
def ocr():
    # 获取图片文件
    if 'file' not in request.files:
        return 'No file part in the request', 400

    file = request.files['file']
    if file.filename == '':
        return 'No file selected', 400
    
    # 保存图片
    input_path = config['input_path']    
    if not os.path.exists(input_path):
        os.mkdir(input_path)
    file.save(f"{input_path}/{file.filename}")
    
    # 切割图片
    segmenter.segment(file.filename)
    coorinates = segmenter.coorinate
    
    # OCR
    ocr_results = ocrer.run_ocr()
    
    result = {key: (coorinates[key], ocr_results[key]) for key in coorinates if key in ocr_results}
    
    return result

@app.route('/clean', methods=['GET'])
def clean():
    segmenter.clean()
    return "Clean Successfully"

if __name__ == '__main__':
    segmenter = Segmenter(input_path=config['input_path'], output_path=config['output_path'], img_clip=config['img_clip'], img_scale=config['img_scale'], angle_point=config['angle_point'])
    ocrer = OCRer(input_path=config['output_path'], use_gpu=config['use_gpu'], thread_count=config['ocr_thread_count'])
    app.run(host="0.0.0.0", port=8080)
    