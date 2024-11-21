from models import db, Item, SpecialCategory, Review, User, Cart
from app import app
from datetime import datetime
from sqlalchemy import text
from sqlalchemy.exc import IntegrityError

# Set up and seed the database
with app.app_context():
    try:
        
        db.drop_all()  
        db.create_all()  
        # seed_data() 

    except Exception as e:
        print(f"An error occurred while setting up the database: {e}")
        db.session.rollback()

    #Delete associated relationships before seeding
    db.session.execute(text("DELETE FROM item_special_categories"))
    db.session.commit()
    
    db.session.execute(text("DELETE FROM reviews WHERE item_id IS NOT NULL"))
    db.session.commit()
    
    #Remove all rows from the tables
    Item.query.delete()
    SpecialCategory.query.delete()
    User.query.delete()
    Review.query.delete()
    db.session.commit()
    
    #Reset primary key sequences to start at 1
    db.session.execute(text("ALTER SEQUENCE items_id_seq RESTART WITH 1;"))
    db.session.execute(text("ALTER SEQUENCE special_categories_id_seq RESTART WITH 1;"))
    db.session.commit()


    print("Seeding users...")
        
    users = [
        User(username="AdminUser", email="admin@example.com", _password_hash = "adminpassword", role="admin"),
        User(username="RegularUser", email="user@example.com", _password_hash = "userpassword", role="user"),
        User(username="RegularUser1", email="user1@example.com", _password_hash = "userpassword1", role="user"),
        User(username="AdminUser2", email="admin2@example.com", _password_hash = "adminpassword", role="admin"),
        User(username="RegularUser3", email="user3@example.com", _password_hash = "userpassword", role="user")
    ]

    db.session.add_all(users)
    db.session.commit()

    print("Users seeded successfully!")
          
    print("Seeding items...")
    
    items = [
        Item(item_name= "Pixel 8 Pro", item_features={"feature1": "50MP main camera", "feature2": "Google Tensor G2 processor", "feature3": "120Hz display"}, item_price= 99900, item_prev_price= 100900, item_image_url= "images/Pixel 8 Pro.jpeg", item_category= "Smartphone", items_in_stock= 7),
        Item(item_name= "MacBook Pro 14-inch", item_features={"feature1": "M2 Pro/Max chip", "feature2": "Liquid Retina XDR display", "feature3": "MagSafe charging"}, item_price= 199900, item_prev_price= 211110, item_image_url= "images/MacBook Pro 14-inch.jpg", item_category= "Laptop", items_in_stock= 7),
        Item(item_name= "Apple iMac 27-inch", item_features={"feature1": "5K Retina display", "feature2": "1080p FaceTime HD camera", "feature3": "studio-quality mics"}, item_price= 179900, item_prev_price= 18900, item_image_url= "images/Apple iMac 27-inch.jpg", item_category= "Desktop", items_in_stock= 7),
        Item(item_name= "Sony WH-1000XM5", item_features={"feature1": "Adaptive Sound Control", "feature2": "Speak-to-Chat", "feature3": "HD Noise Cancelling Processor QN1"}, item_price= 39900, item_image_url= "images/Sony WH-1000XM5.jpg", item_category= "Headphones", items_in_stock= 7),
        Item(item_name= "Apple AirPods Pro (2nd Generation)", item_features={"feature1": "Adaptive Transparency", "feature2": "Personalized Spatial Audio", "feature3": "MagSafe Charging Case"}, item_price= 24900, item_prev_price= 31900, item_image_url= "images/Apple AirPods Pro (2nd Generation).jpeg", item_category= "Earbuds", items_in_stock= 7),
        Item(item_name= "LG C3 Series OLED TV", item_features={"feature1": "Self-Lit OLED", "feature2": "α9 Gen6 Processor 4K", "feature3": "4K, Dolby Vision IQ"}, item_price= 149900, item_prev_price= 195000, item_image_url= "images/LG C3 Series OLED TV.jpg", item_category= "TV", items_in_stock= 7),
        Item(item_name= "Bose Soundbar 700", item_features={"feature1": "Dolby Atmos", "feature2": "Bose Voice Assistant", "feature3": "Wi-Fi and Bluetooth Connectivity"}, item_price= 79900, item_prev_price= 10000, item_image_url= "images/Bose Soundbar 700.jpeg", item_category= "Sound system", items_in_stock= 7),
        Item(item_name= "KEF LS50 Meta", item_features={"feature1": "Uni-Core Driver", "feature2": "Concentric Driver", "feature3": "Titanium Dome Tweeter"}, item_price= 299900, item_prev_price= 1, item_image_url= "images/KEF LS50 Meta.jpg_30ac01", item_category= "Speakers", items_in_stock= 7),
        Item(item_name= "Apple Watch Series 9", item_features={"feature1": "Always-On Retina Display", "feature2": "Advanced Heart Rate Tracking", "feature3": "Crash Detection"}, item_price= 39900, item_prev_price= 1, item_image_url= "images/Apple Watch Series 9.jpg", item_category= "Smartwatch", items_in_stock= 7),
        Item(item_name= "Apple iPad Pro (12.9-inch)", item_features={"feature1": "Liquid Retina XDR Display", "feature2": "M2 Chip", "feature3": "LiDAR Scanner"}, item_price= 109900, item_prev_price= 119110, item_image_url= "images/Apple iPad Pro (12.9-inch).jpeg", item_category= "Tablet", items_in_stock= 7),
        Item(item_name= "iPhone 15 Pro Max", item_features={"feature1": "A17 Bionic chip", "feature2": "Dynamic Island, ProMotion display", "feature3": "Triple-camera system"}, item_price= 109900, item_prev_price= 129000, item_image_url= "images/iPhone 15 Pro Max.jpg", item_category= "Smartphone", items_in_stock= 7),
        Item(item_name= "Dell XPS 13 Plus", item_features={"feature1": "12th Gen Intel Core processor", "feature2": "OLED display", "feature3": "capacitive touch function keys"}, item_price= 149900, item_prev_price= 189900, item_image_url= "images/Dell XPS 13 Plus.jpg", item_category= "Laptop", items_in_stock= 7),
        Item(item_name= "Dell XPS Desktop", item_features={"feature1": "13th Gen Intel Core processor", "feature2": "NVIDIA GeForce RTX 40 series graphics", "feature3": "liquid cooling"}, item_price= 129900, item_prev_price= 199990, item_image_url= "images/Dell XPS Desktop.jpg", item_category= "Desktop", items_in_stock= 7),
        Item(item_name= "Bose QuietComfort 45", item_features={"feature1": "Active EQ", "feature2": "TriPort Acoustic Headphone Structure", "feature3": "Aware Mode"}, item_price= 32900, item_prev_price= 400000, item_image_url= "images/Bose QuietComfort 45.jpg", item_category= "Headphones", items_in_stock= 7),
        Item(item_name= "Sony WF-1000XM5", item_features={"feature1": "Integrated Processor V1", "feature2": "Dynamic Driver X", "feature3": "Adaptive Sound Control"}, item_price= 29900, item_prev_price= 39000, item_image_url= "images/Sony WF-1000XM5.jpg", item_category= "Earbuds", items_in_stock= 7),
        Item(item_name= "Samsung Neo QLED 8K TV", item_features={"feature1": "Neo Quantum Processor 8K", "feature2": "Quantum Matrix Technology", "feature3": "Real Depth Enhancer"}, item_price= 299900, item_prev_price= 320000, item_image_url= "images/Samsung Neo QLED 8K TV.jpeg", item_category= "TV", items_in_stock= 7),
        Item(item_name= "Klipsch Cinema 600", item_features={"feature1": "Reference Premiere Series Drivers", "feature2": "Tractrix Horn Technology", "feature3": "Wireless Subwoofer"}, item_price= 129900, item_image_url= "images/Klipsch Cinema 600.jpg", item_category= "Sound system", items_in_stock= 7),
        Item(item_name= "Focal Kanta No.2", item_features={"feature1": "Beryllium Tweeter", "feature2": "Flax Cone Midrange Driver", "feature3": "Slatefiber Cone Bass Driver"}, item_price= 1299900, item_prev_price= 2110000, item_image_url= "images/Focal Kanta No.2", item_category= "Speakers", items_in_stock= 7),
        Item(item_name= "Samsung Galaxy Watch 6 Classic", item_features={"feature1": "Super AMOLED Display", "feature2": "Advanced Sleep Tracking", "feature3": "Blood Pressure Monitoring"}, item_price= 34900, item_prev_price= 610000, item_image_url= "images/Samsung Galaxy Watch 6 Classic.jpg", item_category= "Smartwatch", items_in_stock= 7),
        Item(item_name= "Samsung Galaxy Tab S9 Ultra", item_features={"feature1": "Dynamic AMOLED 2X Display", "feature2": "Snapdragon 8 Gen 2", "feature3": "S Pen"}, item_price= 119900, item_prev_price= 3210000, item_image_url= "images/Samsung Galaxy Tab S9 Ultra.jpg", item_category= "Tablet", items_in_stock= 7),
        Item(item_name= "Samsung Galaxy S24 Ultra", item_features={"feature1": "200MP main camera", "feature2": "108MP ultrawide camera", "feature3": "Snapdragon 8 Gen 3 processor, 120Hz display"}, item_price= 119900, item_image_url= "images/Samsung Galaxy S24 Ultra.jpg", item_category= "Smartphone", items_in_stock= 7),
        Item(item_name= "HP Spectre x360", item_features={"feature1": "12th Gen Intel Core processor", "feature2": "OLED display", "feature3": "360-degree hinge"}, item_price= 139900, item_image_url= "images/HP Spectre x360.png", item_category= "Laptop", items_in_stock= 7),
        Item(item_name= "Lenovo Legion Tower 7i", item_features={"feature1": "13th Gen Intel Core processor", "feature2": "NVIDIA GeForce RTX 40 series graphics", "feature3": "7.1 channel surround sound"}, item_price= 199900, item_image_url= "images/Lenovo Legion Tower 7i.jpg", item_category= "Desktop", items_in_stock= 7),
        Item(item_name= "Apple AirPods Max", item_features={"feature1": "Adaptive EQ", "feature2": "Spatial Audio with Dynamic Head Tracking", "feature3": "Active Noise Cancellation"}, item_price= 54900, item_image_url= "images/Apple AirPods Max.jpg", item_category= "Headphones", items_in_stock= 7),
        Item(item_name= "Bose QuietComfort Earbuds II", item_features={"feature1": "CustomTune Sound Calibration", "feature2": "Active Noise Cancellation", "feature3": "Aware Mode"}, item_price= 29900, item_prev_price= 10000, item_image_url= "images/Bose QuietComfort Earbuds II.jpg", item_category= "Earbuds", items_in_stock= 7),
        Item(item_name= "Sony BRAVIA XR A95K OLED TV", item_features={"feature1": "Cognitive Processor XR", "feature2": "Perfect Contrast Booster", "feature3": "Acoustic Surface Audio+"}, item_price= 249900, item_prev_price= 10000, item_image_url= "images/Sony BRAVIA XR A95K OLED TV.jpg", item_category= "TV", items_in_stock= 7),
        Item(item_name= "Sennheiser AMBEO Soundbar", item_features={"feature1": "7 Drivers", "feature2": "Up-Firing Speakers", "feature3": "Dolby Atmos"}, item_price= 249900, item_prev_price= 10000, item_image_url= "images/Sennheiser AMBEO Soundbar.jpg", item_category= "Sound system", items_in_stock= 7),
        Item(item_name= "Klipsch RP-8000F", item_features={"feature1": "Tractrix Horn-Loaded Compression Driver", "feature2": "Cerametallic Woofer", "feature3": "Powerful Bass Response"}, item_price= 199900, item_image_url= "images/Klipsch RP-8000F1.jpeg", item_category= "Speakers", items_in_stock= 7),
        Item(item_name= "Fitbit Sense 2", item_features={"feature1": "ECG App", "feature2": "Skin Temperature Sensor", "feature3": "Stress Management Score"}, item_price= 29900, item_image_url= "images/Fitbit Sense 2.jpg", item_category= "Smartwatch", items_in_stock= 7),
        Item(item_name= "Microsoft Surface Pro 9", item_features={"feature1": "PixelSense Flow Display", "feature2": "12th Gen Intel Core Processor", "feature3": "Slim Pen 2"}, item_price= 99900, item_image_url= "images/Microsoft Surface Pro 9.jpg", item_category= "Tablet", items_in_stock= 7),
        Item(item_name= "OnePlus 12", item_features={"feature1": "Snapdragon 8 Gen 3 processor", "feature2": "120Hz display", "feature3": "Hasselblad camera system"}, item_price= 79900, item_image_url= "images/OnePlus 12.jpg", item_category= "Smartphone", items_in_stock= 7),
        Item(item_name= "Acer Swift X", item_features={"feature1": "12th Gen Intel Core processor", "feature2": "OLED display", "feature3": "long battery life"}, item_price= 99900, item_prev_price= 10000, item_image_url= "images/Acer Swift X.jpg", item_category= "Laptop", items_in_stock= 7),
        Item(item_name= "HP Omen 45L", item_features={"feature1": "13th Gen Intel Core processor", "feature2": "NVIDIA GeForce RTX 40 series graphics", "feature3": "OMEN Lighting Sync"}, item_price= 169900, item_prev_price= 10000, item_image_url= "images/HP Omen 45L.jpg", item_category= "Desktop", items_in_stock= 7),
        Item(item_name= "Hisense U8H ULED TV", item_features={"feature1": "ULED", "feature2": "Quantum Dot Color", "feature3": "Dolby Vision HDR"}, item_price= 79900, item_prev_price= 10000, item_image_url= "images/Hisense U8H ULED TV.jpg", item_category= "TV", items_in_stock= 7),
        Item(item_name= "Sennheiser Momentum 4 Wireless", item_features={"feature1": "Adaptive Noise Cancellation", "feature2": "Transparent Hearing", "feature3": "Sound Personalization"}, item_price= 34900, item_prev_price= 10000, item_image_url= "images/Sennheiser Momentum 4 Wireless.jpg", item_category= "Headphones", items_in_stock= 7),
        Item(item_name= "Sennheiser Momentum True Wireless 3", item_features={"feature1": "Adaptive Noise Cancellation", "feature2": "Transparent Hearing", "feature3": "Adaptive Sound"}, item_price= 29900, item_prev_price= 10000, item_image_url= "images/Sennheiser Momentum True Wireless 3.jpg", item_category= "Earbuds", items_in_stock= 7),
        Item(item_name= "LG SN11RG", item_features={"feature1": "AI Sound Pro", "feature2": "Meridian Audio", "feature3": "Wireless Rear Speakers"}, item_price= 199900, item_prev_price= 10000, item_image_url= "images/LG SN11RG.jpg", item_category= "Sound system", items_in_stock= 7),
        Item(item_name= "Klipsch RP-600M", item_features={"feature1": "Tractrix Horn-Loaded Compression Driver", "feature2": "Cerametallic Woofer", "feature3": "Powerful Bass Response"}, item_price= 199900, item_prev_price= 10000, item_image_url= "images/Klipsch RP-8000F1.jpeg", item_category= "Speakers", items_in_stock= 7),
        Item(item_name= "Garmin Venu 2 Plus", item_features={"feature1": "AMOLED Display", "feature2": "Advanced Workout Tracking", "feature3": "Health Snapshot"}, item_price= 44900, item_prev_price= 10000, item_image_url= "images/Garmin Venu 2 Plus.jpeg", item_category= "Smartwatch", items_in_stock= 7),
        Item(item_name= "Amazon Fire HD 10 Plus", item_features={"feature1": "10.1-inch HD Display", "feature2": "Octa-Core Processor", "feature3": "Alexa Built-In"}, item_price= 19900, item_prev_price= 10000, item_image_url= "images/Amazon Fire HD 10 Plus.jpg", item_category= "Tablet", items_in_stock= 7),
        Item(item_name= "Xiaomi 14 Pro", item_features={"feature1": "Snapdragon 8 Gen 3 processor", "feature2": "120Hz display", "feature3": "Leica camera system"}, item_price= 89900, item_prev_price= 10000, item_image_url= "images/Xiaomi 14 Pro.jpeg", item_category= "Smartphone", items_in_stock= 7),
        Item(item_name= "Asus Zenbook 14X OLED", item_features={"feature1": "12th Gen Intel Core processor", "feature2": "OLED display", "feature3": "ASUS NumberPad 2.0"}, item_price= 129900, item_prev_price= 10000, item_image_url= "images/Asus Zenbook 14X OLED.png", item_category= "Laptop", items_in_stock= 7),
        Item(item_name= "ASUS ROG Strix G35CX", item_features={"feature1": "13th Gen Intel Core processor", "feature2": "NVIDIA GeForce RTX 40 series graphics", "feature3": "Aura Sync RGB lighting"}, item_price= 169900, item_prev_price= 10000, item_image_url= "images/ASUS ROG Strix G35CX.jpg", item_category= "Desktop", items_in_stock= 7),
        Item(item_name= "AKG N900NC M2", item_features={"feature1": "Active Noise Cancellation", "feature2": "3D Audio", "feature3": "Long Battery Life"}, item_price= 39900, item_prev_price= 10000, item_image_url= "images/AKG N900NC M2.jpg", item_category= "Headphones", items_in_stock= 7),
        Item(item_name= "Jabra Elite 85t", item_features={"feature1": "Advanced Active Noise Cancellation", "feature2": "Multi-Point Connection", "feature3": "HearThrough"}, item_price= 22900, item_prev_price= 10000, item_image_url= "images/Jabra Elite 85t.jpg", item_category= "Earbuds", items_in_stock= 7),
        Item(item_name= "Panasonic JZ2000 OLED TV", item_features={"feature1": "OLED Master Panel", "feature2": "HCX Processor Pro", "feature3": "Dolby Atmos"}, item_price= 349900, item_prev_price= 10000, item_image_url= "images/Panasonic JZ2000 OLED TV.jpeg", item_category= "TV", items_in_stock= 7),
        Item(item_name= "JBL Bar 500", item_features={"feature1": "MultiBeam", "feature2": "JBL Bass Boost", "feature3": "Wi-Fi and Bluetooth Connectivity"}, item_price= 49900, item_prev_price= 10000, item_image_url= "images/JBL Bar 500.jpg", item_category= "Sound system", items_in_stock= 7),
        Item(item_name= "Elac Debut 2.0 F5.2", item_features={"feature1": "AS-XR Ribbon Tweeter", "feature2": "Aluminum-Cone Woofer", "feature3": "Bass Reflex Design"}, item_price= 49900, item_prev_price= 10000, item_image_url= "images/Elac Debut 2.0 F5.2", item_category= "Speakers", items_in_stock= 7),
        Item(item_name= "Huawei Watch GT 3 Pro", item_features={"feature1": "AMOLED Display", "feature2": "ECG and Blood Oxygen Monitoring", "feature3": "Temperature Sensing"}, item_price= 39900, item_prev_price= 10000, item_image_url= "images/Huawei Watch GT 3 Pro.jpg", item_category= "Smartwatch", items_in_stock= 7),
        Item(item_name= "Lenovo Tab P11 Pro (Gen 2)", item_features={"feature1": "OLED Display", "feature2": "MediaTek Kompanio 1300T", "feature3": "Dolby Atmos"}, item_price= 49900, item_prev_price= 10000, item_image_url= "images/Lenovo Tab P11 Pro (Gen 2).jpeg", item_category= "Tablet", items_in_stock= 7),
        Item(item_name= "Google Pixel Fold", item_features={"feature1": "Google Tensor G2 processor", "feature2": "120Hz display", "feature3": "foldable design"}, item_price= 179900, item_prev_price= 10000, item_image_url= "images/Google Pixel Fold.jpeg", item_category= "Smartphone", items_in_stock= 7),
        Item(item_name= "Microsoft Surface Laptop 5", item_features={"feature1": "12th Gen Intel Core processor", "feature2": "PixelSense Flow display", "feature3": "Dolby Atmos sound system"}, item_price= 119900, item_prev_price= 10000, item_image_url= "images/Microsoft Surface Laptop 5.png", item_category= "Laptop", items_in_stock= 7),
        Item(item_name= "CyberPowerPC Gamer Xtreme VR", item_features={"feature1": "13th Gen Intel Core processor", "feature2": "NVIDIA GeForce RTX 40 series graphics", "feature3": "VR-ready"}, item_price= 189900, item_prev_price= 10000, item_image_url= "images/CyberPowerPC Gamer Xtreme VR.jpg", item_category= "Desktop", items_in_stock= 7),
        Item(item_name= "Shure SRH1540", item_features={"feature1": "Neodymium Drivers", "feature2": "Closed-Back Design", "feature3": "High Sensitivity"}, item_price= 49900, item_prev_price= 10000, item_image_url= "images/Shure SRH1540.jpg", item_category= "Headphones", items_in_stock= 7),
        Item(item_name= "AKG N400BT", item_features={"feature1": "Bluetooth 5.0", "feature2": "40mm Drivers", "feature3": "Long Battery Life"}, item_price= 16900, item_prev_price= 10000, item_image_url= "images/AKG N400BT.jpg", item_category= "Earbuds", items_in_stock= 7),
        Item(item_name= "Philips OLED+937 TV", item_features={"feature1": "OLED Display", "feature2": "P5 Perfect Picture Processor", "feature3": "Ambilight"}, item_price= 289900, item_prev_price= 10000, item_image_url= "images/Philips OLED+937 TV.jpeg", item_category= "TV", items_in_stock= 7),
        Item(item_name= "Beyerdynamic DT 1990 Pro", item_features={"feature1": "Tesla Technology", "feature2": "Open-Back Design", "feature3": "High-Resolution Audio"}, item_price= 59900, item_prev_price= 10000, item_image_url= "images/Beyerdynamic DT 1990 Pro.jpg", item_category= "Speakers", items_in_stock= 7),
        Item(item_name= "Xiaomi Watch S2 Pro", item_features={"feature1": "AMOLED Display", "feature2": "Heart Rate and Blood Oxygen Monitoring", "feature3": "GPS"}, item_price= 24900, item_image_url= "images/Xiaomi Watch S2 Pro.jpg", item_category= "Smartwatch", items_in_stock= 7),
        Item(item_name= "Huawei MatePad Pro 12.6", item_features={"feature1": "OLED Display", "feature2": "Snapdragon 888", "feature3": "HarmonyOS"}, item_price= 79900, item_image_url= "images/Huawei MatePad Pro 12.6.jpg", item_category= "Tablet", items_in_stock= 7),
        Item(item_name= "Motorola Edge 40 Pro", item_features={"feature1": "Snapdragon 8 Gen 2 processor", "feature2": "165Hz display", "feature3": "200MP main camera"}, item_price= 69900, item_image_url= "images/Motorola Edge 40 Pro.jpg", item_category= "Smartphone", items_in_stock= 7),
        Item(item_name= "Lenovo Legion Slim 7", item_features={"feature1": "13th Gen Intel Core processor", "feature2": "RTX 4070 Laptop GPU", "feature3": "165Hz display"}, item_price= 249900, item_image_url= "images/Lenovo Legion Slim 7.jpg", item_category= "Laptop", items_in_stock= 7),
        Item(item_name= "iBUYPOWER Slate MR", item_features={"feature1": "12th Gen Intel Core processor", "feature2": "NVIDIA GeForce RTX 30 series graphics", "feature3": "RGB lighting"}, item_price= 99900, item_image_url= "images/iBUYPOWER Slate MR.jpg", item_category= "Desktop", items_in_stock= 7),
        Item(item_name= "Philips Fidelio X2HR", item_features={"feature1": "50mm Drivers", "feature2": "Open-Back Design", "feature3": "High-Resolution Audio"}, item_price= 49900, item_prev_price= 10000, item_image_url= "images/Philips Fidelio X2HR.jpg", item_category= "Headphones", items_in_stock= 7),
        Item(item_name= "Beyerdynamic Lagoon ANC", item_features={"feature1": "Active Noise Cancellation", "feature2": "Transparent Hearing", "feature3": "Customizable EQ"}, item_price= 24900, item_prev_price= 10000, item_image_url= "images/Beyerdynamic Lagoon ANC.jpg", item_category= "Earbuds", items_in_stock= 7),
        Item(item_name= "LG QNED Mini LED TV", item_features={"feature1": "Mini-LED Backlight", "feature2": "Quantum Dot Color", "feature3": "α7 Gen5 AI Processor 4K"}, item_price= 129900, item_image_url= "images/LG QNED Mini LED TV.jpg", item_category= "TV", items_in_stock= 7),
        Item(item_name= "Amazfit GTR 4", item_features={"feature1": "AMOLED Display", "feature2": "Blood Oxygen Monitoring", "feature3": "Stress Monitoring"}, item_price= 18900, item_image_url= "images/Amazfit GTR 4.jpg", item_category= "Smartwatch", items_in_stock= 7),
        Item(item_name= "Xiaomi Pad 6", item_features={"feature1": "11-inch LCD Display", "feature2": "Snapdragon 870", "feature3": "Dolby Atmos"}, item_price= 39900, item_image_url= "images/Xiaomi Pad 6.jpg", item_category= "Tablet", items_in_stock= 7),
        Item(item_name= "Vivo X90 Pro+", item_features={"feature1": "1-inch sensor main camera", "feature2": "Zeiss optics", "feature3": "Snapdragon 8 Gen 2 processor"}, item_price= 99900, item_image_url= "images/Vivo X90 Pro+.jpg", item_category= "Smartphone", items_in_stock= 7),
        Item(item_name= "Polar Vantage V2", item_features={"feature1": "GPS", "feature2": "Heart Rate and Power Tracking", "feature3": "Recovery Insights"}, item_price= 49900, item_image_url= "images/Polar Vantage V2.jpg", item_category= "Smartwatch", items_in_stock= 7),
        Item(item_name= "iPad Air (5th generation)", item_features={"feature1": "Liquid Retina Display", "feature2": "M1 Chip", "feature3": "Center Stage"}, item_price= 59900, item_prev_price= 10000, item_image_url= "images/iPad Air (5th generation).jpg", item_category= "Tablet", items_in_stock= 7),
        Item(item_name= "OPPO Find X6 Pro", item_features={"feature1": "MariSilicon X imaging NPU", "feature2": "50MP ultrawide camera", "feature3": "Snapdragon 8 Gen 2 processor"}, item_price= 109900, item_prev_price= 10000, item_image_url= "images/OPPO Find X6 Pro.jpg", item_category= "Smartphone", items_in_stock= 7),
        Item(item_name= "Suunto 9 Peak Pro", item_features={"feature1": "GPS", "feature2": "Barometer", "feature3": "Altimeter"}, item_price= 54900, item_prev_price= 10000, item_image_url= "images/Suunto 9 Peak Pro.jpeg", item_category= "Smartwatch", items_in_stock= 7),
        Item(item_name= "Samsung Galaxy Tab S8", item_features={"feature1": "Super AMOLED Display", "feature2": "Snapdragon 8 Gen 1", "feature3": "S Pen"}, item_price= 79900, item_prev_price= 10000, item_image_url= "images/Samsung Galaxy Tab S8.jpg", item_category= "Tablet", items_in_stock= 7),
        Item(item_name= "Redmi Note 13 Pro Plus", item_features={"feature1": "Dimensity 9200 processor", "feature2": "108MP main camera", "feature3": "fast charging"}, item_price= 39900, item_prev_price= 10000, item_image_url= "images/Redmi Note 13 Pro Plus.jpg", item_category= "Smartphone", items_in_stock= 7),
        Item(item_name= "Withings ScanWatch", item_features={"feature1": "Mechanical and Digital Display", "feature2": "ECG and PPG Sensors", "feature3": "Sleep Tracking"}, item_price= 28900, item_prev_price= 10000, item_image_url= "images/Withings ScanWatch.jpg", item_category= "Smartwatch", items_in_stock= 7),
        Item(item_name= "Lenovo Yoga Tab 13", item_features={"feature1": "OLED Display", "feature2": "Snapdragon 870", "feature3": "JBL Speakers"}, item_price=67900, item_prev_price= 1, item_image_url= "images/Lenovo Yoga Tab 13.jpeg", item_category= "Tablet", items_in_stock= 7)
    ]

    db.session.add_all(items)
    db.session.commit()

    print("Items seeded successfully!")

    
    cart_items = [
        Cart(user_id=1, item_id=1, quantity=2),  
        Cart(user_id=2, item_id=2, quantity=1)   
    ]
    db.session.add_all(cart_items)
    db.session.commit()
        
    
    
    print("Seeding special categories...")
    
    special_categories = [
        SpecialCategory(name= "daily_deals"),
        SpecialCategory(name= "best_sellers"),
        SpecialCategory(name= "season_offers"),
        SpecialCategory(name= "hot_&_new")
    ]
    
    db.session.add_all(special_categories)
    
    db.session.commit()
    
    print("Special categories seeded successfully!")
    
    print("Adding items to special categories...")
    
    daily_deals_special_category = SpecialCategory.query.filter_by(name = "daily_deals").first()
    best_seller_special_category = SpecialCategory.query.filter_by(name = "best_sellers").first()
    hot_new_special_category = SpecialCategory.query.filter_by(name = "hot_&_new").first()
    season_offers_special_category = SpecialCategory.query.filter_by(name = "season_offers").first()
    
    daily_deals_items = [
        Item.query.filter(Item.item_name == "Apple iPad Pro (12.9-inch)").first(),
        Item.query.filter(Item.item_name == "Sony WH-1000XM5").first(),
        Item.query.filter(Item.item_name == "Pixel 8 Pro").first(),
        Item.query.filter(Item.item_name == "Withings ScanWatch").first(),
        Item.query.filter(Item.item_name == "Wireless Bluetooth Earbuds").first(),
        Item.query.filter(Item.item_name == "Sennheiser Momentum True Wireless 3").first(),
        Item.query.filter(Item.item_name == "Xiaomi 14 Pro").first(),
        Item.query.filter(Item.item_name == "Apple Watch Series 9").first(),
        Item.query.filter(Item.item_name == "Smartwatch with Fitness Tracker").first(),
        Item.query.filter(Item.item_name == "Samsung Galaxy Tab S9 Ultra").first(),
        Item.query.filter(Item.item_name == "Klipsch RP-8000F").first(),
        Item.query.filter(Item.item_name == "Smartwatch with Fitness Tracker").first(),
        Item.query.filter(Item.item_name == "Samsung Galaxy Tab S8").first()
    ]
    
    best_seller_items = [
        Item.query.filter(Item.item_name == "iPhone 15 Pro Max").first(),
        Item.query.filter(Item.item_name == "Apple AirPods Pro (2nd Generation)").first(),
        Item.query.filter(Item.item_name == "Sony WF-1000XM5").first(),
        Item.query.filter(Item.item_name == "Fitbit Sense 2").first(),
        Item.query.filter(Item.item_name == "Apple AirPods Max").first(),
        Item.query.filter(Item.item_name == "Microsoft Surface Pro 9").first(),
        Item.query.filter(Item.item_name == "Klipsch RP-8000F").first(),
        Item.query.filter(Item.item_name == "Modern Geometric Wall Art").first(),
        Item.query.filter(Item.item_name == "Hisense U8H ULED TV").first(),
        Item.query.filter(Item.item_name == "KEF LS50 Meta").first(),
        Item.query.filter(Item.item_name == "Sennheiser AMBEO Soundbar").first(),
        Item.query.filter(Item.item_name == "Dell XPS 13 Plus").first(),
        Item.query.filter(Item.item_name == "Samsung Neo QLED 8K TV").first()
    ]
    
    hot_new_items = [
        Item.query.filter(Item.item_name == "OnePlus 12").first(),
        Item.query.filter(Item.item_name == "Lenovo Tab P11 Pro (Gen 2)").first(),
        Item.query.filter(Item.item_name == "Acer Swift X").first(),
        Item.query.filter(Item.item_name == "Huawei Watch GT 3 Pro").first(),
        Item.query.filter(Item.item_name == "HP Omen 45L").first(),
        Item.query.filter(Item.item_name == "CyberPowerPC Gamer Xtreme VR").first(),
        Item.query.filter(Item.item_name == "Redmi Note 13 Pro Plus").first(),
        Item.query.filter(Item.item_name == "Amazfit GTR 4").first(),
        Item.query.filter(Item.item_name == "Xiaomi Pad 6").first(),
        Item.query.filter(Item.item_name == "JBL Bar 500").first(),
        Item.query.filter(Item.item_name == "Panasonic JZ2000 OLED TV").first(),
        Item.query.filter(Item.item_name == "Microsoft Surface Laptop 5").first(),
        Item.query.filter(Item.item_name == "Samsung Galaxy Watch 6 Classic").first()
    ]
    
    season_offers_items = [
        Item.query.filter(Item.item_name == "Dell XPS Desktop").first(),
        Item.query.filter(Item.item_name == "Elac Debut 2.0 F5.2").first(),
        Item.query.filter(Item.item_name == "Samsung Galaxy Tab S8").first(),
        Item.query.filter(Item.item_name == "Beyerdynamic Lagoon ANC").first(),
        Item.query.filter(Item.item_name == "Suunto 9 Peak Pro").first(),
        Item.query.filter(Item.item_name == "Lenovo Legion Slim 7").first(),
        Item.query.filter(Item.item_name == "Philips OLED+937 TV").first(),
        Item.query.filter(Item.item_name == "Huawei MatePad Pro 12.6").first(),
        Item.query.filter(Item.item_name == "Bose QuietComfort Earbuds II").first(),
        Item.query.filter(Item.item_name == "Google Pixel Fold").first(),
        Item.query.filter(Item.item_name == "AKG N400BT").first(),
        Item.query.filter(Item.item_name == "Xiaomi Watch S2 Pro").first(),
        Item.query.filter(Item.item_name == "Motorola Edge 40 Pro").first()
    ]
    
    for item in daily_deals_items:
        if item and daily_deals_special_category not in item.special_categories:
            daily_deals_special_category.items.append(item)
            
            
    for item in best_seller_items:
        if item and best_seller_special_category not in item.special_categories:
            best_seller_special_category.items.append(item)
            
            
    for item in hot_new_items:
        if item and hot_new_special_category not in item.special_categories:
            hot_new_special_category.items.append(item)
            
    for item in season_offers_items:
        if item and season_offers_special_category not in item.special_categories:
            season_offers_special_category.items.append(item)
    
    print("Special categories items added successfully!")
    
    db.session.commit()
    
    
    print("Seeding item reviews...")
    reviews = [
        Review(rating = 1, review_message = "The item is amazing.", item_id = 1, user_id = 1),
        Review(rating=4, review_message="This item exceeded my expectations!", item_id=23, user_id=3),
        Review(rating=2, review_message="Not impressed, could be better.", item_id=56, user_id=2),
        Review(rating=5, review_message="Absolutely love it! Highly recommend.", item_id=12, user_id=1),
        Review(rating=3, review_message="Decent item, but not amazing.", item_id=45, user_id=4),
        Review(rating=1, review_message="Very disappointed with this purchase.", item_id=72, user_id=5),
        Review(rating=4, review_message="Good value for the price.", item_id=34, user_id=3),
        Review(rating=5, review_message="Best item I've bought in a long time!", item_id=17, user_id=2),
        Review(rating=2, review_message="Not worth the money, unfortunately.", item_id=68, user_id=1),
        Review(rating=3, review_message="Okay item, could use some improvement.", item_id=5, user_id=4),
        Review(rating=4, review_message="Satisfied with my purchase.", item_id=29, user_id=5),
        Review(rating=1, review_message="Terrible item, do not buy!", item_id=76, user_id=3),
        Review(rating=5, review_message="Amazing quality, highly recommend!", item_id=10, user_id=2),
        Review(rating=3, review_message="Mixed feelings about this item.", item_id=42, user_id=1),
        Review(rating=4, review_message="Good overall, but could be better.", item_id=61, user_id=4),
        Review(rating=5, review_message="Absolutely love it! Highly recommend.", item_id=1, user_id=3),
        Review(rating=5, review_message="Love it! Perfect for what I needed.", item_id=2, user_id=5),
        Review(rating=2, review_message="Disappointed with the performance.", item_id=58, user_id=3),
        Review(rating=4, review_message="Solid item, would buy again.", item_id=15, user_id=2),
        Review(rating=1, review_message="Waste of money, do not recommend.", item_id=70, user_id=1),
        Review(rating=3, review_message="Okay item, nothing special.", item_id=37, user_id=4),
        Review(rating=4, review_message="Happy with my purchase, good value.", item_id=8, user_id=5),
        Review(rating=3, review_message="Decent item, could be better.", item_id=5, user_id=2),
        Review(rating=5, review_message="Amazing quality, highly recommend!", item_id=10, user_id=3),
        Review(rating=1, review_message="Very disappointed with this purchase.", item_id=72, user_id=4),
        Review(rating=4, review_message="Good value for the price.", item_id=34, user_id=1),
        Review(rating=2, review_message="Not impressed, could be better.", item_id=56, user_id=5),
        Review(rating=3, review_message="Okay item, could use some improvement.", item_id=5, user_id=3),
        Review(rating=4, review_message="Satisfied with my purchase.", item_id=29, user_id=2),
        Review(rating=1, review_message="Terrible item, do not buy!", item_id=76, user_id=1),
        Review(rating=5, review_message="Best item I've bought in a long time!", item_id=17, user_id=4),
        Review(rating=2, review_message="Not worth the money, unfortunately.", item_id=68, user_id=5),
        Review(rating=4, review_message="Good overall, but could be better.", item_id=61, user_id=3),
        Review(rating=1, review_message="Waste of money, do not recommend.", item_id=70, user_id=2),
        Review(rating=5, review_message="Absolutely love it! Highly recommend.", item_id=12, user_id=1),
        Review(rating=3, review_message="Mixed feelings about this item.", item_id=42, user_id=4),
        Review(rating=2, review_message="Not impressed, could be better.", item_id=1, user_id=4),
        Review(rating=2, review_message="Disappointed with the performance.", item_id=58, user_id=5),
        Review(rating=4, review_message="This item exceeded my expectations!", item_id=23, user_id=3),
        Review(rating=1, review_message="Very disappointed with this purchase.", item_id=72, user_id=2),
        Review(rating=5, review_message="Amazing quality, highly recommend!", item_id=10, user_id=1),
        Review(rating=3, review_message="Decent item, but not amazing.", item_id=45, user_id=4),
        Review(rating=4, review_message="Good value for the price.", item_id=1, user_id=5),
        Review(rating=4, review_message="Good value for the price.", item_id=1, user_id=1),
        Review(rating=2, review_message="Not impressed, could be better.", item_id=1, user_id=5),
        Review(rating=3, review_message="Okay item, could use some improvement.", item_id=5, user_id=3),
        Review(rating=4, review_message="Satisfied with my purchase.", item_id=29, user_id=2),
    ]
    
    db.session.add_all(reviews)
    
    print("Items reviews seeded successfully!")
    
    # Commit to save the items
    db.session.commit()

    print("Database seeded successfully!")
    
    
    









