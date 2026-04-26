"""
Module SMS OTP pour GabJob via Africa's Talking
"""

import os
import africastalking

# Configuration depuis .env
AT_USERNAME = os.environ.get('AT_USERNAME', 'sandbox')
AT_API_KEY = os.environ.get('AT_API_KEY', '')
AT_SENDER_ID = os.environ.get('AT_SENDER_ID', '')  # Optionnel, vide en sandbox

# Initialiser une seule fois au démarrage
_initialized = False
_sms = None


def init_at():
    """Initialise Africa's Talking (une seule fois)"""
    global _initialized, _sms
    if _initialized:
        return True
    if not AT_API_KEY:
        print("[SMS] ⚠️ AT_API_KEY non configurée — SMS désactivés (mode DEV)")
        return False
    try:
        africastalking.initialize(AT_USERNAME, AT_API_KEY)
        _sms = africastalking.SMS
        _initialized = True
        print(f"[SMS] ✅ Africa's Talking initialisé (username: {AT_USERNAME})")
        return True
    except Exception as e:
        print(f"[SMS] ❌ Erreur init Africa's Talking : {e}")
        return False


def format_phone(telephone):
    """
    Formate un numéro gabonais en format international +241XXXXXXXXX
    """
    tel = str(telephone).strip().replace(' ', '').replace('-', '').replace('+', '')
    if tel.startswith('241'):
        return '+' + tel
    if tel.startswith('0'):
        return '+241' + tel[1:]
    if len(tel) == 8:
        return '+241' + tel
    return '+' + tel


def send_otp_sms(telephone, code):
    """
    Envoie un SMS avec le code OTP au client
    
    Args:
        telephone: Numéro du client (ex: "074029467" ou "+24104029467")
        code: Code OTP à 6 chiffres
    
    Returns:
        dict {success: bool, message: str, cost: str}
    """
    # Toujours afficher en logs (utile pour debug)
    print(f"[OTP DEV] 📱 Code {code} pour {telephone}")
    
    # Si pas configuré, on reste en mode DEV (logs uniquement)
    if not init_at():
        return {'success': False, 'message': 'Mode DEV : voir les logs', 'cost': '0'}
    
    # Formater le numéro
    tel_formatted = format_phone(telephone)
    
    # Message à envoyer
    msg = f"GabJob: Votre code de verification est {code}. Valable 10 minutes. Ne le partagez avec personne."
    
    try:
        # Envoyer le SMS
        if AT_SENDER_ID:
            response = _sms.send(msg, [tel_formatted], AT_SENDER_ID)
        else:
            response = _sms.send(msg, [tel_formatted])
        
        # Analyser la réponse
        recipients = response.get('SMSMessageData', {}).get('Recipients', [])
        if recipients and recipients[0].get('status') == 'Success':
            cost = recipients[0].get('cost', 'N/A')
            print(f"[SMS] ✅ Envoyé à {tel_formatted} | Coût: {cost}")
            return {'success': True, 'message': 'SMS envoyé', 'cost': cost}
        else:
            err = recipients[0].get('status', 'Unknown') if recipients else 'Aucun destinataire'
            print(f"[SMS] ❌ Échec : {err}")
            return {'success': False, 'message': err, 'cost': '0'}
    
    except Exception as e:
        print(f"[SMS] ❌ Exception : {e}")
        return {'success': False, 'message': str(e), 'cost': '0'}


# Test rapide
if __name__ == '__main__':
    from dotenv import load_dotenv
    load_dotenv()
    AT_USERNAME = os.environ.get('AT_USERNAME', 'sandbox')
    AT_API_KEY = os.environ.get('AT_API_KEY', '')
    print("Test envoi SMS...")
    result = send_otp_sms('+24104029467', '123456')
    print("Résultat:", result)
