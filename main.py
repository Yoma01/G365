import requests
from flask import json, render_template
from flask import request
from flask import Flask

app = Flask(__name__)


@app.route('/', methods=["GET", "POST"])
def api_root():
    return 'Home'
    data = request.json
    #print(data["data"]["id"])

    if data["action"] == "newReservation" or data["action"] == "updateReservation":
        trigger_info = {
            'action': data["action"],
            'res_id': data["data"]["id"]
        }
    elif data["action"] == "onlineCheckInUpdate":
        trigger_info = {
            'action': data["action"],
            'res_id': data["data"]["bookingId"]
        }
    else:
        return

    #print(trigger_info['res_id'])
    reservation_id = trigger_info['res_id']
    reservation_action = trigger_info['action']
    url = "https://login.smoobu.com/api/reservations/" + str(reservation_id) + "/placeholders"

    headers = {
        "Api-Key": "Q.iQytYFuq_mFizDvoW~Q0ZIwsWc51LZ",
        "Cache-Control": "no-cache",
    }

    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        print("Request was successful")
        print("Response content:")
        igloo_body = response.json()
        igloo_body2 = igloo_body['placeholders']
        # print(igloo_body2)
        igloo_body3 = igloo_body2[28]
        print(igloo_body3)
        igloo_code = igloo_body3['value']
        print(igloo_body3['value'])
        val_dict = {
            "action": reservation_action,
            "id": reservation_id,
            "igloo_code": igloo_code
        }
        with open('push.txt', 'a') as push_file:
            push_file.write(json.dumps(val_dict))
            push_file.write('\n')

    else:
        print(f"Request failed with status code {response.status_code}")

    
    #print(request.data)



    return 'Home page'




if __name__ == '__main__':
    app.run(host="127.0.0.1", port=8080, debug=True)
