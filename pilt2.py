import face_recognition as fr
import numpy as np
from PIL import Image
import requests
from io import BytesIO
#kõik impordid
def sisselogimine(a):
    lopp=""
    results=False
    try:
        kooding2=fr.face_encodings(a)[0]
    except:
        return "0"
    f=open("pildid.txt", "r", encoding="UTF-8")
    koik=[]
    for i in f:
        i=i.strip("\n")
        koik.append(i.split(" "))
    for i in koik:
        response = requests.get(i[1])
        img = Image.open(BytesIO(response.content))
        pilt=np.array(img)
        kooding=fr.face_encodings(pilt)[0]
        try:
            results = fr.compare_faces([kooding], kooding2)
        except:
            pass
        if results==[True]:
            lopp=i[0]
    f.close()
    if lopp=="":
        return "0"
    else:
        return lopp