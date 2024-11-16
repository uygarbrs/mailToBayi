from flask import Flask, request, jsonify, send_file
import os
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.colors import blue, black
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders

app = Flask(__name__)


# E-posta gönderme fonksiyonu
def send_email(pdf_path, recipient_email):
    sender_email = "uygarb00@gmail.com"  # Gönderen e-posta adresi
    sender_password = "vlvp vvwj khzb xnas"  # E-posta şifresi (Gmail için uygulama parolası kullanabilirsiniz)

    # E-posta içeriği
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = recipient_email
    msg['Subject'] = 'Webhook Verisi PDF Dosyası'

    # PDF dosyasını ekle
    with open(pdf_path, "rb") as attachment:
        part = MIMEBase('application', 'octet-stream')
        part.set_payload(attachment.read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', f"attachment; filename={os.path.basename(pdf_path)}")
        msg.attach(part)

    try:
        # SMTP sunucusuna bağlan
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(sender_email, sender_password)  # Giriş yap
            text = msg.as_string()  # Mesajı string formatına çevir
            server.sendmail(sender_email, recipient_email, text)  # E-posta gönder
            print("E-posta başarıyla gönderildi.")
    except Exception as e:
        print(f"E-posta gönderme hatası: {e}")


# PDF oluşturma fonksiyonu
def create_pdf(questions, answers, filename):
    c = canvas.Canvas(filename, pagesize=letter)
    width, height = letter  # Sayfa boyutu

    # Başlık
    c.setFont("Helvetica", 16)
    c.drawString(100, height - 50, "Webhook Verileri")

    # Veriyi yazdırma
    y_position = height - 100
    for question, answer in zip(questions, answers):
        if 't' in answer:
            c.setFont("Helvetica", 12)
            c.setFillColor(black)
            c.drawString(100, y_position, f"{question['question']}: {answer['t']}")
            y_position -= 20
        elif 'c' in answer:
            choice = answer['c'][0]['t']
            c.setFont("Helvetica", 12)
            c.setFillColor(black)
            c.drawString(100, y_position, f"{question['question']}: {choice}")
            y_position -= 20
        elif 'f' in answer:
            download_url = answer['urls'][0]['downloadUrl']
            photo_label = question['question']  # Foto etiketini oluşturuyoruz

            c.setFont("Helvetica", 12)
            c.setFillColor(blue)
            text_width = c.stringWidth(photo_label)  # Metnin genişliğini alıyoruz
            c.drawString(100, y_position, photo_label)

            # Alt çizgi ekleme
            underline_y = y_position - 2
            c.setStrokeColor(blue)
            c.line(100, underline_y, 100 + text_width, underline_y)

            # Metnin üzerine tıklanabilir bağlantı ekliyoruz
            link_x_start = 100
            link_x_end = link_x_start + text_width
            c.linkURL(download_url, (link_x_start, y_position - 2, link_x_end, y_position + 10), relative=0)

            y_position -= 20

    c.save()


# Webhook URL'sine bir POST isteği geldiğinde çalışacak route
@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.json  # Gelen form verisini JSON formatında alıyoruz
    if data:
        print(data)
        questions = data['form']['questions']
        answers = [item for item in data['answer']['answers']]

        pdf_path = "/tmp/response.pdf"
        create_pdf(questions, answers, pdf_path)

        # Send mail
        recipient_email = "uygar.hatipoglu@sabanciuniv.edu"  # Alıcı e-posta adresi
        send_email(pdf_path, recipient_email)

        if os.path.exists(pdf_path):
            print(f"PDF dosyası başarıyla oluşturuldu: {pdf_path}")
        else:
            print("PDF dosyası oluşturulamadı!")

        # PDF dosyasını istemciye gönderiyoruz
        return send_file(pdf_path, as_attachment=False, mimetype='application/pdf')
    else:
        return {"result": "AN ERROR OCCURRED"}


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))  # Railway otomatik olarak PORT ayarlar
    app.run(host="0.0.0.0", port=port, debug=True)
