from flask import Flask, render_template, request, jsonify
from recommender import get_recommendations_by_profile
from config import Base, engine, SessionLocal
from models import Property
from flask import redirect, url_for
import requests
from flask import jsonify
app = Flask(__name__, static_folder='static', template_folder='templates')
Base.metadata.create_all(bind=engine)

RAJAONGKIR_API_KEY = "mOunkhXO0f516aba4bc32212c8Naa3S4"


@app.route('/api/provinces')
def get_provinces():
    try:
        res = requests.get(
            "https://api.rajaongkir.com/starter/province",
            headers={"x-api-key": RAJAONGKIR_API_KEY}
        )
        data = res.json()

        # ✅ Tambahkan log dan validasi status
        if data["rajaongkir"]["status"]["code"] != 200:
            return jsonify({"error": data["rajaongkir"]["status"]["description"]}), 500

        results = [
            {"id": p["province_id"], "name": p["province"]}
            for p in data["rajaongkir"]["results"]
        ]
        return jsonify(results)
    except Exception as e:
        print("❌ Error get_provinces:", e)
        return jsonify({"error": str(e)}), 500


@app.route('/api/cities/<province_id>')
def get_cities(province_id):
    try:
        res = requests.get(
            f"https://api.rajaongkir.com/starter/city?province={province_id}",
            headers={"key": RAJAONGKIR_API_KEY}
        )
        data = res.json()
        results = [
            {
                "id": c["city_id"],
                "name": f"{c['type']} {c['city_name']}"
            }
            for c in data["rajaongkir"]["results"]
        ]
        return jsonify(results)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/dashboard-summary')
def dashboard_summary():
    db = SessionLocal()
    try:
        total_properties = db.query(Property).count()
        consultations_today = 6
        follow_ups_pending = 4
        latest_activities = [
            {"desc": "🏠 Properti baru ditambahkan di Bekasi", "time": "2 menit lalu"},
            {"desc": "📝 3 konsultasi diselesaikan hari ini", "time": "1 jam lalu"},
            {"desc": "📨 Preferensi pengguna terkirim (Rumah)",
             "time": "Kemarin"}
        ]
        properties = db.query(Property).all()

        properties_location = []
        for p in properties:
            if p.latitude and p.longitude:
                properties_location.append({
                    "id": p.id,
                    "title": p.title,
                    "location": p.location,
                    "type": p.type,
                    "price": p.price,
                    "building_size": p.building_size,
                    "num_rooms": p.num_rooms,
                    "fitur": p.fitur or "",
                    "gambar": p.gambar or "",
                    "lat": p.latitude,
                    "lng": p.longitude
                })

        return jsonify({
            "total_properties": total_properties,
            "consultations_today": consultations_today,
            "follow_ups_pending": follow_ups_pending,
            "latest_activities": latest_activities,
            "properties_location": properties_location
        })
    except Exception as e:
        print("❌ ERROR SERVER:", e)  # ini akan tampil di terminal
        return jsonify({"error": str(e)}), 500
    finally:
        db.close()


@app.route('/view/dashboard')
def view_dashboard():
    return render_template('views/dashboard.html')


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
            # ✅ string dari <select id="kota">
            location=data['location'],
            # ✅ string dari <select id="provinsi">
            province=data['province'],
            price=float(data['price']),
            building_size=int(data['building_size']),
            num_rooms=int(data['num_rooms']),
            type=data['type'],
            latitude=float(data['latitude']),
            longitude=float(data['longitude']),
            fitur=data.get('fitur', ''),
            gambar=data.get('gambar', '')
        )
        db.add(prop)
        db.commit()
        return redirect(url_for('load_properties'))
    except Exception as e:
        db.rollback()
        return f"❌ Error: {e}"
    finally:
        db.close()


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
