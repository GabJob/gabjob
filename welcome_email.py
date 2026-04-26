"""
Module d'email de bienvenue automatique pour GabJob
Envoie un email personnalisé selon le type d'utilisateur (candidat/recruteur/technicien)
"""

import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


EMAIL_SENDER = os.environ.get('EMAIL_SENDER', 'gabjob134@gmail.com')
EMAIL_PASSWORD = os.environ.get('EMAIL_PASSWORD', '')
SMTP_SERVER = 'smtp.gmail.com'
SMTP_PORT = 587


# ═══════════════════════════════════════════════════
# TEMPLATES PAR TYPE D'UTILISATEUR
# ═══════════════════════════════════════════════════

TEMPLATES = {
    'candidat': {
        'subject': '🎉 Bienvenue sur GabJob, {prenom} !',
        'title': 'Bienvenue dans la communauté !',
        'emoji': '👤',
        'intro': "Vous venez de rejoindre GabJob, la plateforme N°1 d'emploi au Gabon. Des milliers d'opportunités s'ouvrent à vous !",
        'tips': [
            ('📝', 'Complétez votre profil', 'Un profil complet attire 5x plus de recruteurs. Ajoutez vos compétences, expériences et formations.'),
            ('📄', 'Créez votre CV pro', 'Utilisez notre générateur de CV niveau Canva pour vous démarquer (10 000 FCFA - paiement unique).'),
            ('🔔', 'Activez les notifications', 'Soyez alerté dès qu\'une offre correspondant à votre profil est publiée.'),
        ],
        'premium_title': '⭐ Passez à Candidat Premium',
        'premium_price': '5 000 FCFA / mois',
        'premium_benefits': [
            'Profil mis en avant en tête des résultats',
            'Voir qui consulte votre profil',
            'Recommandation prioritaire aux recruteurs',
            'Statistiques détaillées de votre profil',
            'Badge Premium ⭐ sur votre profil',
        ],
        'cta_text': 'Compléter mon profil',
        'cta_url': 'https://gabjob.org/dashboard',
    },
    'recruteur': {
        'subject': '🏢 Bienvenue sur GabJob Recruteur, {prenom} !',
        'title': 'Bienvenue, recruteur !',
        'emoji': '🏢',
        'intro': "Vous avez désormais accès à la plus grande base de candidats vérifiés du Gabon. Trouvez vos talents en quelques clics !",
        'tips': [
            ('🔍', 'Explorez la base candidats', 'Filtrez par compétence, ville, expérience. Vous trouverez forcément la perle rare.'),
            ('📋', 'Publiez votre première offre', 'Une annonce bien rédigée reçoit en moyenne 25 candidatures qualifiées.'),
            ('💬', 'Contactez via WhatsApp', 'Les meilleurs candidats répondent vite. Initiez la conversation directement.'),
        ],
        'premium_title': '🚀 Passez à Recruteur Pro',
        'premium_price': '120 000 FCFA / an',
        'premium_benefits': [
            'Accès illimité à la base candidats',
            'Publication d\'offres illimitée',
            'Filtres avancés par compétence',
            'Contact WhatsApp direct',
            'Statistiques de performance',
            'Support prioritaire',
        ],
        'cta_text': 'Accéder au dashboard',
        'cta_url': 'https://gabjob.org/dashboard-recruteur',
    },
    'technicien': {
        'subject': '🔧 Bienvenue sur GabJob Dépannage, {prenom} !',
        'title': 'Bienvenue, technicien !',
        'emoji': '🔧',
        'intro': "Vous rejoignez le réseau GabJob de techniciens vérifiés au Gabon. De nouveaux clients vous attendent !",
        'tips': [
            ('📷', 'Ajoutez vos réalisations', 'Photos et vidéos de vos travaux augmentent vos chances de 3x.'),
            ('📍', 'Définissez votre zone', 'Indiquez vos quartiers d\'intervention pour recevoir les bonnes demandes.'),
            ('⭐', 'Collectez des avis', 'Demandez à vos clients satisfaits de laisser un avis sur votre profil.'),
        ],
        'premium_title': '⚡ Activez votre abonnement Technicien',
        'premium_price': '10 000 FCFA / mois',
        'premium_benefits': [
            'Visibilité maximale sur les recherches',
            'Demandes de devis illimitées',
            'Profil mis en avant par catégorie',
            'Badge "Technicien Vérifié" 🛡️',
            'Notifications instantanées de nouvelles demandes',
        ],
        'cta_text': 'Compléter mon profil technicien',
        'cta_url': 'https://gabjob.org/depannage',
    },
}


