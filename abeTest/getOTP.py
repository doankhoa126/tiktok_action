import imaplib
import email
from email.header import decode_header
import re

def verifiedTiktok(username, password):
    # Kết nối tới máy chủ IMAP của Hotmail
    mail = imaplib.IMAP4_SSL("imap-mail.outlook.com")

    try:
        # Đăng nhập
        mail.login(username, password)
    except imaplib.IMAP4.error as e:
        print(f"Login failed: {e}")
        return None

    try:
        # Chọn hộp thư bạn muốn đọc (INBOX, Spam, v.v.)
        status, messages = mail.select("inbox")
        
        if status != "OK":
            print(f"Failed to select mailbox: {status}")
            mail.logout()
            return None

        # Tìm tất cả email trong hộp thư
        status, messages = mail.search(None, "ALL")

        # Kiểm tra xem có email không
        if status != "OK":
            print("No messages found!")
            mail.logout()
            return None

        # Lấy danh sách id email
        email_ids = messages[0].split()

        # Đọc email mới nhất trước (đảo ngược danh sách)
        for email_id in reversed(email_ids):
            status, msg_data = mail.fetch(email_id, "(RFC822)")
            for response_part in msg_data:
                if isinstance(response_part, tuple):
                    msg = email.message_from_bytes(response_part[1])
                    subject, encoding = decode_header(msg["Subject"])[0]
                    if isinstance(subject, bytes):
                        subject = subject.decode(encoding if encoding else "utf-8")
                    from_ = msg.get("From")
                    print(f"Subject: {subject}")
                    print(f"From: {from_}")

                    # Nếu email có phần nội dung
                    if msg.is_multipart():
                        for part in msg.walk():
                            content_type = part.get_content_type()
                            content_disposition = str(part.get("Content-Disposition"))

                            try:
                                body = part.get_payload(decode=True).decode()
                            except:
                                body = None

                            if content_type == "text/plain" and "attachment" not in content_disposition:
                                print(f"Text body: {body}")
                            elif content_type == "text/html" and "attachment" not in content_disposition:
                                print(f"HTML body: {body}")
                                if body:
                                    verification_code = re.search(r"\b\d{6}\b", body)
                                    if verification_code:
                                        print(f"Verification Code: {verification_code.group(0)}")
                                        mail.logout()
                                        return verification_code.group(0)
                    else:
                        body = msg.get_payload(decode=True).decode()
                        print(f"Single part body: {body}")
                        if body:
                            verification_code = re.search(r"\b\d{6}\b", body)
                            if verification_code:
                                print(f"Verification Code: {verification_code.group(0)}")
                                mail.logout()
                                return verification_code.group(0)
        mail.logout()
    except imaplib.IMAP4.error as e:
        print(f"IMAP error occurred: {e}")
        mail.logout()
        return None
    except Exception as e:
        print(f"An error occurred: {e}")
        mail.logout()
        return None

# Example usage
username = 'galindez7us@hotmail.com'
password = 'GWvPTboy4DF1'
verified_code = verifiedTiktok(username, password)
print(f"Verified Code: {verified_code}")
