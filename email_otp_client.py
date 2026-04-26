"""
Module d'envoi OTP par email AU CLIENT (pas à l'admin)
Utilisé en remplacement du SMS quand Africa's Talking n'est pas chargé
"""

import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


# Configuration depuis .env
EMAIL_SENDER = os.environ.get('EMAIL_SENDER', 'gabjob134@gmail.com')
EMAIL_PASSWORD = os.environ.get('EMAIL_PASSWORD', '')
SMTP_SERVER = 'smtp.gmail.com'
SMTP_PORT = 587


def send_otp_to_client(client_email, code, prenom='Cher utilisateur'):
    """
    Envoie le code OTP directement au client par email
    
    Args:
        client_email: Email du client
        code: Code OTP à 6 chiffres
        prenom: Prénom du client (optionnel)
    
    Returns:
        bool: True si envoyé, False sinon
    """
    print(f"[OTP EMAIL] 📧 Envoi du code {code} à {client_email}")
    
    if not EMAIL_PASSWORD:
        print("[OTP EMAIL] ⚠️ EMAIL_PASSWORD non configuré")
        return False
    
    if not client_email or '@' not in client_email:
        print(f"[OTP EMAIL] ❌ Email invalide : {client_email}")
        return False
    
    # Email HTML pro
    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
      <meta charset="UTF-8">
      <style>
        body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Arial, sans-serif; background: #f9fafb; margin: 0; padding: 20px; }}
        .container {{ max-width: 480px; margin: 0 auto; background: #fff; border-radius: 16px; overflow: hidden; box-shadow: 0 4px 24px rgba(0,0,0,0.08); }}
        .header {{ background: linear-gradient(135deg, #f97316, #ea580c); color: #fff; padding: 32px 24px; text-align: center; }}
        .header h1 {{ margin: 0; font-size: 26px; font-weight: 800; letter-spacing: -1px; }}
        .header h1 span {{ color: #fff; opacity: 0.95; }}
        .header .subtitle {{ font-size: 14px; opacity: 0.9; margin-top: 6px; font-weight: 500; }}
        .content {{ padding: 32px 28px; }}
        .greeting {{ font-size: 16px; color: #111827; margin-bottom: 16px; }}
        .message {{ font-size: 14px; color: #4b5563; line-height: 1.6; margin-bottom: 24px; }}
        .code-box {{ background: linear-gradient(135deg, #fff7ed, #fff); border: 3px dashed #f97316; border-radius: 14px; padding: 24px; text-align: center; margin: 24px 0; }}
        .code-label {{ font-size: 12px; color: #ea580c; text-transform: uppercase; letter-spacing: 2px; font-weight: 700; margin-bottom: 8px; }}
        .code {{ font-size: 42px; font-weight: 800; color: #f97316; letter-spacing: 8px; font-family: 'Courier New', monospace; }}
        .info {{ background: #fef3c7; border-left: 4px solid #f59e0b; padding: 14px 16px; border-radius: 8px; font-size: 13px; color: #92400e; line-height: 1.5; margin: 20px 0; }}
        .footer {{ background: #f9fafb; padding: 20px; text-align: center; font-size: 12px; color: #6b7280; line-height: 1.6; }}
        .footer a {{ color: #f97316; text-decoration: none; font-weight: 600; }}
      </style>
    </head>
    <body>
      <div class="container">
        <div class="header">
          <h1>Gab<span>Job</span></h1>
          <div class="subtitle">🔐 Code de vérification</div>
        </div>
        
        <div class="content">
          <div class="greeting">Bonjour {prenom} 👋</div>
          
          <div class="message">
            Vous avez demandé un code de vérification pour vous connecter à votre compte GabJob. 
            Voici votre code :
          </div>
          
          <div class="code-box">
            <div class="code-label">Votre code</div>
            <div class="code">{code}</div>
          </div>
          
          <div class="info">
            ⏱️ <strong>Ce code expire dans 10 minutes.</strong><br>
            🔒 Ne partagez ce code avec personne, même pas avec un employé GabJob.
          </div>
          
          <div class="message" style="margin-top: 24px; font-size: 13px; color: #6b7280;">
            Si vous n'avez pas demandé ce code, vous pouvez ignorer cet email en toute sécurité.
          </div>
        </div>
        
        <div class="footer">
          <strong>GabJob</strong> — La plateforme N°1 d'emploi au Gabon 🇬🇦<br>
          <a href="https://gabjob.org">gabjob.org</a> · 
          <a href="https://gabjob.org/contact">Contact</a>
        </div>
      </div>
    </body>
    </html>
    """
    
    text = f"""
    GabJob - Code de vérification
    
    Bonjour {prenom},
    
    Votre code de vérification GabJob est : {code}
    
    Ce code expire dans 10 minutes. Ne le partagez avec personne.
    
    Si vous n'avez pas demandé ce code, ignorez cet email.
    
    --
    GabJob - https://gabjob.org
    """
    
    try:
        message = MIMEMultipart('alternative')
        message['Subject'] = f"🔐 Votre code GabJob : {code}"
        message['From'] = f"GabJob <{EMAIL_SENDER}>"
        message['To'] = client_email
        
        message.attach(MIMEText(text, 'plain', 'utf-8'))
        message.attach(MIMEText(html, 'html', 'utf-8'))
        
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(EMAIL_SENDER, EMAIL_PASSWORD)
            server.send_message(message)
        
        print(f"[OTP EMAIL] ✅ Code envoyé à {client_email}")
        return True
        
    except Exception as e:
        print(f"[OTP EMAIL] ❌ Erreur : {e}")
        return False


# Test
if __name__ == '__main__':
    from dotenv import load_dotenv
    load_dotenv()
    EMAIL_PASSWORD = os.environ.get('EMAIL_PASSWORD', '')
    print("Test envoi OTP par email...")
    result = send_otp_to_client('test@example.com', '123456', 'Abdel')
    print("✅ Succès" if result else "❌ Échec")
