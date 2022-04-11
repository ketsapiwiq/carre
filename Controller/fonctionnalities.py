from flask import Flask, render_template

app = Flask(__name__)

@app.route("/addPad", methods=['POST'])
def ajoutPad():
    print("Coucou ! ajout d'un pad")
    newPad = Pad()
    #return render_template('index.html')


@app.route("/")
def hello():
    return render_template('Vue/index.html', name = 'World')
app.run(debug = True)