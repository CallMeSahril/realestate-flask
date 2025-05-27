import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from scipy.sparse import hstack, csr_matrix
from config import SessionLocal
from models import Property

# Hitung jarak antar 2 titik koordinat (km)
def haversine_np(lat1, lon1, lat2, lon2):
    R = 6371  # Radius bumi dalam KM
    lat1 = np.radians(lat1)
    lat2 = np.radians(lat2)
    delta_lat = lat2 - lat1
    delta_lon = np.radians(lon2 - lon1)
    a = np.sin(delta_lat / 2)**2 + np.cos(lat1) * np.cos(lat2) * np.sin(delta_lon / 2)**2
    c = 2 * np.arcsin(np.sqrt(a))
    return R * c

def get_recommendations_by_profile(preferences, top_k=5):
    db = SessionLocal()
    try:
        all_properties = db.query(Property).all()
        if not all_properties:
            return []

        weights = preferences.get("weights", {
            "location": 1.0,
            "type": 1.0,
            "price": 1.0,
            "size": 1.0,
            "rooms": 1.0
        })

        df = pd.DataFrame([{
            'id': p.id,
            'title': p.title,
            'location': p.location,
            'price': p.price,
            'building_size': p.building_size,
            'num_rooms': p.num_rooms,
            'type': p.type,
            'latitude': p.latitude,
            'longitude': p.longitude
        } for p in all_properties])

        df['text_features'] = df['location'] + " " + df['type']
        vec = CountVectorizer()
        text_matrix = vec.fit_transform(df['text_features'])

        scaler = StandardScaler()
        numeric_matrix = scaler.fit_transform(df[['price', 'building_size', 'num_rooms']])

        text_matrix = text_matrix.multiply(weights['location'] + weights['type'])
        numeric_matrix[:, 0] *= weights['price']
        numeric_matrix[:, 1] *= weights['size']
        numeric_matrix[:, 2] *= weights['rooms']

        full_feature_matrix = hstack([text_matrix, numeric_matrix]).tocsr()

        user_text = preferences['preferred_location'] + " " + preferences['preferred_type']
        user_text_vec = vec.transform([user_text]).multiply(weights['location'] + weights['type'])

        user_numeric = np.array([[
            preferences['budget'],
            preferences['building_size'],
            preferences['num_rooms']
        ]])
        user_numeric_scaled = scaler.transform(user_numeric)
        user_numeric_scaled[:, 0] *= weights['price']
        user_numeric_scaled[:, 1] *= weights['size']
        user_numeric_scaled[:, 2] *= weights['rooms']

        user_profile_vector = hstack([user_text_vec, user_numeric_scaled])
        user_profile_vector = csr_matrix(user_profile_vector)

        similarities = cosine_similarity(user_profile_vector, full_feature_matrix).flatten()
        df['score'] = similarities

        if 'latitude' in preferences and 'longitude' in preferences:
            df['distance_km'] = haversine_np(preferences['latitude'], preferences['longitude'], df['latitude'], df['longitude'])
        else:
            df['distance_km'] = None

        df_filtered = df[df['score'] >= 0.4]
        df_sorted = df_filtered.sort_values(by=['score', 'distance_km'], ascending=[False, True])

        return df_sorted.head(top_k).to_dict(orient='records')
    finally:
        db.close()
