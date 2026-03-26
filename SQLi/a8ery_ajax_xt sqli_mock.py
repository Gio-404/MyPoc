from flask import Flask, request

app = Flask(__name__)

@app.route("/Service/Ajax_XT.ashx", methods=['post'])
def test():
    files = request.headers
    print(files)
    filecontent = files.read()
    print(filecontent)
    return 'ok'


app.run("0.0.0.0", debug=True)

