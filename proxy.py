from flask import Flask, request
app = Flask(__name__)

import requests

@app.route('/')
def ok():
    return serve(request)

@app.route("/<path:path>/")
def rest(path):
    return serve(request)

def serve(request):
    r = requests.get(request.url, stream=True, proxies={'http': ""})
    out = ""
    for chunk in r.iter_content(1024):
        out += chunk
    return out

if __name__ == "__main__":
    app.run(debug=True, port=1337)
