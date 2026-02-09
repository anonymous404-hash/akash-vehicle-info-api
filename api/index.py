from flask import Flask, request, jsonify
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import pytz

app = Flask(__name__)

# ===============================================
# 🔐 API KEY DATABASE (Yahan Keys Manage Karo)
# ===============================================
# Format: "KEY_STRING": "YYYY-MM-DD" (Expiry Date)
API_KEYS = {
    "AKASH_PAID8DAYS": "2026-01-25",
    "AKASH_PAID30DAYS": "2026-02-15",
    "FREE_TRY": "2026-01-18",
    "MY_TEST_KEY": "2030-12-31" 
}

# ===============================================
# ⚙️ CONFIGURATION
# ===============================================
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36",
    "Referer": "https://vahanx.in/",
}

def clean_text(text):
    if not text:
        return "NA"
    return text.strip()

# ===============================================
# 🚙 SCRAPING LOGIC
# ===============================================
def get_vehicle_data(rc_number):
    rc = rc_number.strip().upper()
    url = f"https://vahanx.in/rc-search/{rc}"
    
    try:
        response = requests.get(url, headers=HEADERS, timeout=9)
        if response.status_code != 200:
            return {"error": "Source website unreachable"}
        soup = BeautifulSoup(response.text, "html.parser")
    except Exception as e:
        return {"error": str(e)}

    # Helper to extract text safely
    def get_by_label(label_text):
        element = soup.find("span", string=lambda t: t and label_text.lower() in t.lower())
        if element:
            parent = element.find_parent("div")
            if parent:
                value = parent.find("p")
                if value:
                    return clean_text(value.text)
        return "NA"

    # --- Data Extraction ---
    reg_num_tag = soup.find("h1")
    reg_display = clean_text(reg_num_tag.text) if reg_num_tag else rc

    basic_info = {
        "address": get_by_label("Address"),
        "city": get_by_label("City Name"),
        "code": get_by_label("Code"),
        "model_name": get_by_label("Modal Name") or get_by_label("Model Name"),
        "owner_name": get_by_label("Owner Name"),
        "phone": get_by_label("Phone"),
        "website": "https://transport.assam.gov.in//"
    }

    insurance = {
        "company": get_by_label("Insurance Company"),
        "expiry_date": get_by_label("Insurance Expiry").split("0 years")[0],
        "status": "Active",
        "valid_upto": get_by_label("Insurance Upto")
    }

    ownership = {
        "owner_name": basic_info["owner_name"],
        "rto": get_by_label("Registered RTO")
    }

    vehicle_details = {
        "cubic_capacity": get_by_label("Cubic Capacity"),
        "fuel_type": get_by_label("Fuel Type"),
        "maker": get_by_label("Maker Model"),
        "model": get_by_label("Model Name"),
        "seating_capacity": get_by_label("Seating Capacity"),
        "vehicle_class": get_by_label("Vehicle Class")
    }

    validity = {
        "fitness_upto": get_by_label("Fitness Upto"),
        "insurance_status": "Checked Above",
        "insurance_upto": get_by_label("Insurance Upto"),
        "registration_date": get_by_label("Registration Date"),
        "tax_upto": get_by_label("Tax Upto"),
        "vehicle_age": get_by_label("Vehicle Age")
    }

    puc_details = {
        "puc_valid_upto": get_by_label("PUC Upto")
    }

    # Handling Financier (Merging from Other Info)
    financer = get_by_label("Financier Name")
    if financer == "NA":
        financer = get_by_label("Financer Name")

    other_info = {
        "blacklist_status": get_by_label("Blacklist Status"),
        "financer": financer,
        "noc": get_by_label("NOC Details"),
        "permit_type": get_by_label("Permit Type")
    }

    return {
        "status": "success",
        "registration_number": reg_display,
        "basic_info": basic_info,
        "ownership_details": ownership,
        "vehicle_details": vehicle_details,
        "insurance": insurance,
        "validity": validity,
        "puc_details": puc_details,
        "other_info": other_info
    }

# ===============================================
# 🌐 API ROUTE WITH KEY AUTH
# ===============================================
@app.route('/', methods=['GET'])
def home():
    # 1. Input Check
    rc = request.args.get('rc') or request.args.get('num') # 'num' bhi support karega
    user_key = request.args.get('key')

    # 2. Key Validation Logic
    if not user_key:
        return jsonify({"error": "API Key missing!", "status": "Failed"}), 401
    
    if user_key not in API_KEYS:
        return jsonify({"error": "Invalid API Key!", "status": "Failed"}), 401

    # 3. Expiry Logic (India Time)
    expiry_str = API_KEYS[user_key]
    tz_india = pytz.timezone('Asia/Kolkata')
    today = datetime.now(tz_india).date()
    expiry_date = datetime.strptime(expiry_str, "%Y-%m-%d").date()

    # Calculate Days Remaining
    delta = expiry_date - today
    days_left = delta.days

    # 4. Check if Expired
    if days_left < 0:
        return jsonify({
            "error": "Key Expired!",
            "expiry_date": expiry_str,
            "status": "Expired",
            "message": f"Aapki key {expiry_str} ko khatam ho chuki hai."
        }), 403

    # 5. Check RC Number
    if not rc:
        return jsonify({
            "error": "RC Number missing. Use ?rc=NUMBER&key=YOURKEY",
            "key_details": {
                "expiry_date": expiry_str,
                "days_remaining": f"{days_left} Days" if days_left > 0 else "Last Day Today",
                "status": "Active"
            }
        }), 400

    # 6. Fetch Data
    data = get_vehicle_data(rc)

    # 7. Add Branding & Key Info (Clean Response)
    if "error" in data:
        return jsonify(data), 500

    # Adding the specific key details requested
    data["key_details"] = {
        "expiry_date": expiry_str,
        "days_remaining": f"{days_left} Days" if days_left > 0 else "Last Day Today",
        "status": "Active"
    }
    data["source"] = "@AKASHHACKER"
    data["powered_by"] = "@AKASHHACKER"

    return jsonify(data)

# Local testing
if __name__ == '__main__':
    app.run(debug=True)
