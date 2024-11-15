from flask import Flask, request, jsonify
import os

app = Flask(__name__)


# Webhook URL'sine bir POST isteği geldiğinde çalışacak route
@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.json  # Gelen form verisini JSON formatında alıyoruz
    if data:
        #answers = data['form']['answers']
        print(data)
    else:
        print(".....................")
    return {"result": "deneme"}



if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))  # Railway otomatik olarak PORT ayarlar
    app.run(host="0.0.0.0", port=port, debug=True)
