from paddleocr import PaddleOCR, draw_ocr
from flask import Flask, request

app = Flask(__name__)

@app.route('/')
def main():
    print("aa")
    return "<h1>hello!</h1>"

@app.route('/ocr', methods=['POST'])
def upload():
    if 'file' not in request.files:
        return 'No file part in the request', 400

    file = request.files['file']
    if file.filename == '':
        return 'No file selected', 400

    file.save(f"./temp/{file.filename}")
    
    ocr = PaddleOCR(use_angle_cls=True, lang="ch", use_gpu=True, show_log=None) 
    img_path = f"./temp/{file.filename}"
    result = ocr.ocr(img_path, cls=True)
    for idx in range(len(result)):
        res = result[idx]
        for line in res:
            print(line)
            
    return 'File saved successfully'

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8080)