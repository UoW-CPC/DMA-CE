import binascii

import requests
from flask import Blueprint
from flask_restful import Api, Resource, reqparse

from apps.utils.crypto import SymmetricEncryption, H2_hash_function

CE_bp = Blueprint('CE', __name__, url_prefix='/ce')
api = Api(CE_bp)

class CESecureCommunicatewithMHApi(Resource):
    def get(self):
        pass

    def post(self):
        # 4. CE starts the conversation with MH.
        payload = {
            "status": 200,
            "msg": "CE starts the conversation with MH.",
            "Flag": "0",
            "DMi": 100
        }
        # CE sends a POST to MH and then will receive the response from MH.
        MH_response = requests.post(' http://127.0.0.1:5001/mh/MH2CE', data=payload)

        # CE receives the response from MH and get the c2 from MH.
        # Next, CE will decrypt c2 as m2 and then will execute the Message Integrity Check.
        # If Message Integrity Check is ok, CE returns r1 and t2 back to MH. If not, Auth is failed.
        c2 = MH_response.json().get('c2')
        c2 = binascii.unhexlify(c2.encode('utf-8'))

        # passwordSalt_value, iv_value and nonce should be received from EMGWAM. Please replace them.
        passwordSalt_value = b'a#\xa1\xbe\r\xe4^\x06,a\xeeZ\x91\xfc\xf3j'
        iv_value = 90603373939604955465082505548528970619254170524234007075663211789259246989110
        nonce = 'ymNIaotdN3EQPMHpl+gZTkhYNQqGu7eHUG+MBAIbfOE='

        # CE decrypts c2 as m2 using encryptor
        encryptor = SymmetricEncryption(passwordSalt_value, iv_value)
        m2 = encryptor.decryption(c2, nonce).decode('utf-8')
        # m2 = str(r1) + ' ' + str(t2) + ' ' + str(DMi) + ' ' + H2
        m2_list = m2.split(' ')
        # r1
        r1 = m2_list[0]
        # t2
        t2_date = m2_list[1]
        t2_time = m2_list[2]
        t2 = t2_date + ' ' + t2_time
        # DMi
        DMi = m2_list[-2]
        # H2
        H2 = m2_list[-1]

        temp = r1 + t2 + DMi
        res = H2_hash_function(temp)

        # Message Integrity Check
        if res == H2:
            payload = {
                "status": 200,
                "r1_from_CE": r1,
                "t2_from_CE": t2,
                "Flag": "1"
            }
            # 6. CE sends (r1, t2) to MH
            MH_response = requests.post(' http://127.0.0.1:5001/mh/MH2CE', data=payload)
            return MH_response.json()
        else:
            data = {
                "status": 400,
                "msg": "Auth is failed."
            }
            return data

api.add_resource(CESecureCommunicatewithMHApi, '/CE2MH')