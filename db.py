from flask import Flask, request, render_template
from tinydb import TinyDB
from datetime import datetime


app = Flask(__name__)
db = TinyDB('obiskovalci.json')


@app.route('/' , methods=['GET','POST']) 
def  index():   
    # Pridobi IP naslov obiskovalca
    ip = request.remote_addr  
    if request.headers.get('X-Forwarded-For'): 
        ip = request.headers.get('X-Forwarded-For').split(',')[0]
        
        print(f"Obisk z IP:{ip}")

    drzava = "Slovenia(test)"
    obisk = {
        'cas': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        'ip': ip,
        'drzava': drzava
    }
    db.insert(obisk)

    return render_template("index.html", ip=ip, stevilo_obiskov=len(db))


@app.route('/obiskovalci')
def seznam_obiskov():
    vsi = db.all()
    vsi = sorted(vsi, key=lambda x: x.get('cas', ''), reverse=True)
    return render_template("obiskovalci.html", obiski=vsi)


if __name__ == '__main__':
    app.run(debug=True)