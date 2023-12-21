
import face_recognition as fr
from pilt2 import sisselogimine
from flask import Flask, render_template, request, redirect, url_for, session
from flask_socketio import SocketIO, emit
import base64
from PIL import Image
import io
import numpy as np
messages=[]
app = Flask(__name__)
app.config["TEMPLATES_AUTO_RELOAD"] = True
app.config['SECRET_KEY'] = 'vnkdjnfjknfl1232#'
app.secret_key = "leboturvalineasjandus"
socketio = SocketIO(app)
TEMPLATES_AUTO_RELOAD = True
@app.route("/", methods=['GET', 'POST'])

def sessions():
    print("Received a request")
    if request.method == 'POST' and 'registreeri' in request.form:
        return redirect(url_for("regi"))
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
        if "Kasutaja" in session and session["Kasutaja"] != "0":
            kasutaja = session["Kasutaja"]
            user_message = request.form.get('user_message')
            if user_message:
                messages.append({'kasutaja': kasutaja, 'tekst': user_message})
                socketio.emit('message', {'kasutaja': kasutaja, 'tekst': user_message}, broadcast=True)
        return redirect(url_for("foorum"))
    else:
        try:
            if "Kasutaja" in session and session["Kasutaja"] != "0":
                kasutaja1 = session["Kasutaja"]
                return render_template("index.html", kasutaja1=kasutaja1, messages=messages)
            else:
                return render_template("keeld.html")
        except:
            return render_template("keeld.html")
@app.route("/regi", methods=['GET', 'POST'])
def regi():
    error = None
    if request.method == 'POST':
        file=open("pildid.txt","r",encoding="utf-8")
        nimi={}
        koik=[]
        nimi_ei_ole_olemas=0
        for i in file:
            koik.append(i)
            i=i.strip("\n").split(" ")
            nimi[i[0]]=i[1]
        file.close()
        kasutaja= request.form['username']
        if " " in kasutaja:
            return render_template('reg.html', error="Kasutrajanimi ei tohi omada tühikuid")
        imgur=request.form['password']
        if kasutaja in nimi:
            error = 'Nimi on juba võetud'
        else:
            uus_nimi=[kasutaja,imgur]
            nimi_ei_ole_olemas=1
            error="Registreeritud"
        file=open("pildid.txt","w",encoding="utf-8")
        for i in koik:
            file.write(i)
            print(i)
        if nimi_ei_ole_olemas==1:
            file.write("\n"+uus_nimi[0]+" "+uus_nimi[1])
        file.close()
        if error=="Registreeritud":
            return redirect(url_for("sessions"))
    return render_template('reg.html', error=error)
@socketio.on('connect')
def test_connect():
    print('Client connected')

@socketio.on('disconnect')
def test_disconnect():
    print('Client disconnected')
@socketio.on('message')
def handle_message(data):
    messages.append(data)
    emit('message', data, broadcast=True)



if __name__ == '__main__':
    socketio.run(app, debug=True)
