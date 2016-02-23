import os
root_dir = os.path.abspath( os.path.dirname(__file__) )

from flask import Flask, send_from_directory
app = Flask(__name__, static_url_path=root_dir)

@app.route('/',defaults={'path':'index.html'})
def index(path):
    return send_from_directory('.',path)
    return app.send_static_file('index.html')


@app.route('/<path:dir>/<path:path>')
def send_js(dir,path):
    return send_from_directory(dir, path)

if __name__ == '__main__':
    app.run()
