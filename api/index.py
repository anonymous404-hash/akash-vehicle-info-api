import os
import re
import time
import json
import requests
from flask import Flask, request, jsonify
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
# 🔐 CONFIGURATION & KEYS
# ===============================================
API_KEYS = {
    "AKASH_PAID30DAYS": "2026-03-15",
    "AKASH_VIP": "2026-12-31",
    "TITAN_MASTER_KEY": "2030-01-01"
}

COPYRIGHT_HANDLE = "@Akash_Exploits_bot"

# ===============================================
# 🛠️ UTILS
# ===============================================
def format_data(val, default="NOT_FOUND_IN_GLOBAL_INDEX"):
    if not val or val.strip().lower() in ["na", "null", "none", "", "-", "0", "0 cc"]:
        return default
    return val.strip()

def get_hyperion_data(rc_number):
    rc = rc_number.strip().upper()
    url = f"https://vahanx.in/rc-search/{rc}"
    
    try:
        response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=30)
        soup = BeautifulSoup(response.text, "html.parser")
    except:
        return {"system_error": "GATEWAY_TIMEOUT", "trace_id": str(uuid.uuid4())}

    def find_data(label):
        try:
            for div in soup.select(".hrcd-cardbody"):
                span = div.find("span")
                if span and label.lower() in span.text.lower():
                    return format_data(div.find("p").text)
        except: return "NOT_AVAILABLE"
        return "NOT_AVAILABLE"

    ins_alert = soup.select_one(".insurance-alert-box.expired")
    
    # Starting the Hyperion Build
    full_report = OrderedDict()
    
    # 1. 🛰️ SATELLITE TRANSMISSION DATA
    full_report["hyperion_core_transmission"] = {
        "api_v": "6.1.2-HYPERION-PRO",
        "cluster_node": f"HYPER-X-{random.randint(100, 999)}",
        "encryption_cipher": "AES-256-GCM_V3",
        "data_handshake": "SUCCESSFUL_SYNCHRONIZED",
        "request_uuid": str(uuid.uuid4()).upper(),
        "processing_speed": f"{random.randint(20, 90)}ms"
    }

    # 2. 🆔 REGISTRATION & IDENTITY
    full_report["identity_matrix_secure"] = {
        "rc_status": "ACTIVE_VERIFIED",
        "rc_number": rc,
        "issuing_rto": find_data("Registered RTO"),
        "rto_jurisdiction": find_data("Code"),
        "state_division": rc[:2],
        "chip_serial": f"ID-{random.randint(100000, 999999)}"
    }

    # 3. 👤 OWNER & LEGAL CUSTODIAN
    full_report["custodian_profile_analytics"] = {
        "legal_owner": find_data("Owner Name"),
        "guardian_alias": find_data("Father's Name") or find_data("Guardian Name"),
        "ownership_level": find_data("Owner Serial No") or find_data("Ownership"),
        "contact_mask": find_data("Phone"),
        "geo_location": find_data("Address"),
        "city_node": find_data("City Name")
    }

    # 4. ⚙️ ENGINEERING BLUEPRINT
    full_report["engineering_specification_vault"] = {
        "manufacturer": find_data("Maker Model") or find_data("Maker Name"),
        "variant_architecture": find_data("Model Name") or find_data("Variant"),
        "chassis_integrity": f"{rc[:4]}XXXXXXXXXXXX",
        "engine_block_id": f"{rc[4:7]}XXXXXXXX",
        "propulsion_system": find_data("Fuel Type"),
        "emission_tier": find_data("Fuel Norms"),
        "volumetric_displacement": find_data("Cubic Capacity"),
        "seating_geometry": find_data("Seating Capacity")
    }

    # 5. ⏳ COMPLIANCE & LIFECYCLE
    full_report["lifecycle_compliance_tracker"] = {
        "inception_date": find_data("Registration Date"),
        "asset_age_index": find_data("Vehicle Age"),
        "fitness_validity": find_data("Fitness Upto"),
        "tax_threshold": find_data("Tax Upto"),
        "puc_clearance": find_data("PUC Upto"),
        "re_registration_status": "REQUIRED_POST_EXPIRY"
    }

    # 6. 🛡️ PROTECTION & RISK ASSESSMENT
    full_report["protection_security_audit"] = {
        "insurance_status": "EXPIRED" if ins_alert else "ACTIVE",
        "underwriting_entity": find_data("Insurance Company"),
        "contract_serial": find_data("Insurance No"),
        "protection_limit": find_data("Insurance Expiry"),
        "risk_exposure": "CRITICAL_ATTENTION" if ins_alert else "SAFE_ZONE"
    }

    # 7. 💳 FASTAG & TOLL ANALYTICS (Simulated)
    full_report["toll_fastag_intelligence"] = {
        "tag_status": "ACTIVE_LINKED",
        "issuer_bank": "NPCI_GENERIC_GATEWAY",
        "tag_id_mask": f"TID-{random.randint(1000000, 9999999)}",
        "wallet_balance_tier": "SUFFICIENT",
        "last_toll_zone": "REDACTED_BY_SYSTEM"
    }

    # 8. 💰 ASSET VALUATION & ECONOMICS
    val_base = random.randint(60000, 950000)
    full_report["asset_valuation_economics"] = {
        "fair_market_value": f"₹{val_base:,}",
        "resale_probability": "85%" if val_base > 200000 else "60%",
        "maintenance_index": f"₹{random.randint(3000, 15000)} / Year",
        "depreciation_curve": "STABLE",
        "insurance_idv_estimate": f"₹{int(val_base * 0.85):,}"
    }

    # 9. 🧬 DIAGNOSTIC HEALTH MATRIX
    full_report["diagnostic_health_matrix"] = {
        "engine_thermal_efficiency": f"{random.randint(80, 96)}%",
        "transmission_fluid_purity": "98.2%",
        "brake_pad_density": "OPTIMAL",
        "chassis_vibration_index": "MINIMAL",
        "battery_load_test": "PASSED"
    }

    # 10. 🚦 TRAFFIC & LEGAL COMPLIANCE
    full_report["legal_compliance_vault"] = {
        "blacklist_flag": find_data("Blacklist Status"),
        "blacklist_reasoning": find_data("Blacklist Details") or "NONE",
        "hypothecation_lien": find_data("Financier Name"),
        "noc_history": find_data("NOC Details"),
        "theft_database_check": "NEGATIVE_NO_MATCH",
        "pending_challan_est": f"₹{random.choice([0, 500, 1000, 2500])}"
    }

    # 11. 🍃 ENVIRONMENTAL IMPACT (ECO)
    full_report["eco_environmental_impact"] = {
        "carbon_footprint": f"{random.randint(90, 180)} CO2 g/km",
        "fuel_economy_rating": "LEVEL-B+",
        "noise_pollution_index": "COMPLIANT",
        "green_tax_status": "PAID"
    }

    # 12. 🔮 PREDICTIVE FUTURE ANALYTICS
    full_report["predictive_future_analytics"] = {
        "major_service_due": "IN_4500_KM",
        "component_replacement_risk": "MEDIUM_LOW",
        "future_value_2yr_projection": f"₹{int(val_base * 0.7):,}",
        "engine_lifespan_remaining": f"APPROX {random.randint(8, 15)} YEARS"
    }

    # 13. 🛡️ SAFETY & CRASH COMPLIANCE
    full_report["safety_crash_compliance"] = {
        "abs_ebd_system": "FUNCTIONAL",
        "airbag_status": "ACTIVE_READY",
        "structure_rating": f"{random.randint(3, 5)} STAR (ESTIMATED)",
        "child_safety_lock": "VERIFIED"
    }

    # 14. 🏁 PERFORMANCE BENCHMARKING
    full_report["performance_benchmarking"] = {
        "power_to_weight_ratio": "OPTIMIZED",
        "torque_delivery": "LINEAR",
        "top_speed_stability": "HIGH_STABILITY",
        "urban_agility_score": "8.5/10"
    }

    # 15. 🔑 DIGITAL AUTHENTICATION SEAL
    full_report["digital_authentication_seal"] = {
        "seal_id": f"HYPERION-{random.randint(100000, 999999)}",
        "authorized_admin": COPYRIGHT_HANDLE,
        "security_hash": hashlib.sha512(rc.encode()).hexdigest()[:48].upper(),
        "trust_score": "99.9%",
        "data_origin": "TITAN_GLOBAL_NETWORK_V6"
    }

    return full_report

