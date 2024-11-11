from models import db, Item, SpecialCategory
from datetime import datetime

items = [
    Item(id= 1, item_name= "Pixel 8 Pro", item_features=["50MP main camera", "Google Tensor G2 processor", "120Hz display"], item_price= 99900, item_prev_price= 1, item_image_url= "images/Pixel 8 Pro.jpeg", item_category= "Smartphone", items_instock= 7),
    Item(id= 2, item_name= "MacBook Pro 14-inch", item_features=["M2 Pro/Max chip", "Liquid Retina XDR display", "MagSafe charging"], item_price= 199900, item_prev_price= 1, item_image_url= "images/MacBook Pro 14-inch.jpg", item_category= "Laptop", items_instock= 7),
    Item(id= 3, item_name= "Apple iMac 27-inch", item_features=["5K Retina display", "1080p FaceTime HD camera", "studio-quality mics"], item_price= 179900, item_prev_price= 1, item_image_url= "images/Apple iMac 27-inch.jpg", item_category= "Desktop", items_instock= 7),
    Item(id= 4, item_name= "Sony WH-1000XM5", item_features=["Adaptive Sound Control", "Speak-to-Chat", "HD Noise Cancelling Processor QN1"], item_price= 39900, item_prev_price= 1, item_image_url= "images/Sony WH-1000XM5.jpg", item_category= "Headphones", items_instock= 7),
    Item(id= 5, item_name= "Apple AirPods Pro (2nd Generation)", item_features=["Adaptive Transparency", "Personalized Spatial Audio", "MagSafe Charging Case"], item_price= 24900, item_prev_price= 1, item_image_url= "images/Apple AirPods Pro (2nd Generation).jpeg", item_category= "Earbuds", items_instock= 7),
    Item(id= 6, item_name= "LG C3 Series OLED TV", item_features=["Self-Lit OLED", "α9 Gen6 Processor 4K", "4K, Dolby Vision IQ"], item_price= 149900, item_prev_price= 1, item_image_url= "images/LG C3 Series OLED TV.jpg", item_category= "TV", items_instock= 7),
    Item(id= 7, item_name= "Bose Soundbar 700", item_features=["Dolby Atmos", "Bose Voice Assistant", "Wi-Fi and Bluetooth Connectivity"], item_price= 79900, item_prev_price= 1, item_image_url= "images/Bose Soundbar 700.jpeg", item_category= "Sound system", items_instock= 7),
    Item(id= 8, item_name= "KEF LS50 Meta", item_features=["Uni-Core Driver", "Concentric Driver", "Titanium Dome Tweeter"], item_price= 299900, item_prev_price= 1, item_image_url= "images/KEF LS50 Meta.jpg_30ac01", item_category= "Speakers", items_instock= 7),
    Item(id= 9, item_name= "Apple Watch Series 9", item_features=["Always-On Retina Display", "Advanced Heart Rate Tracking", "Crash Detection"], item_price= 39900, item_prev_price= 1, item_image_url= "images/Apple Watch Series 9.jpg", item_category= "Smartwatch", items_instock= 7),
    Item(id= 10, item_name= "Apple iPad Pro (12.9-inch)", item_features=["Liquid Retina XDR Display", "M2 Chip", "LiDAR Scanner"], item_price= 109900, item_prev_price= 1, item_image_url= "images/Apple iPad Pro (12.9-inch).jpeg", item_category= "Tablet", items_instock= 7),
    Item(id= 11, item_name= "iPhone 15 Pro Max", item_features=["A17 Bionic chip", "Dynamic Island, ProMotion display", "triple-camera system"], item_price= 109900, item_prev_price= 1, item_image_url= "images/iPhone 15 Pro Max.jpg", item_category= "Smartphone", items_instock= 7),
    Item(id= 12, item_name= "Dell XPS 13 Plus", item_features=["12th Gen Intel Core processor", "OLED display", "capacitive touch function keys"], item_price= 149900, item_prev_price= 1, item_image_url= "images/Dell XPS 13 Plus.jpg", item_category= "Laptop", items_instock= 7),
    Item(id= 13, item_name= "Dell XPS Desktop", item_features=["13th Gen Intel Core processor", "NVIDIA GeForce RTX 40 series graphics", "liquid cooling"], item_price= 129900, item_prev_price= 1, item_image_url= "images/Dell XPS Desktop.jpg", item_category= "Desktop", items_instock= 7),
    Item(id= 14, item_name= "Bose QuietComfort 45", item_features=["Active EQ", "TriPort Acoustic Headphone Structure", "Aware Mode"], item_price= 32900, item_prev_price= 1, item_image_url= "images/Bose QuietComfort 45.jpg", item_category= "Headphones", items_instock= 7),
    Item(id= 15, item_name= "Sony WF-1000XM5", item_features=["Integrated Processor V1", "Dynamic Driver X", "Adaptive Sound Control"], item_price= 29900, item_prev_price= 1, item_image_url= "images/Sony WF-1000XM5.jpg", item_category= "Earbuds", items_instock= 7),
    Item(id= 16, item_name= "Samsung Neo QLED 8K TV", item_features=["Neo Quantum Processor 8K", "Quantum Matrix Technology", "Real Depth Enhancer"], item_price= 299900, item_prev_price= 1, item_image_url= "images/Samsung Neo QLED 8K TV.jpeg", item_category= "TV", items_instock= 7),
    Item(id= 17, item_name= "Klipsch Cinema 600", item_features=["Reference Premiere Series Drivers", "Tractrix Horn Technology", "Wireless Subwoofer"], item_price= 129900, item_prev_price= 1, item_image_url= "images/Klipsch Cinema 600.jpg", item_category= "Sound system", items_instock= 7),
    Item(id= 18, item_name= "Focal Kanta No.2", item_features=["Beryllium Tweeter", "Flax Cone Midrange Driver", "Slatefiber Cone Bass Driver"], item_price= 1299900, item_prev_price= 1, item_image_url= "images/Focal Kanta No.2", item_category= "Speakers", items_instock= 7),
    Item(id= 19, item_name= "Samsung Galaxy Watch 6 Classic", item_features=["Super AMOLED Display", "Advanced Sleep Tracking", "Blood Pressure Monitoring"], item_price= 34900, item_prev_price= 1, item_image_url= "images/Samsung Galaxy Watch 6 Classic.jpg", item_category= "Smartwatch", items_instock= 7),
    Item(id= 20, item_name= "Samsung Galaxy Tab S9 Ultra", item_features=["Dynamic AMOLED 2X Display", "Snapdragon 8 Gen 2", "S Pen"], item_price= 119900, item_prev_price= 1, item_image_url= "images/Samsung Galaxy Tab S9 Ultra.jpg", item_category= "Tablet", items_instock= 7),
    Item(id= 21, item_name= "Samsung Galaxy S24 Ultra", item_features=["200MP main camera", "108MP ultrawide camera", "Snapdragon 8 Gen 3 processor, 120Hz display"], item_price= 119900, item_prev_price= 1, item_image_url= "images/Samsung Galaxy S24 Ultra.jpg", item_category= "Smartphone", items_instock= 7),
    Item(id= 22, item_name= "HP Spectre x360", item_features=["12th Gen Intel Core processor", "OLED display", "360-degree hinge"], item_price= 139900, item_prev_price= 1, item_image_url= "images/HP Spectre x360.png", item_category= "Laptop", items_instock= 7),
    Item(id= 23, item_name= "Lenovo Legion Tower 7i", item_features=["13th Gen Intel Core processor", "NVIDIA GeForce RTX 40 series graphics", "7.1 channel surround sound"], item_price= 199900, item_prev_price= 1, item_image_url= "images/Lenovo Legion Tower 7i.jpg", item_category= "Desktop", items_instock= 7),
    Item(id= 24, item_name= "Apple AirPods Max", item_features=["Adaptive EQ", "Spatial Audio with Dynamic Head Tracking", "Active Noise Cancellation"], item_price= 54900, item_prev_price= 1, item_image_url= "images/Apple AirPods Max.jpg", item_category= "Headphones", items_instock= 7),
    Item(id= 25, item_name= "Bose QuietComfort Earbuds II", item_features=["CustomTune Sound Calibration", "Active Noise Cancellation", "Aware Mode"], item_price= 29900, item_prev_price= 1, item_image_url= "images/Bose QuietComfort Earbuds II.jpg", item_category= "Earbuds", items_instock= 7),
    Item(id= 26, item_name= "Sony BRAVIA XR A95K OLED TV", item_features=["Cognitive Processor XR", "Perfect Contrast Booster", "Acoustic Surface Audio+"], item_price= 249900, item_prev_price= 1, item_image_url= "images/Sony BRAVIA XR A95K OLED TV.jpg", item_category= "TV", items_instock= 7),
    Item(id= 27, item_name= "Sennheiser AMBEO Soundbar", item_features=["7 Drivers", "Up-Firing Speakers", "Dolby Atmos"], item_price= 249900, item_prev_price= 1, item_image_url= "images/Sennheiser AMBEO Soundbar.jpg", item_category= "Sound system", items_instock= 7),
    Item(id= 28, item_name= "Klipsch RP-8000F", item_features=["Tractrix Horn-Loaded Compression Driver", "Cerametallic Woofer", "Powerful Bass Response"], item_price= 199900, item_prev_price= 1, item_image_url= "images/Klipsch RP-8000F1.jpeg", item_category= "Speakers", items_instock= 7),
    Item(id= 29, item_name= "Fitbit Sense 2", item_features=["ECG App", "Skin Temperature Sensor", "Stress Management Score"], item_price= 29900, item_prev_price= 1, item_image_url= "images/Fitbit Sense 2.jpg", item_category= "Smartwatch", items_instock= 7),
    Item(id= 30, item_name= "Microsoft Surface Pro 9", item_features=["PixelSense Flow Display", "12th Gen Intel Core Processor", "Slim Pen 2"], item_price= 99900, item_prev_price= 1, item_image_url= "images/Microsoft Surface Pro 9.jpg", item_category= "Tablet", items_instock= 7),
    Item(id= 31, item_name= "OnePlus 12", item_features=["Snapdragon 8 Gen 3 processor", "120Hz display", "Hasselblad camera system"], item_price= 79900, item_prev_price= 1, item_image_url= "images/OnePlus 12.jpg", item_category= "Smartphone", items_instock= 7),
    Item(id= 32, item_name= "Acer Swift X", item_features=["12th Gen Intel Core processor", "OLED display", "long battery life"], item_price= 99900, item_prev_price= 1, item_image_url= "images/Acer Swift X.jpg", item_category= "Laptop", items_instock= 7),
    Item(id= 33, item_name= "HP Omen 45L", item_features=["13th Gen Intel Core processor", "NVIDIA GeForce RTX 40 series graphics", "OMEN Lighting Sync"], item_price= 169900, item_prev_price= 1, item_image_url= "images/HP Omen 45L.jpg", item_category= "Desktop", items_instock= 7),
    Item(id= 34, item_name= "Hisense U8H ULED TV", item_features=["ULED", "Quantum Dot Color", "Dolby Vision HDR"], item_price= 79900, item_prev_price= 1, item_image_url= "images/Hisense U8H ULED TV.jpg", item_category= "TV", items_instock= 7),
    Item(id= 35, item_name= "Sennheiser Momentum 4 Wireless", item_features=["Adaptive Noise Cancellation", "Transparent Hearing", "Sound Personalization"], item_price= 34900, item_prev_price= 1, item_image_url= "images/Sennheiser Momentum 4 Wireless.jpg", item_category= "Headphones", items_instock= 7),
    Item(id= 36, item_name= "Sennheiser Momentum True Wireless 3", item_features=["Adaptive Noise Cancellation", "Transparent Hearing", "Adaptive Sound"], item_price= 29900, item_prev_price= 1, item_image_url= "images/Sennheiser Momentum True Wireless 3.jpg", item_category= "Earbuds", items_instock= 7),
    Item(id= 37, item_name= "LG SN11RG", item_features=["AI Sound Pro", "Meridian Audio", "Wireless Rear Speakers"], item_price= 199900, item_prev_price= 1, item_image_url= "images/LG SN11RG.jpg", item_category= "Sound system", items_instock= 7),
    Item(id= 38, item_name= "Klipsch RP-8000F", item_features=["Tractrix Horn-Loaded Compression Driver", "Cerametallic Woofer", "Powerful Bass Response"], item_price= 199900, item_prev_price= 1, item_image_url= "images/Klipsch RP-8000F1.jpeg", item_category= "Speakers", items_instock= 7),
    Item(id= 39, item_name= "Garmin Venu 2 Plus", item_features=["AMOLED Display", "Advanced Workout Tracking", "Health Snapshot"], item_price= 44900, item_prev_price= 1, item_image_url= "images/Garmin Venu 2 Plus.jpeg", item_category= "Smartwatch", items_instock= 7),
    Item(id= 40, item_name= "Amazon Fire HD 10 Plus", item_features=["10.1-inch HD Display", "Octa-Core Processor", "Alexa Built-In"], item_price= 19900, item_prev_price= 1, item_image_url= "images/Amazon Fire HD 10 Plus.jpg", item_category= "Tablet", items_instock= 7),
    Item(id= 41, item_name= "Xiaomi 14 Pro", item_features=["Snapdragon 8 Gen 3 processor", "120Hz display", "Leica camera system"], item_price= 89900, item_prev_price= 1, item_image_url= "images/Xiaomi 14 Pro.jpeg", item_category= "Smartphone", items_instock= 7),
    Item(id= 42, item_name= "Asus Zenbook 14X OLED", item_features=["12th Gen Intel Core processor", "OLED display", "ASUS NumberPad 2.0"], item_price= 129900, item_prev_price= 1, item_image_url= "images/Asus Zenbook 14X OLED.png", item_category= "Laptop", items_instock= 7),
    Item(id= 43, item_name= "ASUS ROG Strix G35CX", item_features=["13th Gen Intel Core processor", "NVIDIA GeForce RTX 40 series graphics", "Aura Sync RGB lighting"], item_price= 169900, item_prev_price= 1, item_image_url= "images/ASUS ROG Strix G35CX.jpg", item_category= "Desktop", items_instock= 7),
    Item(id= 44, item_name= "AKG N900NC M2", item_features=["Active Noise Cancellation", "3D Audio", "Long Battery Life"], item_price= 39900, item_prev_price= 1, item_image_url= "images/AKG N900NC M2.jpg", item_category= "Headphones", items_instock= 7),
    Item(id= 45, item_name= "Jabra Elite 85t", item_features=["Advanced Active Noise Cancellation", "Multi-Point Connection", "HearThrough"], item_price= 22900, item_prev_price= 1, item_image_url= "images/Jabra Elite 85t.jpg", item_category= "Earbuds", items_instock= 7),
    Item(id= 46, item_name= "Panasonic JZ2000 OLED TV", item_features=["OLED Master Panel", "HCX Processor Pro", "Dolby Atmos"], item_price= 349900, item_prev_price= 1, item_image_url= "images/Panasonic JZ2000 OLED TV.jpeg", item_category= "TV", items_instock= 7),
    Item(id= 47, item_name= "JBL Bar 500", item_features=["MultiBeam", "JBL Bass Boost", "Wi-Fi and Bluetooth Connectivity"], item_price= 49900, item_prev_price= 1, item_image_url= "images/JBL Bar 500.jpg", item_category= "Sound system", items_instock= 7),
    Item(id= 48, item_name= "Elac Debut 2.0 F5.2", item_features=["AS-XR Ribbon Tweeter", "Aluminum-Cone Woofer", "Bass Reflex Design"], item_price= 49900, item_prev_price= 1, item_image_url= "images/Elac Debut 2.0 F5.2", item_category= "Speakers", items_instock= 7),
    Item(id= 49, item_name= "Huawei Watch GT 3 Pro", item_features=["AMOLED Display", "ECG and Blood Oxygen Monitoring", "Temperature Sensing"], item_price= 39900, item_prev_price= 1, item_image_url= "images/Huawei Watch GT 3 Pro.jpg", item_category= "Smartwatch", items_instock= 7),
    Item(id= 50, item_name= "Lenovo Tab P11 Pro (Gen 2)", item_features=["OLED Display", "MediaTek Kompanio 1300T", "Dolby Atmos"], item_price= 49900, item_prev_price= 1, item_image_url= "images/Lenovo Tab P11 Pro (Gen 2).jpeg", item_category= "Tablet", items_instock= 7),
    Item(id= 51, item_name= "Google Pixel Fold", item_features=["Google Tensor G2 processor", "120Hz display", "foldable design"], item_price= 179900, item_prev_price= 1, item_image_url= "images/Google Pixel Fold.jpeg", item_category= "Smartphone", items_instock= 7),
    Item(id= 52, item_name= "Microsoft Surface Laptop 5", item_features=["12th Gen Intel Core processor", "PixelSense Flow display", "Dolby Atmos sound system"], item_price= 119900, item_prev_price= 1, item_image_url= "images/Microsoft Surface Laptop 5.png", item_category= "Laptop", items_instock= 7),
    Item(id= 53, item_name= "CyberPowerPC Gamer Xtreme VR", item_features=["13th Gen Intel Core processor", "NVIDIA GeForce RTX 40 series graphics", "VR-ready"], item_price= 189900, item_prev_price= 1, item_image_url= "images/CyberPowerPC Gamer Xtreme VR.jpg", item_category= "Desktop", items_instock= 7),
    Item(id= 54, item_name= "Shure SRH1540", item_features=["Neodymium Drivers", "Closed-Back Design", "High Sensitivity"], item_price= 49900, item_prev_price= 1, item_image_url= "images/Shure SRH1540.jpg", item_category= "Headphones", items_instock= 7),
    Item(id= 55, item_name= "AKG N400BT", item_features=["Bluetooth 5.0", "40mm Drivers", "Long Battery Life"], item_price= 16900, item_prev_price= 1, item_image_url= "images/AKG N400BT.jpg", item_category= "Earbuds", items_instock= 7),
    Item(id= 56, item_name= "Philips OLED+937 TV", item_features=["OLED Display", "P5 Perfect Picture Processor", "Ambilight"], item_price= 289900, item_prev_price= 1, item_image_url= "images/Philips OLED+937 TV.jpeg", item_category= "TV", items_instock= 7),
    Item(id= 57, item_name= "Beyerdynamic DT 1990 Pro", item_features=["Tesla Technology", "Open-Back Design", "High-Resolution Audio"], item_price= 59900, item_prev_price= 1, item_image_url= "images/Beyerdynamic DT 1990 Pro.jpg", item_category= "Speakers", items_instock= 7),
    Item(id= 58, item_name= "Xiaomi Watch S2 Pro", item_features=["AMOLED Display", "Heart Rate and Blood Oxygen Monitoring", "GPS"], item_price= 24900, item_prev_price= 1, item_image_url= "images/Xiaomi Watch S2 Pro.jpg", item_category= "Smartwatch", items_instock= 7),
    Item(id= 59, item_name= "Huawei MatePad Pro 12.6", item_features=["OLED Display", "Snapdragon 888", "HarmonyOS"], item_price= 79900, item_prev_price= 1, item_image_url= "images/Huawei MatePad Pro 12.6.jpg", item_category= "Tablet", items_instock= 7),
    Item(id= 60, item_name= "Motorola Edge 40 Pro", item_features=["Snapdragon 8 Gen 2 processor", "165Hz display", "200MP main camera"], item_price= 69900, item_prev_price= 1, item_image_url= "images/Motorola Edge 40 Pro.jpg", item_category= "Smartphone", items_instock= 7),
    Item(id= 61, item_name= "Lenovo Legion Slim 7", item_features=["13th Gen Intel Core processor", "RTX 4070 Laptop GPU", "165Hz display"], item_price= 249900, item_prev_price= 1, item_image_url= "images/Lenovo Legion Slim 7.jpg", item_category= "Laptop", items_instock= 7),
    Item(id= 62, item_name= "iBUYPOWER Slate MR", item_features=["12th Gen Intel Core processor", "NVIDIA GeForce RTX 30 series graphics", "RGB lighting"], item_price= 99900, item_prev_price= 1, item_image_url= "images/iBUYPOWER Slate MR.jpg", item_category= "Desktop", items_instock= 7),
    Item(id= 63, item_name= "Philips Fidelio X2HR", item_features=["50mm Drivers", "Open-Back Design", "High-Resolution Audio"], item_price= 49900, item_prev_price= 1, item_image_url= "images/Philips Fidelio X2HR.jpg", item_category= "Headphones", items_instock= 7),
    Item(id= 64, item_name= "Beyerdynamic Lagoon ANC", item_features=["Active Noise Cancellation", "Transparent Hearing", "Customizable EQ"], item_price= 24900, item_prev_price= 1, item_image_url= "images/Beyerdynamic Lagoon ANC.jpg", item_category= "Earbuds", items_instock= 7),
    Item(id= 65, item_name= "LG QNED Mini LED TV", item_features=["Mini-LED Backlight", "Quantum Dot Color", "α7 Gen5 AI Processor 4K"], item_price= 129900, item_prev_price= 1, item_image_url= "images/LG QNED Mini LED TV.jpg", item_category= "TV", items_instock= 7),
    Item(id= 66, item_name= "Amazfit GTR 4", item_features=["AMOLED Display", "Blood Oxygen Monitoring", "Stress Monitoring"], item_price= 18900, item_prev_price= 1, item_image_url= "images/Amazfit GTR 4.jpg", item_category= "Smartwatch", items_instock= 7),
    Item(id= 67, item_name= "Xiaomi Pad 6", item_features=["11-inch LCD Display", "Snapdragon 870", "Dolby Atmos"], item_price= 39900, item_prev_price= 1, item_image_url= "images/Xiaomi Pad 6.jpg", item_category= "Tablet", items_instock= 7),
    Item(id= 68, item_name= "Vivo X90 Pro+", item_features=["1-inch sensor main camera", "Zeiss optics", "Snapdragon 8 Gen 2 processor"], item_price= 99900, item_prev_price= 1, item_image_url= "images/Vivo X90 Pro+.jpg", item_category= "Smartphone", items_instock= 7),
    Item(id= 69, item_name= "Polar Vantage V2", item_features=["GPS", "Heart Rate and Power Tracking", "Recovery Insights"], item_price= 49900, item_prev_price= 1, item_image_url= "images/Polar Vantage V2.jpg", item_category= "Smartwatch", items_instock= 7),
    Item(id= 70, item_name= "iPad Air (5th generation)", item_features=["Liquid Retina Display", "M1 Chip", "Center Stage"], item_price= 59900, item_prev_price= 1, item_image_url= "images/iPad Air (5th generation).jpg", item_category= "Tablet", items_instock= 7),
    Item(id= 71, item_name= "OPPO Find X6 Pro", item_features=["MariSilicon X imaging NPU", "50MP ultrawide camera", "Snapdragon 8 Gen 2 processor"], item_price= 109900, item_prev_price= 1, item_image_url= "images/OPPO Find X6 Pro.jpg", item_category= "Smartphone", items_instock= 7),
    Item(id= 72, item_name= "Suunto 9 Peak Pro", item_features=["GPS", "Barometer", "Altimeter"], item_price= 54900, item_prev_price= 1, item_image_url= "images/Suunto 9 Peak Pro.jpeg", item_category= "Smartwatch", items_instock= 7),
    Item(id= 73, item_name= "Samsung Galaxy Tab S8", item_features=["Super AMOLED Display", "Snapdragon 8 Gen 1", "S Pen"], item_price= 79900, item_prev_price= 1, item_image_url= "images/Samsung Galaxy Tab S8.jpg", item_category= "Tablet", items_instock= 7),
    Item(id= 74, item_name= "Redmi Note 13 Pro Plus", item_features=["Dimensity 9200 processor", "108MP main camera", "fast charging"], item_price= 39900, item_prev_price= 1, item_image_url= "images/Redmi Note 13 Pro Plus.jpg", item_category= "Smartphone", items_instock= 7),
    Item(id= 75, item_name= "Withings ScanWatch", item_features=["Mechanical and Digital Display", "ECG and PPG Sensors", "Sleep Tracking"], item_price= 28900, item_prev_price= 1, item_image_url= "images/Withings ScanWatch.jpg", item_category= "Smartwatch", items_instock= 7),
    Item(id= 76, item_name= "Lenovo Yoga Tab 13", item_features=["OLED Display", "Snapdragon 870", "JBL Speakers"], item_price=67900, item_prev_price= 1, item_image_url= "images/Lenovo Yoga Tab 13.jpeg", item_category= "Tablet", items_instock= 7)
]

db.session.add_all(items)

    print("Items seeded successfully!")
    
    
    print("Seeding special categories...")
    
    special_categories = [
        SpecialCategory(name= "daily_deals"),
        SpecialCategory(name= "best_seller"),
        SpecialCategory(name= "season_offers"),
        SpecialCategory(name= "hot_&_new")
    ]
    
    db.session.add_all(special_categories)
    
    db.session.commit()
    
    print("Special categories seeded successfully!")
    
    print("Adding items to special categories...")
    
    daily_deals_special_category = SpecialCategory.query.filter_by(name = "daily_deals").first()
    best_seller_special_category = SpecialCategory.query.filter_by(name = "best_seller").first()
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
    

    # Commit to save the items
    db.session.commit()

    print("Database seeded successfully!")