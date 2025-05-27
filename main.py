from flask import Flask, render_template, request, jsonify
from recommender import get_recommendations_by_profile
from config import Base, engine, SessionLocal
from models import Property

app = Flask(__name__, static_folder='static', template_folder='templates')
Base.metadata.create_all(bind=engine)
from flask import redirect, url_for

@app.route('/locations')
def get_locations():
    db = SessionLocal()
    try:
        result = db.query(Property.location).distinct().all()
        return jsonify([row[0] for row in result])  # <-- penting!
    finally:
        db.close()


@app.route('/add-property', methods=['POST'])
def add_property():
    data = request.form
    db = SessionLocal()
    try:
        prop = Property(
            title=data['title'],
            location=data['location'],
            type=data['type'],
            price=float(data['price']),
            building_size=int(data['building_size']),
            num_rooms=int(data['num_rooms']),
            latitude=float(data['latitude']),
            longitude=float(data['longitude'])
        )
        db.add(prop)
        db.commit()
    finally:
        db.close()
    return redirect(url_for('load_properties'))

@app.route('/delete-property/<int:prop_id>', methods=['DELETE'])
def delete_property(prop_id):
    db = SessionLocal()
    try:
        prop = db.query(Property).filter_by(id=prop_id).first()
        if prop:
            db.delete(prop)
            db.commit()
            return jsonify({"status": "deleted"})
        return jsonify({"status": "not found"}), 404
    finally:
        db.close()

@app.route('/')
def home():
    return render_template('index.html')
@app.route('/api/properties/count')
def get_property_count():
    db = SessionLocal()
    try:
        count = db.query(Property).count()
        return jsonify({"total": count})
    finally:
        db.close()

@app.route('/view/properties')
def load_properties():
    db = SessionLocal()
    try:
        properties = db.query(Property).all()
        return render_template('views/properties.html', properties=properties)
    finally:
        db.close()

@app.route('/view/<page>')
def load_view(page):
    if page == 'properties':
        return load_properties()
    return render_template(f'views/{page}.html')
@app.route('/view/recommendations')
def view_recommendations():
    return render_template("views/recommendations.html")


@app.route('/recommendations/by-profile', methods=['POST'])
def recommend():
    preferences = request.json
    result = get_recommendations_by_profile(preferences)
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)
