from flask import Flask, request, render_template, jsonify
import requests
from threading import Thread
from client import post, DataSet
from model.predict import run
import io
from PIL import Image
import wave
import pyaudio
from Ifasr import RequestApi
import socket
# from serial_adapter import Adapter

url = "http://localhost:8080"
file_path = "./ai/adapter/static/pic/1.jpeg"

books = []

app = Flask(__name__)
app.response_class.charset = 'utf-8'

host = '192.168.43.78'
port = 2233
# adapter = Adapter(port="COM3", baud=115200)

def ocr():
    global url
    if url != "":
        # adapter.transmit("b")
        res = post(url=f"{url}/ocr", file_path=file_path)
        # adapter.transmit("c")
        data_sets = DataSet.DataSetbuilder(res)
        global books
        books.clear()
        if len(data_sets) > 0:
            for e in sorted(data_sets, key=lambda data_set: data_set.coorinate):
                books.append((e.coorinate, e.connected_result))

def asr():
    chunk = 1024  # Record in chunks of 1024 samples
    sample_format = pyaudio.paInt16  # 16 bits per sample
    channels = 2
    fs = 44100  # Record at 44100 samples per second
    seconds = 3
    filename = "./ai/adapter/static/audio/output.wav"

    p = pyaudio.PyAudio()  # Create an interface to PortAudio

    print('Recording')

    stream = p.open(format=sample_format,
                    channels=channels,
                    rate=fs,
                    frames_per_buffer=chunk,
                    input=True)

    frames = []  # Initialize array to store frames

    # Store data in chunks for 3 seconds
    for _ in range(0, int(fs / chunk * seconds)):
        data = stream.read(chunk)
        frames.append(data)

    # Stop and close the stream 
    stream.stop_stream()
    stream.close()
    # Terminate the PortAudio interface
    p.terminate()

    print('Finished recording')

    # Save the recorded data as a WAV file
    with wave.open(filename, 'wb') as wf:
        wf.setnchannels(channels)
        wf.setsampwidth(p.get_sample_size(sample_format))
        wf.setframerate(fs)
        wf.writeframes(b''.join(frames))
        
    api = RequestApi(appid="d5f2605d",
                     secret_key="29e36a21a06fc7cc10a7553185748ab8",
                     upload_file_path=filename)
    asr_result = api.get_result()
    return asr_result

def match(data: str) -> list:
    result = []
    print("Comprehending")
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host , port))
    # adapter.transmit("a")
    s.sendall("a".encode("ascii"))
    for e in books:
        prop = run(data['description'], e[1])
        result.append(prop)
    try:
        result = [x[0] for x in enumerate(result) if x[1] > 0.7]
        print(result)
        book = [1 - books[index][0] for index in result]
        # adapter.transmit(f"{str(book)[1:-1]}")
        s.sendall(f"{str(book)[1:-1]}\n".encode("ascii"))
        return result
    except IndexError:
        return []

@app.route('/web', methods=['GET'])
def web():
    return render_template('index.html')

@app.route('/config', methods=['POST'])
def config():
    data = request.get_json()

    global url
    url = data['host']
    config = data['config']
    response = requests.post(url=f'{url}/config', json=config)    
    response.encoding = 'utf-8'

    if response.status_code == 200:
        response_data = {'message': response.content.decode()}
        return jsonify(response_data)

@app.route('/query', methods=['POST'])
def query():
    data = request.get_json()
    result = match(data)
    return jsonify({'result': result})

@app.route('/pic', methods=['POST'])
def pic():
    data = request.data
    
    if data:
        global file_path
        image_stream = io.BytesIO(data)
        image = Image.open(image_stream)
        image = image.transpose(Image.FLIP_LEFT_RIGHT) 
        image.save(file_path)
        ocr_thread = Thread(target=ocr)
        ocr_thread.start()
        ocr_thread.join()
        return "Upload Picture Successfully"
    else:
        return "Upload Picture Failed"

@app.route('/update', methods=['GET'])
def update():
    ocr_thread = Thread(target=ocr)
    ocr_thread.start()
    ocr_thread.join()
    return jsonify({"books": books})

@app.route('/record', methods=['GET'])
def record():
    print("Recognize")
    data = asr()
    data = {'description': data}
    result = match(data)
    return jsonify({'result': result})

if __name__ == '__main__':
    app.run(host="192.168.43.169", port=2020, debug=True)
    