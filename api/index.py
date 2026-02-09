from flask import Flask, request, jsonify
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import pytz

app = Flask(__name__)

# ===============================================
# 🔐 API KEY DATABASE
# ===============================================
API_KEYS = {
    "AKASH_PAID8DAYS": "2026-02-15",
    "AKASH_PAID30DAYS": "2026-03-15",
    "FREE_TRY": "2026-01-18",
    "MY_TEST_KEY": "2030-12-31" 
}

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
}

def get_state_website(rc):
    # RTO code se state website nikalne ka logic
    state_code = rc[:2].upper()
    state_sites = {
        "AS": "https://transport.assam.gov.in/",
        "HR": "https://haryanatransport.gov.in/",
        "DL": "https://transport.delhi.gov.in/",
        "UP": "https://uptransport.upsdc.gov.in/"
    }
    return state_sites.get(state_code, "https://parivahan.gov.in/")

# ===============================================
# 🚙 SCRAPING LOGIC
# ===============================================
def get_vehicle_data(rc_number):
    rc = rc_number.strip().upper()
    url = f"https://vahanx.in/rc-search/{rc}"
    
    try:
        response = requests.get(url, headers=HEADERS, timeout=10)
        if response.status_code != 200:
            return {"error": "Source down ya RC galat hai"}
        soup = BeautifulSoup(response.text, "html.parser")
    except Exception as e:
        return {"error": str(e)}

    # Improved Label Search
    def get_by_label(labels):
        if isinstance(labels, str): labels = [labels]
        for label in labels:
            element = soup.find("span", string=lambda t: t and label.lower() in t.lower())
            if element:
                parent = element.find_parent(["div", "td", "tr"])
                if parent:
                    # P ya Span ya Div mein value ho sakti hai
                    val = parent.find_all(["p", "span", "div"], recursive=False)
                    for v in val:
                        if v.text.strip() != element.text.strip():
                            return v.text.strip()
        return "NA"

    # Extraction Logic
    ins_expiry = get_by_label(["Insurance Expiry", "Insurance Upto"]).split(" ")[0]
    
    # Check Insurance Validity Dynamically
    ins_status = "Expired"
    try:
        if ins_expiry != "NA":
            exp_dt = datetime.strptime(ins_expiry, "%d-%b-%Y").date()
            if exp_dt >= datetime.now().date():
                ins_status = "Active"
    except: pass

    data = {
        "status": "success",
        "registration_number": rc,
        "basic_info": {
            "address": get_by_label("Address"),
            "city": get_by_label("City Name"),
            "model_name": get_by_label(["Model Name", "Modal Name"]),
            "owner_name": get_by_label("Owner Name"),
            "website": get_state_website(rc)
        },
        "vehicle_details": {
            "cubic_capacity": get_by_label("Cubic Capacity"),
            "fuel_type": get_by_label("Fuel Type"),
            "maker": get_by_label("Maker Model"),
            "seating_capacity": get_by_label("Seating Capacity"),
            "vehicle_class": get_by_label("Vehicle Class")
        },
        "insurance": {
            "company": get_by_label("Insurance Company"),
            "expiry_date": ins_expiry,
            "status": ins_status
        },
        "validity": {
            "fitness_upto": get_by_label("Fitness Upto"),
            "registration_date": get_by_label("Registration Date"),
            "vehicle_age": get_by_label("Vehicle Age")
        }
    }
    return data

# ===============================================
# 🌐 API ROUTE
# ===============================================
@app.route('/', methods=['GET'])
def home():
    rc = request.args.get('rc')
    user_key = request.args.get('key')

    if not user_key or user_key not in API_KEYS:
        return jsonify({"error": "Invalid or Missing API Key"}), 401

    # Time Logic
    tz_india = pytz.timezone('Asia/Kolkata')
    today = datetime.now(tz_india).date()
    expiry_date = datetime.strptime(API_KEYS[user_key], "%Y-%m-%d").date()
    days_left = (expiry_date - today).days

    if days_left < 0:
        return jsonify({"status": "Expired", "error": "Key khatam ho gayi"}), 403

    if not rc:
        return jsonify({
            "msg": "Send RC number",
            "key_details": {"days_remaining": f"{days_left} Days", "status": "Active"}
        })

    result = get_vehicle_data(rc)
    if "error" in result: return jsonify(result), 400

    # Meta Info
    result["key_details"] = {
        "expiry_date": str(expiry_date),
        "days_remaining": f"{days_left} Days",
        "status": "Active"
    }
    result["powered_by"] = "@AKASHHACKER"
    
    return jsonify(result)

if __name__ == '__main__':
    app.run(port=5000)
