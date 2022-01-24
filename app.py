from flask import Flask,render_template,request,jsonify
from nft import Creator

app = Flask(__name__,template_folder='templates')

@app.route('/')
def hello():
    return render_template('index.html')

@app.route('/mint',methods=['POST'])
def mint():    
    with Creator() as creator:        
        return jsonify(creator.mint_nft(int(request.json["count"])))

if __name__ == '__main__':
    app.run(debug=True)
    