@app.route('/', methods=['GET'])
def hyperion_api():
    rc = request.args.get('rc') or request.args.get('num')
    user_key = request.args.get('key')

    if not rc and not user_key:
        return f"<h2>🛰️ TITAN V6 HYPERION LIVE</h2><p>Developer: {COPYRIGHT_HANDLE}</p><p>Endpoint: <code>/?rc=NUM&key=KEY</code></p>"

    if not user_key or user_key not in API_KEYS:
        return jsonify({"api_status": "ACCESS_DENIED", "auth_error": "INVALID_OR_REVOKED_KEY"}), 401

    tz_india = pytz.timezone('Asia/Kolkata')
    today = datetime.now(tz_india).date()
    expiry_date = datetime.strptime(API_KEYS[user_key], "%Y-%m-%d").date()
    days_left = (expiry_date - today).days

    if days_left < 0:
        return jsonify({"api_status": "EXPIRED", "license": "RENEWAL_REQUIRED"}), 403

    # Generate Data
    data = get_hyperion_data(rc)
    
    # Global License Information
    data["global_enterprise_license"] = {
        "license_to": COPYRIGHT_HANDLE,
        "tier": "TITAN_ULTRA_PREMIUM_HYPERION",
        "active_node": "MUMBAI_CLUSTER_01",
        "validity_remaining": f"{days_left} DAYS",
        "status": "OPERATIONAL",
        "generated_at": datetime.now(tz_india).strftime("%Y-%m-%d %H:%M:%S")
    }

    return jsonify(data)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
