import smtplib
import imaplib
import email as em
from email.mime.text import MIMEText

# Bước 1: Đọc thông tin đăng nhập
with open('email_credentials.txt', 'r', encoding='utf-8') as file:
    account_info = file.readlines()
    email_user = account_info[0].strip()
    app_password = account_info[1].strip()

# Bước 2: Đọc các file khác
with open('email_content.txt', 'r', encoding='utf-8') as file:
    email_content = file.read()

with open('recipient.txt', 'r', encoding='utf-8') as file:
    recipient_email = file.read().strip()

with open('email_filter.txt', 'r', encoding='utf-8') as file:
    filter_sender = file.read().strip()

# Bước 3: Gửi email
msg = MIMEText(email_content)
msg['Subject'] = 'Email tự động từ Python'
msg['From'] = email_user
msg['To'] = recipient_email

try:
    with smtplib.SMTP('smtp.gmail.com', 587) as server:
        server.starttls()
        server.login(email_user, app_password)
        server.send_message(msg)
        print("✅ Email đã gửi thành công!")
except Exception as e:
    print("Lỗi khi gửi email:", e)

# Bước 4: Nhận email
try:
    with imaplib.IMAP4_SSL('imap.gmail.com') as server:
        server.login(email_user, app_password)
        server.select('INBOX')
        _, data = server.search(None, f'FROM "{filter_sender}"')
        for num in data[0].split():
            _, msg_data = server.fetch(num, '(RFC822)')
            email_msg = em.message_from_bytes(msg_data[0][1])
            print("\n📩 [EMAIL NHẬN ĐƯỢC]")
            print("Tiêu đề:", email_msg['Subject'])
            if email_msg.is_multipart():
                for part in email_msg.walk():
                    if part.get_content_type() == 'text/plain':
                        print("Nội dung:\n", part.get_payload(decode=True).decode())
            else:
                print("Nội dung:\n", email_msg.get_payload(decode=True).decode())
            break
except Exception as e:
    print("Lỗi khi nhận email:", e)