#         def create_items(admin_user):
# #     """Create electronics items associated with the admin user."""
# #     items = [
# #         item(
# #             name="Laptop", 
# #             description="A powerful laptop for professionals.", 
# #             price=1099, 
# #             item_availability=50, 
# #             user_id=admin_user.id  
# #         ),
# #         item(
# #             name="Smartphone", 
# #             description="A high-end smartphone with all the latest features.", 
# #             price=899, 
# #             item_availability=100, 
# #             user_id=admin_user.id
# #         ),
# #         item(
# #             name="Headphones", 
# #             description="Noise-canceling headphones for an immersive experience.", 
# #             price=199, 
# #             item_availability=75, 
# #             user_id=admin_user.id
# #         )
# #     ]
# #     return items


# print("Seeding users...")
    
#     # users = [
#     #     User(id=1, username= "User 1", role = 'Admin'),
#     #     User(id=2, username= "User 2"),
#     #     User(id=3, username= "User 3", role = 'Admin'),
#     #     User(id=4, username= "User 4"),
#     #     User(id=5, username= "User 5", role = 'Admin')
#     # ]
    
#     # db.session.add_all(users)
#     # db.session.commit()
    
#     # print("Users seeded successfully!")

# def create_users():
#     """Create and return admin and regular users."""
#     admin_user =   