def send_welcome_email(client_email, prenom, nom, type_user='candidat'):
    """
    Envoie un email de bienvenue personnalisé selon le type d'utilisateur
    
    Args:
        client_email: Email du nouveau client
        prenom: Prénom
        nom: Nom
        type_user: 'candidat', 'recruteur' ou 'technicien'
    
    Returns:
        bool: True si envoyé, False sinon
    """
    print(f"[WELCOME EMAIL] 📧 Envoi à {client_email} (type: {type_user})")
    
    if not EMAIL_PASSWORD:
        print("[WELCOME EMAIL] ⚠️ EMAIL_PASSWORD non configuré (mode DEV)")
        return False
    
    if not client_email or '@' not in client_email:
        print(f"[WELCOME EMAIL] ❌ Email invalide : {client_email}")
        return False
    
    # Sélectionner le template
    template = TEMPLATES.get(type_user, TEMPLATES['candidat'])
    
    # Construire le HTML
    tips_html = ''.join([
        f'''
        <div class="tip">
          <div class="tip-icon">{icon}</div>
          <div class="tip-content">
            <div class="tip-title">{title}</div>
            <div class="tip-desc">{desc}</div>
          </div>
        </div>
        ''' for (icon, title, desc) in template['tips']
    ])
    
    benefits_html = ''.join([
        f'<li>{b}</li>' for b in template['premium_benefits']
    ])
    
    prenom_safe = prenom or 'Cher utilisateur'
    
    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
      <meta charset="UTF-8">
      <style>
        body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Arial, sans-serif; background: #f9fafb; margin: 0; padding: 20px; color: #111827; }}
        .container {{ max-width: 560px; margin: 0 auto; background: #fff; border-radius: 18px; overflow: hidden; box-shadow: 0 8px 32px rgba(0,0,0,0.08); }}
        .header {{ background: linear-gradient(135deg, #f97316, #ea580c); color: #fff; padding: 36px 28px; text-align: center; }}
        .header .emoji {{ font-size: 48px; margin-bottom: 8px; }}
        .header h1 {{ margin: 0; font-size: 26px; font-weight: 800; letter-spacing: -1px; }}
        .header h1 span {{ opacity: 0.95; }}
        .header .title {{ font-size: 18px; opacity: 0.95; margin-top: 8px; font-weight: 600; }}
        .content {{ padding: 32px 28px; }}
        .greeting {{ font-size: 18px; color: #111827; margin-bottom: 12px; font-weight: 600; }}
        .intro {{ font-size: 14px; color: #4b5563; line-height: 1.7; margin-bottom: 28px; }}
        .section-title {{ font-size: 12px; text-transform: uppercase; letter-spacing: 1.5px; color: #f97316; font-weight: 800; margin: 28px 0 16px; padding-bottom: 8px; border-bottom: 2px solid #fed7aa; }}
        .tip {{ display: flex; gap: 14px; align-items: flex-start; padding: 14px; background: #f9fafb; border-radius: 12px; margin-bottom: 10px; }}
        .tip-icon {{ font-size: 24px; flex-shrink: 0; }}
        .tip-title {{ font-weight: 700; font-size: 14px; margin-bottom: 4px; }}
        .tip-desc {{ font-size: 13px; color: #6b7280; line-height: 1.5; }}
        .premium-box {{ background: linear-gradient(135deg, #fff7ed, #fff); border: 2px dashed #f97316; border-radius: 14px; padding: 20px; margin: 24px 0; }}
        .premium-title {{ font-size: 18px; font-weight: 800; color: #111827; margin-bottom: 6px; }}
        .premium-price {{ font-size: 24px; font-weight: 800; color: #f97316; margin-bottom: 14px; }}
        .premium-benefits {{ list-style: none; padding: 0; margin: 0 0 16px 0; }}
        .premium-benefits li {{ padding: 6px 0; font-size: 13px; color: #4b5563; }}
        .premium-benefits li::before {{ content: '✅ '; }}
        .cta-btn {{ display: block; background: linear-gradient(135deg, #f97316, #ea580c); color: #fff !important; text-decoration: none; padding: 14px 24px; border-radius: 10px; text-align: center; font-weight: 700; font-size: 15px; margin: 16px 0; }}
        .cta-btn-outline {{ display: block; background: #fff; color: #f97316 !important; text-decoration: none; padding: 12px 24px; border: 2px solid #f97316; border-radius: 10px; text-align: center; font-weight: 700; font-size: 14px; margin: 8px 0; }}
        .footer {{ background: #f9fafb; padding: 20px; text-align: center; font-size: 12px; color: #6b7280; line-height: 1.6; border-top: 1px solid #e5e7eb; }}
        .footer a {{ color: #f97316; text-decoration: none; font-weight: 600; }}
        .help {{ background: #eff6ff; border-radius: 10px; padding: 14px; font-size: 13px; color: #1e40af; margin-top: 20px; line-height: 1.5; }}
      </style>
    </head>
    <body>
      <div class="container">
        <div class="header">
          <div class="emoji">{template['emoji']}</div>
          <h1>Gab<span>Job</span></h1>
          <div class="title">{template['title']}</div>
        </div>
        
        <div class="content">
          <div class="greeting">Bonjour {prenom_safe} 👋</div>
          
          <div class="intro">
            {template['intro']}
          </div>
          
          <div class="section-title">🚀 Pour bien démarrer</div>
          {tips_html}
          
          <a class="cta-btn" href="{template['cta_url']}">{template['cta_text']} →</a>
          
          <div class="premium-box">
            <div class="premium-title">{template['premium_title']}</div>
            <div class="premium-price">{template['premium_price']}</div>
            <ul class="premium-benefits">
              {benefits_html}
            </ul>
            <a class="cta-btn-outline" href="https://wa.me/24107402946700?text=Bonjour%20GabJob%2C%20je%20veux%20activer%20mon%20abonnement%20Premium">💬 Activer via WhatsApp</a>
          </div>
          
          <div class="help">
            💡 <strong>Une question ?</strong> Notre équipe est là pour vous aider. 
            Contactez-nous sur WhatsApp au +241 074 02 94 67 ou via la page <a href="https://gabjob.org/contact" style="color:#1e40af;">Contact</a>.
          </div>
        </div>
        
        <div class="footer">
          <strong>GabJob</strong> — La plateforme N°1 d'emploi au Gabon 🇬🇦<br>
          <a href="https://gabjob.org">gabjob.org</a> · 
          <a href="https://gabjob.org/about">À propos</a> · 
          <a href="https://gabjob.org/contact">Contact</a><br>
          <span style="font-size:11px;opacity:0.7;margin-top:8px;display:inline-block;">Vous recevez cet email car vous venez de créer un compte sur GabJob.</span>
        </div>
      </div>
    </body>
    </html>
    """
    
    text = f"""
    Bienvenue sur GabJob, {prenom_safe} !
    
    {template['intro']}
    
    Pour bien démarrer :
    """ + '\n'.join([f"- {title} : {desc}" for (icon, title, desc) in template['tips']]) + f"""
    
    Accédez à votre espace : {template['cta_url']}
    
    {template['premium_title']} - {template['premium_price']}
    Pour activer : WhatsApp +241 074 02 94 67
    
    --
    GabJob - https://gabjob.org
    """
    
    try:
        message = MIMEMultipart('alternative')
        subject = template['subject'].format(prenom=prenom_safe)
        message['Subject'] = subject
        message['From'] = f"GabJob <{EMAIL_SENDER}>"
        message['To'] = client_email
        
        message.attach(MIMEText(text, 'plain', 'utf-8'))
        message.attach(MIMEText(html, 'html', 'utf-8'))
        
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(EMAIL_SENDER, EMAIL_PASSWORD)
            server.send_message(message)
        
        print(f"[WELCOME EMAIL] ✅ Envoyé à {client_email} ({type_user})")
        return True
        
    except Exception as e:
        print(f"[WELCOME EMAIL] ❌ Erreur : {e}")
        return False


# Test
if __name__ == '__main__':
    from dotenv import load_dotenv
    load_dotenv()
    EMAIL_PASSWORD = os.environ.get('EMAIL_PASSWORD', '')
    print("Test email candidat...")
    send_welcome_email('test@example.com', 'Abdel', 'Moustapha', 'candidat')
    print("Test email recruteur...")
    send_welcome_email('test@example.com', 'Abdel', 'Moustapha', 'recruteur')
    print("Test email technicien...")
    send_welcome_email('test@example.com', 'Abdel', 'Moustapha', 'technicien')
