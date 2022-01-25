from flask import Blueprint, render_template, jsonify, request
from nft import Creator

manage = Blueprint('manage', __name__,url_prefix='/manage')

@manage.route('/')
def home():
    with Creator() as c:
        return render_template('layers.html')

@manage.route('/layers')
def layers():
    with Creator() as c:
        return jsonify(c.get_layers())

@manage.route('/upload', methods=['POST'])
def upload():
    with Creator() as c:
        return c.upload_layer(request.form,request.files)      

@manage.route('/delete', methods=['GET'])
def delete():
    with Creator() as c:
        return c.delete_layer(request.args)