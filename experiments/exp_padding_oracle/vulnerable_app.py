from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello():
    return "hello world"

if __name__ == '__main__':
    # Chạy ở 0.0.0.0 để container mở port ra ngoài
    app.run(host='0.0.0.0', port=5000)