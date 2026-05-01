"""
Module de traitement des paiements manuels GabJob
Reçoit les demandes du formulaire et notifie l'admin par email
"""

import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from datetime import datetime


EMAIL_SENDER = os.environ.get('EMAIL_SENDER', 'gabjob134@gmail.com')
EMAIL_PASSWORD = os.environ.get('EMAIL_PASSWORD', '')
EMAIL_ADMIN = os.environ.get('EMAIL_ADMIN', 'gabjob134@gmail.com')
SMTP_SERVER = 'smtp.gmail.com'
SMTP_PORT = 587


def notifier_paiement_manuel(data, capture_file=None):
    """
    Envoie un email à l'admin avec les détails du paiement
    
    Args:
        data: dict avec plan, amount, nom, telephone, email, mobile, reference, operateur, message
        capture_file: file object de la capture (optionnel)
    
    Returns:
        bool: True si envoyé
    """
    if not EMAIL_PASSWORD:
        print("[PAYMENT] ⚠️ EMAIL_PASSWORD non configuré")
        return False
    
    now = datetime.now().strftime('%d/%m/%Y à %H:%M:%S')
    operateur_emoji = {'airtel': '📱 Airtel Money', 'moov': '📱 Moov Money'}.get(data.get('operateur', ''), 'N/A')
    
    plan = data.get('plan', 'N/A')
    amount = int(data.get('amount', 0))
    nom = data.get('nom', 'N/A')
    tel = data.get('telephone', 'N/A')
    email_client = data.get('email', 'N/A')
    mobile = data.get('mobile', 'N/A')
    ref = data.get('reference', 'N/A')
    msg = data.get('message', '')
    
    # WhatsApp link pré-rempli pour activer
    import urllib.parse
    wa_msg = f"Bonjour {nom}, votre abonnement {plan} GabJob a été activé avec succès ! Connectez-vous sur https://gabjob.org pour profiter de vos avantages."
    tel_clean = tel.replace(' ', '').replace('+', '').replace('-', '')
    if not tel_clean.startswith('241'):
        tel_clean = '241' + tel_clean.lstrip('0')
    wa_link = f"https://wa.me/{tel_clean}?text={urllib.parse.quote(wa_msg)}"
    
    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
      <meta charset="UTF-8">
      <style>
        body {{ font-family: Arial, sans-serif; background: #f9fafb; margin: 0; padding: 20px; }}
        .container {{ max-width: 620px; margin: 0 auto; background: #fff; border-radius: 16px; overflow: hidden; box-shadow: 0 4px 24px rgba(0,0,0,0.08); }}
        .header {{ background: linear-gradient(135deg, #16a34a, #15803d); color: #fff; padding: 28px; text-align: center; }}
        .header h1 {{ margin: 0; font-size: 22px; font-weight: 800; }}
        .header .subtitle {{ font-size: 14px; opacity: 0.95; margin-top: 4px; }}
        .content {{ padding: 28px; }}
        .alert {{ background: #fef3c7; border: 2px solid #f59e0b; border-radius: 12px; padding: 16px; margin-bottom: 20px; text-align: center; }}
        .alert .label {{ font-size: 11px; text-transform: uppercase; color: #92400e; font-weight: 700; letter-spacing: 1px; margin-bottom: 6px; }}
        .alert .value {{ font-size: 14px; color: #78350f; font-weight: 700; }}
        .plan-box {{ background: linear-gradient(135deg, #fff7ed, #fff); border: 2px dashed #f97316; border-radius: 14px; padding: 18px; text-align: center; margin: 16px 0; }}
        .plan-name {{ font-size: 13px; color: #ea580c; text-transform: uppercase; letter-spacing: 1.5px; font-weight: 700; margin-bottom: 8px; }}
        .plan-amount {{ font-size: 38px; font-weight: 800; color: #f97316; }}
        .info-row {{ display: flex; justify-content: space-between; padding: 10px 0; border-bottom: 1px solid #e5e7eb; align-items: center; }}
        .info-row:last-child {{ border-bottom: none; }}
        .info-label {{ color: #6b7280; font-size: 13px; }}
        .info-value {{ color: #111827; font-weight: 600; font-size: 13px; word-break: break-word; text-align: right; max-width: 60%; }}
        .info-value.highlight {{ color: #ea580c; font-weight: 700; font-family: monospace; }}
        .actions {{ padding: 20px; background: #f9fafb; border-top: 1px solid #e5e7eb; }}
        .actions h3 {{ font-size: 14px; color: #111827; margin-bottom: 12px; text-transform: uppercase; letter-spacing: 0.5px; }}
        .btn {{ display: block; padding: 12px 16px; border-radius: 10px; text-align: center; font-weight: 700; font-size: 14px; text-decoration: none; margin-bottom: 8px; }}
        .btn-wa {{ background: #25d366; color: #fff !important; }}
        .btn-mail {{ background: #f97316; color: #fff !important; }}
        .checklist {{ background: #fff; border: 1px solid #e5e7eb; border-radius: 10px; padding: 14px; margin-top: 12px; }}
        .checklist ol {{ padding-left: 20px; font-size: 13px; color: #4b5563; line-height: 1.7; }}
        .footer {{ padding: 16px; text-align: center; font-size: 12px; color: #9ca3af; border-top: 1px solid #e5e7eb; }}
        .message-box {{ background: #eff6ff; border-left: 4px solid #3b82f6; padding: 12px; border-radius: 8px; margin-top: 12px; font-size: 13px; color: #1e40af; line-height: 1.5; }}
      </style>
    </head>
    <body>
      <div class="container">
        <div class="header">
          <h1>💰 Nouveau paiement reçu</h1>
          <div class="subtitle">Vérifier et activer l'abonnement</div>
        </div>
        
        <div class="content">
          <div class="alert">
            <div class="label">⚠️ Action requise</div>
            <div class="value">Vérifiez le paiement Mobile Money et activez le compte</div>
          </div>
          
          <div class="plan-box">
            <div class="plan-name">{plan}</div>
            <div class="plan-amount">{amount:,} FCFA</div>
          </div>
          
          <h3 style="font-size:13px;color:#6b7280;margin:20px 0 8px;text-transform:uppercase;letter-spacing:0.8px;">👤 Informations client</h3>
          <div class="info-row">
            <span class="info-label">Nom complet</span>
            <span class="info-value">{nom}</span>
          </div>
          <div class="info-row">
            <span class="info-label">📱 Téléphone</span>
            <span class="info-value">{tel}</span>
          </div>
          <div class="info-row">
            <span class="info-label">📧 Email</span>
            <span class="info-value">{email_client}</span>
          </div>
          
          <h3 style="font-size:13px;color:#6b7280;margin:20px 0 8px;text-transform:uppercase;letter-spacing:0.8px;">💳 Détails du paiement</h3>
          <div class="info-row">
            <span class="info-label">Opérateur</span>
            <span class="info-value">{operateur_emoji}</span>
          </div>
          <div class="info-row">
            <span class="info-label">Numéro payeur</span>
            <span class="info-value">{mobile}</span>
          </div>
          <div class="info-row">
            <span class="info-label">Référence transaction</span>
            <span class="info-value highlight">{ref}</span>
          </div>
          <div class="info-row">
            <span class="info-label">🕐 Reçu le</span>
            <span class="info-value">{now}</span>
          </div>
          
          {f'<div class="message-box"><strong>💬 Message du client :</strong><br>{msg}</div>' if msg else ''}
        </div>
        
        <div class="actions">
          <h3>✅ Étapes d'activation</h3>
          <div class="checklist">
            <ol>
              <li>Vérifier la transaction dans votre téléphone Airtel/Moov</li>
              <li>Activer le compte du client dans le dashboard admin</li>
              <li>Envoyer un message WhatsApp de confirmation au client</li>
            </ol>
          </div>
          
          <div style="margin-top:14px;">
            <a class="btn btn-wa" href="{wa_link}" target="_blank">💬 Confirmer au client par WhatsApp</a>
            <a class="btn btn-mail" href="https://gabjob.org/admin">🔧 Ouvrir dashboard admin</a>
          </div>
        </div>
        
        <div class="footer">
          GabJob - Notification automatique<br>
          Ne pas répondre à cet email
        </div>
      </div>
    </body>
    </html>
    """
    
    text = f"""
    NOUVEAU PAIEMENT GABJOB
    
    Plan : {plan}
    Montant : {amount:,} FCFA
    
    Client :
    - Nom : {nom}
    - Téléphone : {tel}
    - Email : {email_client}
    
    Paiement :
    - Opérateur : {operateur_emoji}
    - Numéro payeur : {mobile}
    - Référence : {ref}
    - Reçu le : {now}
    
    {f'Message : {msg}' if msg else ''}
    
    Actions :
    1. Vérifier la transaction dans votre téléphone
    2. Activer le compte dans le dashboard
    3. Confirmer par WhatsApp : {wa_link}
    """
    
    try:
        message = MIMEMultipart('mixed')
        message['Subject'] = f"💰 [GabJob] Paiement {amount:,} FCFA - {plan} - {nom}"
        message['From'] = f"GabJob Paiements <{EMAIL_SENDER}>"
        message['To'] = EMAIL_ADMIN
        
        # Body
        body = MIMEMultipart('alternative')
        body.attach(MIMEText(text, 'plain', 'utf-8'))
        body.attach(MIMEText(html, 'html', 'utf-8'))
        message.attach(body)
        
        # Capture en pièce jointe si fournie
        if capture_file:
            try:
                capture_data = capture_file.read()
                part = MIMEBase('application', 'octet-stream')
                part.set_payload(capture_data)
                encoders.encode_base64(part)
                filename = capture_file.filename if hasattr(capture_file, 'filename') else 'capture.png'
                part.add_header('Content-Disposition', f'attachment; filename="{filename}"')
                message.attach(part)
            except Exception as e:
                print(f"[PAYMENT] ⚠️ Erreur attachement capture : {e}")
        
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(EMAIL_SENDER, EMAIL_PASSWORD)
            server.send_message(message)
        
        print(f"[PAYMENT] ✅ Email envoyé à {EMAIL_ADMIN} pour paiement {amount} FCFA - {nom}")
        return True
        
    except Exception as e:
        print(f"[PAYMENT] ❌ Erreur : {e}")
        return False
