from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-here'
app.config['SQLALCHEMY_DATABASE_URI'] ='sqlite:///komodohub.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class User(db.Model):
    Uid = db.Column(db.Integer, nullable=False, primary_key=True)
    email = db.Column(db.String(100), nullable=False, unique=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(100), nullable=False)
    acc_type = db.Column(db.String(20), nullable=False)

    def __repr__(self):
        return f"User('{self.Uid}','{self.first_name}', '{self.last_name}')"
class Organization(db.Model):
    Oid = db.Column(db.Integer, nullable=False, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    og_type = db.Column(db.String(20), nullable=False)

    def __repr__(self):
        return f"Organization('{self.Oid}','{self.name}')"

with app.app_context():
    if not os.path.exists('komodohub.db'):
        db.create_all()

@app.route("/")
def index():
    return f"<h1>{User.query.all()}</h1>"
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=2222, debug=True)

 