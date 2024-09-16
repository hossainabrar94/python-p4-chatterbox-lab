from flask import Flask, request, make_response, jsonify
from flask_cors import CORS
from flask_migrate import Migrate

from models import db, Message

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

CORS(app)
migrate = Migrate(app, db)

db.init_app(app)

@app.route('/messages', methods=['GET', 'POST'])
def messages():
    messages_list = [message.to_dict() for message in Message.query.order_by(Message.created_at).all()]
    if request.method == 'GET':
        return make_response(messages_list,200)
    elif request.method == 'POST':
        data = request.get_json()
        new_message = Message(
            body = data.get('body'),
            username = data.get('username')
        )
        db.session.add(new_message)
        db.session.commit()
        new_message_dict = new_message.to_dict()
        return make_response(new_message_dict, 201)

@app.route('/messages/<int:id>', methods = ['GET','PATCH', 'DELETE'])
def messages_by_id(id):
    message = Message.query.filter(Message.id == id).first()
    if request.method == 'GET':
        message_dict = message.to_dict()
        return make_response(message_dict, 200)
    elif request.method == 'PATCH':
        data = request.get_json()
        for attr in data:
            setattr(message, attr, data.get(attr))
        db.session.add(message)
        db.session.commit()

        message_dict = message.to_dict()
        return make_response(message_dict, 200)
    elif request.method == 'DELETE':
        db.session.delete(message)
        db.session.commit()

        return '', 204


if __name__ == '__main__':
    app.run(port=5555)
