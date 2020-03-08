"""Flask app for Cupcakes"""

from flask import Flask, request, render_template, redirect, flash, session, jsonify
from models import db, connect_db, Cupcake

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///cupcakedb'
app.config['SECRET_KEY'] = 'supersecret'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

connect_db(app)

@app.route('/')
def show_index():
    return 'hello'

@app.route('/api/cupcakes')
def get_all_cupcakes():
    data = Cupcake.query.all()
    cupcakes = [serialize_cupcake(c) for c in data]
    return jsonify(cupcakes=cupcakes)

@app.route('/api/cupcakes', methods=['POST'])
def create_cupcake():
    flavor = request.json['flavor']
    size = request.json['size']
    rating = request.json['rating']
    image = request.json['image']

    new_cupcake = Cupcake(flavor=flavor, size=size, rating=rating, image=image)
    db.session.add(new_cupcake)
    db.session.commit()

    serialized = serialize_cupcake(new_cupcake)
    return (jsonify(cupcake=serialized), 201)

@app.route('/api/cupcakes/<int:id>')
def get_single_cupcake(id):
    res = Cupcake.query.get_or_404(id)
    cupcake = serialize_cupcake(res)
    return jsonify(cupcake=cupcake)

def serialize_cupcake(cupcake):
    return {
        "id": cupcake.id,
        "flavor": cupcake.flavor,
        "size": cupcake.size,
        "rating": cupcake.rating,
        "image": cupcake.image,
    }
