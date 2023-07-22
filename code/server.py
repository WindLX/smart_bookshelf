from flask import Flask, request
import os
import json
import logging
from config import Configer
from segment import Segmenter
from ocr import OCRer

app = Flask(__name__)
app.response_class.charset = 'utf-8'
app.logger.setLevel(logging.INFO)
if not os.path.exists('./log'):
    os.mkdir('./log')
file_handler = logging.FileHandler('./log/app.log')
file_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
app.logger.addHandler(file_handler)

@app.route('/ocr', methods=['POST'])
def ocr():
    # 获取图片文件
    if 'file' not in request.files:
        app.logger.warning('[ocr] No file part in the request')
        return 'No file part in the request', 400

    file = request.files['file']
    if file.filename == '':
        app.logger.warning('[ocr] No file selected')
        return 'No file selected', 400
    
    # 保存图片
    input_path = configer['segment_config']['input_path']    
    if not os.path.exists(input_path):
        os.mkdir(input_path)
    file.save(f"{input_path}/{file.filename}")
    
    # 切割图片
    segmenter.segment(file.filename)
    coorinates = segmenter.coorinate
    
    # OCR
    ocr_results = ocrer.run_ocr()
    
    result = {key: (coorinates[key], ocr_results[key]) for key in coorinates if key in ocr_results}
    
    app.logger.info('[ocr] OCR successfully')
    
    return result

@app.route('/clean', methods=['GET'])
def clean():
    segmenter.clean()
    app.logger.info('[clean] Clean successfully')
    return "Clean Successfully"

@app.route('/config', methods=['POST'])
def config():
    config_data = request.get_json()
    if config_data:
        with open('./config.json', 'w') as file:
            json.dump(config_data, file, indent=4)
            global segmenter, ocrer
        configer.update_config()
        segmenter = Segmenter.builder(configer['segment_config'])
        ocrer = OCRer.builder(configer['ocr_config'])
        app.logger.info('[config] Update config successfully')
        return "Update Config Successfully"
    else:
        app.logger.warning('[config] No JSON data found')
        return 'No JSON Data Found'

if __name__ == '__main__':
    configer = Configer('./config.json')
    segmenter = Segmenter.builder(configer['segment_config'])
    ocrer = OCRer.builder(configer['ocr_config'])
    app.run(host="0.0.0.0", port=8080, debug=False)
        