from flask import Flask, request, jsonify
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

app = Flask(__name__)


# Webhook URL'sine bir POST isteği geldiğinde çalışacak route
@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.json  # Gelen form verisini JSON formatında alıyoruz
    if data:
        print(data)
    else:
        print(".....................")


# E-posta gönderme fonksiyonu
def send_email(to_address, form_data):
    from_address = "sizin_mail_adresiniz@example.com"
    password = "sifre"

    # E-posta başlığı ve içeriği
    subject = "Yeni Form Yanıtı"
    body = f"Yeni bir form yanıtı aldınız:\n\n{form_data}"

    # SMTP üzerinden e-posta gönderme
    msg = MIMEMultipart()
    msg['From'] = from_address
    msg['To'] = to_address
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    try:
        server = smtplib.SMTP('smtp.example.com', 587)  # SMTP sunucusunun ayarlarını ekleyin
        server.starttls()
        server.login(from_address, password)
        text = msg.as_string()
        server.sendmail(from_address, to_address, text)
        server.quit()
        print("E-posta başarıyla gönderildi")
    except Exception as e:
        print(f"E-posta gönderim hatası: {e}")


if __name__ == '__main__':
    app.run(port=5000)
