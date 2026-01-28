import os
import json
import google.generativeai as genai
from flask import Flask, jsonify, request
from flask_cors import CORS
from werkzeug.utils import secure_filename
from datetime import datetime
from dotenv import load_dotenv #

# 1. Load file .env di awal aplikasi
load_dotenv() #

app = Flask(__name__)
CORS(app)

# 2. Tarik API KEY dari environment variable
# Ganti hardcoded key dengan os.getenv
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY") #

# Cek apakah API Key ada, agar server tidak error saat dijalankan
if not GEMINI_API_KEY:
    print("⚠️ PERINGATAN: GEMINI_API_KEY tidak ditemukan di file .env!")
else:
    genai.configure(api_key=GEMINI_API_KEY)

# Kita pakai model yang terbukti berhasil di akunmu
model = genai.GenerativeModel('gemini-2.5-flash') #

# --- KONFIGURASI FILE ---
UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), 'uploads')
DATABASE_FILE = os.path.join(os.path.dirname(__file__), 'data.json')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'webp'}

# ... (Fungsi load_data, save_data, dan allowed_file tetap sama) ...

# --- ENDPOINT 1: DASHBOARD ---
@app.route('/api/dashboard', methods=['GET'])
def get_dashboard_data():
    transactions = load_data()
    total_spending = sum(item['total_amount'] for item in transactions)
    recent_transactions = sorted(transactions, key=lambda x: x['id'], reverse=True)[:5]
    
    data = {
        "user_name": "Haris", #
        "total_spending": total_spending,
        "items_scanned": len(transactions),
        "spending_trend": [
            {"name": "Week 1", "amount": 1200000},
            {"name": "Week 2", "amount": 900000},
            {"name": "Week 3", "amount": 1500000},
            {"name": "Week 4", "amount": total_spending / 4},
        ],
        "recent_transactions": recent_transactions
    }
    return jsonify(data)

# ... (Endpoint /api/chat, /api/scan-receipt, /api/insights, dan /api/transactions tetap sama) ...

if __name__ == '__main__':
    # Saat di Render nanti, port akan diambil secara dinamis
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, host='0.0.0.0', port=port)