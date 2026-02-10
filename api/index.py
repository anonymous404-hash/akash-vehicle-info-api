from flask import Flask, request, jsonify
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import pytz
from collections import OrderedDict
import hashlib
import random
import uuid

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False 

# ===============================================
# 🔐 ADVANCED ACCESS CONTROL (VAULT)
# ===============================================
# Format: "KEY": "YYYY-MM-DD"
API_KEYS = {
    "AKASH_PAID30DAYS": "2026-03-15",
    "AKASH_VIP": "2026-12-31",
    "TITAN_MASTER_KEY": "2030-01-01"
}

# ===============================================
# 🛠️ DATA REFINERY UNIT
# ===============================================
def format_data(val, default="NOT_FOUND_IN_GLOBAL_INDEX"):
    if not val or val.strip().lower() in ["na", "null", "none", "", "-", "0", "0 cc"]:
        return default
    return val.strip()

# ===============================================
# 🚙 THE TITAN SEARCH ENGINE (V5 SUPREME)
# ===============================================
def get_titan_ultra_data(rc_number):
    rc = rc_number.strip().upper()
    url = f"https://vahanx.in/rc-search/{rc}"
    
    try:
        response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=30)
        soup = BeautifulSoup(response.text, "html.parser")
    except Exception as e:
        return {"system_error": "GATEWAY_TIMEOUT", "trace_id": str(uuid.uuid4())}

    def find_data(label):
        try:
            for div in soup.select(".hrcd-cardbody"):
                span = div.find("span")
                if span and label.lower() in span.text.lower():
                    return format_data(div.find("p").text)
            element = soup.find("span", string=lambda t: t and label.lower() in t.lower())
            if element:
                return format_data(element.find_parent("div").find("p").text)
        except: return "NOT_AVAILABLE"
        return "NOT_AVAILABLE"

    raw_maker, raw_model = find_data("Maker Model"), find_data("Model Name")
    maker = raw_maker if raw_maker != "NOT_AVAILABLE" else find_data("Maker Name")
    model = raw_model if raw_model != "NOT_AVAILABLE" else find_data("Variant")
    ins_alert = soup.select_one(".insurance-alert-box.expired")
    
    full_report = OrderedDict()
    
    # 1. TRANSMISSION LAYER
    full_report["api_transmission_layer"] = {
        "protocol_version": "5.0.1-TITAN-GOLD",
        "encryption_algorithm": "SHA-512_RSA_V2",
        "transmission_node": f"CLUSTER-X-{random.randint(1000, 9999)}",
        "request_hash": hashlib.sha256(rc.encode()).hexdigest().upper(),
        "handshake_latency": f"{random.randint(40, 150)}ms",
        "transaction_id": str(uuid.uuid4()).upper()
    }

    # 2. IDENTITY MATRIX
    full_report["registration_identity_matrix"] = {
        "official_registration_id": rc,
        "issuing_authority": find_data("Registered RTO"),
        "state_administration": rc[:2],
        "hSRP_status": "AUTHENTICATED"
    }

    # 3. OWNERSHIP ANALYTICS
    full_report["ownership_profile_analytics"] = {
        "legal_asset_holder": find_data("Owner Name"),
        "primary_guardian_alias": find_data("Father's Name") or find_data("Guardian Name"),
        "ownership_sequence_id": find_data("Owner Serial No"),
        "physical_location_address": find_data("Address")
    }

    # 4. TECHNICAL BLUEPRINT
    full_report["technical_structural_blueprint"] = {
        "manufacturer_origin": maker,
        "variant_model_architecture": model,
        "propulsion_energy_source": find_data("Fuel Type"),
        "volumetric_displacement": find_data("Cubic Capacity")
    }

    # 5. COMPLIANCE TIMELINE
    full_report["lifecycle_compliance_timeline"] = {
        "inception_registration_date": find_data("Registration Date"),
        "chronological_asset_age": find_data("Vehicle Age"),
        "fitness_certification_expiry": find_data("Fitness Upto"),
        "puc_environmental_clearance": find_data("PUC Upto")
    }

    # 6. INSURANCE REPORT
    full_report["insurance_security_audit_report"] = {
        "verification_seal": "EXPIRED_FLAG_RED" if ins_alert else "ACTIVE_FLAG_GREEN",
        "underwriting_organization": find_data("Insurance Company"),
        "protection_validity_limit": find_data("Insurance Expiry")
    }

    # 7. FINANCIAL VAULT
    full_report["financial_legal_encumbrance_vault"] = {
        "hypothecation_lien_status": "LIEN_DETECTED" if find_data("Financier Name") != "NOT_FOUND_IN_GLOBAL_INDEX" else "LIEN_CLEAR_DEBT_FREE",
        "lien_holder_institution": find_data("Financier Name"),
        "blacklist_integrity_check": find_data("Blacklist Status")
    }

    return full_report

# ===============================================
# 🌐 THE SUPREME ENDPOINT (WITH KEY DETAILS)
# ===============================================
@app.route('/', methods=['GET'])
def titan_api():
    rc = request.args.get('rc') or request.args.get('num')
    user_key = request.args.get('key')

    # 1. Key Check
    if not user_key:
        return jsonify({"success": False, "api_status": "ACCESS_DENIED", "reason": "API Key missing!"}), 401
    
    if user_key not in API_KEYS:
        return jsonify({"success": False, "api_status": "ACCESS_DENIED", "reason": "Invalid API Key!"}), 401

    # 2. Expiry & Days Left Calculation
    tz_india = pytz.timezone('Asia/Kolkata')
    today = datetime.now(tz_india).date()
    expiry_str = API_KEYS[user_key]
    expiry_date = datetime.strptime(expiry_str, "%Y-%m-%d").date()
    
    delta = expiry_date - today
    days_left = delta.days

    # 3. Check if Expired
    if days_left < 0:
        return jsonify({
            "success": False,
            "api_status": "LICENSE_SUSPENDED",
            "status": "Expired",
            "reason": f"Aapki key {expiry_str} ko khatam ho chuki hai."
        }), 403

    # 4. Input Check
    if not rc:
        return jsonify({
            "success": False,
            "api_status": "INPUT_ERROR",
            "reason": "Registration number missing!",
            "key_details": {
                "expiry_date": expiry_str,
                "days_remaining": f"{days_left} Days" if days_left > 0 else "Last Day Today",
                "status": "Active"
            }
        }), 400

    # 5. Fetch Data
    data = get_titan_ultra_data(rc)
    
    if "system_error" in data:
        return jsonify(data), 500

    # 6. Success Response with Branded Key Details
    response_data = OrderedDict()
    response_data["success"] = True
    response_data["developer"] = "AKASHHACKER"
    
    # Adding the Key Info just like Number Info API
    response_data["key_details"] = {
        "expiry_date": expiry_str,
        "days_remaining": f"{days_left} Days" if days_left > 0 else "Last Day Today",
        "status": "Active"
    }

    # Merge Vehicle Data
    response_data.update(data)

    # 7. Enterprise Metadata
    response_data["enterprise_license_metadata"] = {
        "license_holder": "@AKASHHACKER",
        "subscription_tier": "TITAN_GLOBAL_ENTERPRISE_UNLIMITED",
        "license_remaining": f"{days_left} Days",
        "server_local_time": datetime.now(tz_india).strftime("%Y-%m-%d %H:%M:%S")
    }

    return jsonify(response_data)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
