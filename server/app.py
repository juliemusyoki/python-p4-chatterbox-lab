from flask import Flask, request, jsonify
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
    if request.method == 'GET':
        # Return all messages as JSON
        messages = Message.query.order_by(Message.created_at.asc()).all()
        return jsonify(messages), 200, {'Content-Type': 'application/json'}

    elif request.method == 'POST':
        # Create a new message
        data = request.get_json()
        new_message = Message(body=data['body'], username=data['username'])
        db.session.add(new_message)
        db.session.commit()
        return jsonify(new_message), 201, {'Content-Type': 'application/json'}

if __name__ == '__main__':
    app.run(port=5555)
