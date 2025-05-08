from flask import Flask, request, jsonify
import curl_cffi.requests as requests

app = Flask(__name__)

EMAIL = "hkedia@dimagi-associate.com"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Accept": "application/json,text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
    "Referer": "https://www.expensify.com/",
    "Connection": "keep-alive",
}

@app.route('/request-otp', methods=['GET'])
def request_otp():
    url = f"https://www.expensify.com/api?command=ResendValidateCode&email={EMAIL}&api_setcookie=false"
    with requests.Session(impersonate="chrome110") as session:
        response = session.get(url, headers=headers)
    return jsonify({"message": response.text})

@app.route('/get-auth-token', methods=['POST'])
def get_auth_token():
    otp = request.json.get('otp')
    url = f"https://www.expensify.com/api?command=SignIn&email={EMAIL}&validateCode={otp}"
    with requests.Session(impersonate="chrome110") as session:
        response = session.get(url, headers=headers)
    return jsonify(response.json())

if __name__ == '__main__':
    app.run(debug=True) 