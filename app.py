from flask import Flask, request, jsonify
from otp.main_otp import OTP
from otp.dto import RequestOtpSchema, ValidateOtpSchema
from datetime import datetime, timedelta
from database import conf
import logging

app = Flask(__name__)
otp = OTP()

@app.route('/', methods=['GET'])
def index():
    return "Hello World!"

@app.route('/request', methods=['POST'])
def request_otp():
    request_otp_data = RequestOtpSchema(**request.json)

    # Sama seperti sebelumnya, aku mengommentari bagian ini:
    # ... 

    response = otp.send_otp_request(phone=request_otp_data.phone_number)
    current_time = datetime.now()
    expiry_time = current_time + timedelta(minutes=3)

    query = """
    INSERT INTO tb_otp_transaction (
        otp_id, merchant_id, provider_id, type, pic_id, otp, timestamp, purpose, latitude, 
        longitude, device_name, os_version, manufacturer, cpu_info, platform, ip, 
        is_active, expired_at, created_at
    ) VALUES (
        :otp_id, :merchant_id, :provider_id, :type, :pic_id, :otp, :timestamp, :purpose, 
        :latitude, :longitude, :device_name, :os_version, :manufacturer, :cpu_info, 
        :platform, :ip, :is_active, :expired_at, :created_at
    )
    """

    values = {
        # ... (sama seperti kode sebelumnya)
    }

    conf.database.execute(query, values)
    
    return jsonify(response)

@app.route('/verify', methods=['POST'])
def verify_otp():
    validate_otp_data = ValidateOtpSchema(**request.json)
    
    response = otp.send_otp_verify(otp=validate_otp_data.otp, otp_id=validate_otp_data.otp_id)

    if response["status"] == True:
        current_time = datetime.now()
        query = """
        UPDATE tb_otp_transaction
        SET is_active = :is_active, updated_at = :updated_at
        WHERE otp_id = :otp_id
        """

        values = {
            "otp_id": validate_otp_data.otp_id,
            "is_active": False,
            "updated_at": current_time
        }

        conf.database.execute(query, values)
        
    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True)
