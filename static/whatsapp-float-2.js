/* ================================================================ */
/* BOUTON WHATSAPP FLOTTANT — GabJob */
/* Injection automatique sur toutes les pages */
/* ================================================================ */

(function() {
  // Configuration
  const WA_NUMBER = '24107402946700'; // +241 074 02 94 67 (sans le + ni espaces)
  const WA_NUMBER_FORMATTED = '+241 074 02 94 67';
  
  // Détecter le contexte de la page pour personnaliser le message
  function getContextMessage() {
    const path = window.location.pathname;
    let baseMsg = "Bonjour GabJob 👋";
    
    if (path.includes('/dashboard-recruteur')) {
      return baseMsg + ", je suis recruteur et je voudrais activer mon abonnement Pro (120 000 FCFA/an).";
    }
    if (path.includes('/dashboard')) {
      return baseMsg + ", je voudrais activer mon abonnement Candidat Premium (5 000 FCFA/mois).";
    }
    if (path.includes('/depannage')) {
      return baseMsg + ", je suis technicien et je voudrais m'inscrire au service dépannage (10 000 FCFA/mois).";
    }
    if (path.includes('/cv-generator')) {
      return baseMsg + ", je voudrais débloquer le générateur de CV Pro (10 000 FCFA).";
    }
    if (path.includes('/parrainage')) {
      return baseMsg + ", je voudrais activer mon abonnement pour utiliser le programme parrainage.";
    }
    if (path.includes('/contact')) {
      return baseMsg + ", j'ai une question concernant GabJob.";
    }
    
    return baseMsg + ", j'aimerais en savoir plus sur GabJob.";
  }
  
  // Créer le bouton
  function createWaButton() {
    const message = encodeURIComponent(getContextMessage());
    const link = document.createElement('a');
    link.className = 'gj-wa-float';
    link.href = `https://wa.me/${WA_NUMBER}?text=${message}`;
    link.target = '_blank';
    link.rel = 'noopener noreferrer';
    link.setAttribute('aria-label', 'Contacter GabJob sur WhatsApp');
    link.innerHTML = `
      <span class="gj-wa-tooltip">Une question ? Écrivez-nous !</span>
      <span class="gj-wa-icon">
        <svg viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
          <path d="M.057 24l1.687-6.163c-1.041-1.804-1.588-3.849-1.587-5.946.003-6.556 5.338-11.891 11.893-11.891 3.181.001 6.167 1.24 8.413 3.488 2.245 2.248 3.481 5.236 3.48 8.414-.003 6.557-5.338 11.892-11.893 11.892-1.99-.001-3.951-.5-5.688-1.448l-6.305 1.654zm6.597-3.807c1.676.995 3.276 1.591 5.392 1.592 5.448 0 9.886-4.434 9.889-9.885.002-5.462-4.415-9.89-9.881-9.892-5.452 0-9.887 4.434-9.889 9.884-.001 2.225.651 3.891 1.746 5.634l-.999 3.648 3.742-.981zm11.387-5.464c-.074-.124-.272-.198-.57-.347-.297-.149-1.758-.868-2.031-.967-.272-.099-.47-.149-.669.149-.198.297-.768.967-.941 1.165-.173.198-.347.223-.644.074-.297-.149-1.255-.462-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.297-.347.446-.521.151-.172.2-.296.3-.495.099-.198.05-.372-.025-.521-.075-.148-.669-1.611-.916-2.206-.242-.579-.487-.501-.669-.51l-.57-.01c-.198 0-.52.074-.792.372s-1.04 1.016-1.04 2.479 1.065 2.876 1.213 3.074c.149.198 2.095 3.2 5.076 4.487.709.306 1.263.489 1.694.626.712.226 1.36.194 1.872.118.571-.085 1.758-.719 2.006-1.413.248-.695.248-1.29.173-1.414z"/>
        </svg>
      </span>
      <span class="gj-wa-text">WhatsApp</span>
    `;
    
    // Tracking optionnel (pour stats plus tard)
    link.addEventListener('click', function() {
      try {
        const clicks = parseInt(localStorage.getItem('gj_wa_clicks') || '0');
        localStorage.setItem('gj_wa_clicks', (clicks + 1).toString());
      } catch(e) {}
    });
    
    return link;
  }
  
  // Injecter dans le DOM quand prêt
  function inject() {
    // Ne pas dupliquer si déjà présent
    if (document.querySelector('.gj-wa-float')) return;
    
    const btn = createWaButton();
    document.body.appendChild(btn);
  }
  
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', inject);
  } else {
    inject();
  }
})();