#     regular_user =   

#     regular_user1 = 

#     admin_user2 =   

#     regular_user3 =  


#     return admin_user, regular_user, regular_user1, admin_user2, regular_user3

# def seed_data():
#     """Seed the database with sample data."""
#     try:
        
#         admin_user, regular_user, regular_user1 = create_users()
#         db.session.add(admin_user)
#         db.session.add_all([regular_user, regular_user1])

        
#         db.session.commit()

#         print("seed data message")
#         items = create_users(admin_user)
#         db.session.add_all(items)
#         db.session.commit()

        
#         add_cart_items_for_user(regular_user, items)  
#         add_cart_items_for_user(regular_user1, items)  

        
#         db.session.commit()

#         print("Database seeded successfully with Admin, and Users!")

#     except IntegrityError as ie:
#         print(f"Integrity error occurred: {ie}")
#         db.session.rollback()  

#     except Exception as e:
#         print(f"An error occurred while seeding the database: {e}")
#         db.session.rollback()


# def add_cart_items_for_user(user, item):
#         """Add sample cart items for a user."""
#         cart_items = [
#             Cart(user_id=user.id, item_id=1, quantity=2),  
#             Cart(user_id=user.id, item_id=2, quantity=1)   
#         ]
#         db.session.add_all(cart_items)
#         db.session.commit()
#         return cart_items