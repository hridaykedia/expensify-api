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

@app.route("/update-transaction", methods=["POST"])
def update_transaction_route():
    data = request.json
    required_fields = ["amount", "category", "tag", "comment", "reimbursable", "billable", "transactionID", "auth_token"]
    
    # Ensure all required keys are present (even if empty)
    if not all(field in data for field in required_fields):
        return jsonify({"error": "Missing one or more required fields"}), 400

    url = (
        f"https://www.expensify.com/api?command=UpdateTransaction"
        f"&authToken={data['auth_token']}"
        f"&transactionID={data['transactionID']}"
        f"&amount={data['amount']}"
        f"&category={data['category']}"
        f"&tag={data['tag']}"
        f"&comment={data['comment']}"
        f"&reimbursable={str(data['reimbursable']).lower()}"
        f"&billable={str(data['billable']).lower()}"
    )

    with requests.Session(impersonate="chrome110") as session:
        response = session.get(url, headers=headers)

    return jsonify({"response": response.text})

@app.route("/get-report-details", methods=["POST"])
def get_report_details_route():
    data = request.json
    report_id = data.get("reportId")
    auth_token = data.get("auth_token")
    if not report_id:
        return jsonify({"error": "Missing 'reportId' in request"}), 400

    url = (
        f"https://www.expensify.com/api/Get?returnValueList=reportStuff"
        f"&reportIDList={report_id}&shouldLoadOptionalKeys=false&pageName=report"
    )

    cookies = {
        "authToken": auth_token
    }

    with requests.Session(impersonate="chrome110") as session:
        response = session.get(url, headers=headers, cookies=cookies)
        data = response.json()

    return jsonify({
        "status": response.status_code,
        "transactions": data['reports'][report_id]['transactionList']
    })


if __name__ == '__main__':
    app.run(debug=True) 