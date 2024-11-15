from flask import Flask, request, jsonify

app = Flask(__name__)


# Webhook URL'sine bir POST isteği geldiğinde çalışacak route
@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.json  # Gelen form verisini JSON formatında alıyoruz
    if data:
        print(data)
    else:
        print(".....................")



if __name__ == '__main__':
    app.run(port=5000)
