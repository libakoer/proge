
import face_recognition as fr
from pilt2 import sisselogimine
from flask import Flask, render_template, request, redirect, url_for, session
from flask_socketio import SocketIO
import base64
from PIL import Image
import io
import numpy as np
app = Flask(__name__)
app.config["TEMPLATES_AUTO_RELOAD"] = True
app.config['SECRET_KEY'] = 'vnkdjnfjknfl1232#'
app.secret_key = "leboturvalineasjandus"
socketio = SocketIO(app)
TEMPLATES_AUTO_RELOAD = True
@app.route("/", methods=['GET', 'POST'])

def sessions():
    print("Received a request")
    if request.method == 'POST':
        if 'action1' in request.form and request.form['action1'] == 'Logi sisse:':
            image_data = request.form.get('image')
            decoded_img = base64.b64decode(image_data)
            img = Image.open(io.BytesIO(decoded_img))
            img= img.convert('RGB')
            img2=np.array(img)
            login=sisselogimine(img2)
            session["Kasutaja"]=login
        else:
            render_template("session.html")

    return render_template("session.html")

@app.route("/foorum", methods=['GET', 'POST'])

def foorum():
    if request.method == 'POST':
        pass
    else:
        try:
            if "Kasutaja" in session and session["Kasutaja"]!="0":
                print(session["Kasutaja"])
                session.pop("Kasutaja")
                return render_template("index.html")
            else:
                print(session["Kasutaja"])
                return render_template("keeld.html")
        except:
            return render_template("keeld.html")


if __name__ == '__main__':
    socketio.run(app, debug=True)
