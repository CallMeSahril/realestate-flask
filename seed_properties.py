import pandas as pd
from config import SessionLocal
from models import Property

# Load data dari file CSV / DataFrame yang sudah dibuat
df = pd.read_csv("data_dummy_properti.csv")  # Pastikan file CSV ini ada di folder yang sama

def seed_properties():
    db = SessionLocal()
    try:
        for _, row in df.iterrows():
            prop = Property(
                title=row['title'],
                location=row['location'],
                price=row['price'],
                building_size=row['building_size'],
                num_rooms=row['num_rooms'],
                type=row['type'],
                latitude=row['latitude'],
                longitude=row['longitude']
            )
            db.add(prop)
        db.commit()
        print("✅ Data dummy properti berhasil disimpan ke database.")
    except Exception as e:
        db.rollback()
        print("❌ Gagal menyimpan data:", e)
    finally:
        db.close()

if __name__ == '__main__':
    seed_properties()
