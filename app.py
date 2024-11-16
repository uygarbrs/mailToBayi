from flask import Flask, request, jsonify, send_file
import os
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.colors import blue
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders

app = Flask(__name__)


# E-posta gönderme fonksiyonu

# Webhook URL'sine bir POST isteği geldiğinde çalışacak route
@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.json  # Gelen form verisini JSON formatında alıyoruz
    if data:
        print(data)
    else:
        print("aaaaaaaaaa")


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))  # Railway otomatik olarak PORT ayarlar
    app.run(host="0.0.0.0", port=port, debug=True)
