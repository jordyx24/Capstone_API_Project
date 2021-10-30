from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_cors import CORS, cross_origin
import os

app = Flask(__name__)


basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'app.sqlite')

db = SQLAlchemy(app)
ma = Marshmallow(app)

CORS(app, support_credentials=True)


class Guide(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=False)
    thoughs = db.Column(db.String, unique=False)

    def __init__(self, thoughs, name):
        self.name = name
        self.thoughs = thoughs
        

class GuideSchema(ma.Schema):
    class Meta:
        fields = ("name", "thoughs")

guide_schema = GuideSchema()
guides_schema = GuideSchema(many=True)


@app.route('/thoughs', methods=["POST"])
def add_guide():
    name = request.json['name']
    thoughs = request.json['thoughs']

    new_guide = Guide(name, thoughs)

    db.session.add(new_guide)
    db.session.commit()

    guide = Guide.query.get(new_guide.id)

    return guide_schema.jsonify(guide)

@app.route("/thoughs/get", methods=["GET"])
def get_thoughs():
    all_thoughs = Guide.query.all()
    result = guides_schema.dump(all_thoughs)

    return jsonify(result)






@app.route('/',methods=["GET"])
def home():
    return "Jordy's API"

if __name__ == '__main__':
    app.run(debug=True)