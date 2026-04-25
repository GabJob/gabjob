// =================================================================
// PROGRAMME PARRAINAGE — GabJob (v2 : Réservé aux abonnés payants)
// =================================================================

const API = '';
let token = localStorage.getItem('gabjob_token') || null;
let currentUser = null;
const SEUIL = 10; // 10 filleuls payants = 1 mois gratuit

// =================================================================
// AUTH
// =================================================================

function showLogin() {
  document.getElementById('auth-overlay').style.display = 'flex';
  document.getElementById('paywall-overlay').style.display = 'none';
  document.getElementById('main-nav').style.display = 'none';
  document.getElementById('main').style.display = 'none';
}

function showPaywall() {
  document.getElementById('auth-overlay').style.display = 'none';
  document.getElementById('paywall-overlay').style.display = 'flex';
  document.getElementById('main-nav').style.display = 'none';
  document.getElementById('main').style.display = 'none';
}

function showApp() {
  document.getElementById('auth-overlay').style.display = 'none';
  document.getElementById('paywall-overlay').style.display = 'none';
  document.getElementById('main-nav').style.display = 'flex';
  document.getElementById('main').style.display = 'block';
  loadParrainageData();
}

async function sendLoginOtp() {
  const tel = document.getElementById('login-tel').value.trim();
  if (!tel) { showMsg('login-msg', 'Entrez votre numéro', 'error'); return; }
  try {
    const res = await fetch(API + '/api/auth/envoyer-otp', {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({telephone: tel})
    });
    const data = await res.json();
    if (res.ok) {
      document.getElementById('login-otp-section').style.display = 'block';
      showMsg('login-msg', 'Code envoyé !', 'success');
      window.loginTel = tel;
    } else {
      showMsg('login-msg', data.error || 'Erreur', 'error');
    }
  } catch(e) {
    showMsg('login-msg', 'Erreur de connexion', 'error');
  }
}

async function verifyLoginOtp() {
  const code = document.getElementById('login-otp').value.trim();
  if (!code || code.length !== 6) { showMsg('login-msg', 'Code à 6 chiffres', 'error'); return; }
  try {
    const res = await fetch(API + '/api/auth/verifier-otp', {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({telephone: window.loginTel, code: code})
    });
    const data = await res.json();
    if (res.ok && data.token) {
      token = data.token;
      currentUser = data.user;
      localStorage.setItem('gabjob_token', token);
      localStorage.setItem('gabjob_user', JSON.stringify(currentUser));
      checkSubscription();
    } else {
      showMsg('login-msg', data.error || 'Code invalide', 'error');
    }
  } catch(e) {
    showMsg('login-msg', 'Erreur de connexion', 'error');
  }
}

// =================================================================
// CHECK SUBSCRIPTION (Premium / Pro / Technicien)
// =================================================================

async function checkSubscription() {
  if (!token) { showLogin(); return; }
  
  try {
    const res = await fetch(API + '/api/auth/me', {
      headers: {'Authorization': 'Bearer ' + token}
    });
    if (res.ok) {
      currentUser = await res.json();
      localStorage.setItem('gabjob_user', JSON.stringify(currentUser));
    }
  } catch(e) {
    const saved = localStorage.getItem('gabjob_user');
    if (saved) currentUser = JSON.parse(saved);
  }
  
  // Vérifier si l'utilisateur a un abonnement payant actif
  const isPaying = currentUser && (
    currentUser.abonnement_actif === true ||
    currentUser.premium === true ||
    currentUser.is_premium === true ||
    (currentUser.type === 'recruteur' && currentUser.abonnement_actif) ||
    (currentUser.type === 'technicien' && currentUser.abonnement_actif)
  );
  
  if (isPaying) {
    showApp();
  } else {
    // Mettre à jour les infos du paywall avec le type d'utilisateur
    updatePaywallContent();
    showPaywall();
  }
}

function updatePaywallContent() {
  const type = currentUser ? currentUser.type : 'candidat';
  const titles = {
    candidat: { name: 'Candidat Premium', price: '5 000 FCFA / mois' },
    recruteur: { name: 'Recruteur Pro', price: '120 000 FCFA / an' },
    technicien: { name: 'Technicien Dépannage', price: '10 000 FCFA / mois' }
  };
  const info = titles[type] || titles.candidat;
  const titleEl = document.getElementById('paywall-plan-name');
  const priceEl = document.getElementById('paywall-plan-price');
  if (titleEl) titleEl.textContent = info.name;
  if (priceEl) priceEl.textContent = info.price;
}

// =================================================================
// LOAD DATA
// =================================================================

async function loadParrainageData() {
  try {
    const res = await fetch(API + '/api/parrainage/mes-stats', {
      headers: {'Authorization': 'Bearer ' + token}
    });
    if (res.ok) {
      const data = await res.json();
      renderData(data);
      return;
    }
  } catch(e) {}
  
  // Fallback données locales
  const data = {
    code_parrainage: generateCode(currentUser),
    nb_filleuls_payants: 0,
    nb_filleuls_total: 0,
    filleuls: [],
    rewards: [],
    mois_gratuits: 0
  };
  
  const localFilleuls = JSON.parse(localStorage.getItem('gabjob_filleuls') || '[]');
  data.filleuls = localFilleuls;
  data.nb_filleuls_payants = localFilleuls.filter(f => f.payant === true).length;
  data.nb_filleuls_total = localFilleuls.length;
  
  const localRewards = JSON.parse(localStorage.getItem('gabjob_rewards') || '[]');
  data.rewards = localRewards;
  
  renderData(data);
}

function generateCode(user) {
  if (user && user.code_parrainage) return user.code_parrainage;
  const prefix = (user && user.prenom ? user.prenom : 'GAB').toUpperCase().substring(0, 5).replace(/[^A-Z]/g, '');
  const suffix = user && user.id ? user.id : Math.floor(Math.random() * 9000 + 1000);
  return prefix + suffix;
}

function getReferralLink(code) {
  return 'https://gabjob.org/?ref=' + code;
}

function renderData(data) {
  const link = getReferralLink(data.code_parrainage);
  document.getElementById('referral-link').value = link;
  
  const payants = data.nb_filleuls_payants || 0;
  const total = data.nb_filleuls_total || 0;
  const count = payants % SEUIL;
  
  document.getElementById('filleuls-count').textContent = count;
  document.getElementById('filleuls-total').textContent = total;
  document.getElementById('filleuls-payants').textContent = payants;
  
  const pct = (count / SEUIL) * 100;
  document.getElementById('progress-fill').style.width = pct + '%';
  
  const remaining = SEUIL - count;
  let progressText;
  if (count === 0 && payants === 0) {
    progressText = 'Plus que 10 filleuls Premium pour gagner 1 mois gratuit !';
  } else if (remaining === 0) {
    progressText = '🎉 Bravo ! 1 mois Premium débloqué !';
  } else if (remaining === 1) {
    progressText = '🔥 Plus qu\'1 filleul Premium pour gagner 1 mois gratuit !';
  } else {
    progressText = `Plus que ${remaining} filleuls Premium pour gagner 1 mois gratuit !`;
  }
  document.getElementById('progress-text').textContent = progressText;
  
  renderFilleuls(data.filleuls);
  renderRewards(data.rewards);
  setupShareButtons(link, data.code_parrainage);
}

function renderFilleuls(filleuls) {
  const container = document.getElementById('filleuls-list');
  if (!filleuls || filleuls.length === 0) {
    container.innerHTML = '<div class="empty-state"><div class="empty-icon">👻</div><div class="empty-title">Aucun filleul pour l\'instant</div><p>Partagez votre lien pour commencer à gagner !</p></div>';
    return;
  }
  container.innerHTML = filleuls.map(f => {
    const initials = ((f.prenom || '?')[0] + (f.nom ? f.nom[0] : '')).toUpperCase();
    const date = new Date(f.date_inscription || f.date || Date.now()).toLocaleDateString('fr-FR', {day:'numeric',month:'long',year:'numeric'});
    const isPayant = f.payant === true;
    return `
      <div class="filleul-row ${isPayant ? '' : 'pending'}">
        <div class="filleul-avatar ${isPayant ? '' : 'gray'}">${initials}</div>
        <div class="filleul-info">
          <div class="filleul-name">${f.prenom || 'Filleul'} ${f.nom || ''}</div>
          <div class="filleul-date">${isPayant ? '✓ Abonné Premium · ' : 'Inscrit (gratuit) · '}${date}</div>
        </div>
        <div class="filleul-status ${isPayant ? 'paid' : 'free'}">
          ${isPayant ? '⭐ Compte +1' : '🔓 Pas Premium'}
        </div>
      </div>
    `;
  }).join('');
}

function renderRewards(rewards) {
  const card = document.getElementById('rewards-card');
  const container = document.getElementById('rewards-list');
  if (!rewards || rewards.length === 0) {
    card.style.display = 'none';
    return;
  }
  card.style.display = 'block';
  container.innerHTML = rewards.map(r => {
    const date = new Date(r.date || Date.now()).toLocaleDateString('fr-FR', {day:'numeric',month:'long',year:'numeric'});
    const expire = new Date(r.expire || Date.now()).toLocaleDateString('fr-FR', {day:'numeric',month:'long',year:'numeric'});
    return `
      <div class="reward-row">
        <div class="reward-icon">⭐</div>
        <div class="reward-info">
          <div class="reward-info-title">1 mois Premium gratuit</div>
          <div class="reward-info-date">Crédité le ${date} · Expire le ${expire}</div>
        </div>
        <div class="reward-info-status">${r.statut || 'Actif'}</div>
      </div>
    `;
  }).join('');
}

// =================================================================
// SHARE
// =================================================================

function setupShareButtons(link, code) {
  const message = `Salut ! 👋 Je viens de découvrir GabJob, la plateforme N°1 d'emploi au Gabon. Inscris-toi avec mon lien et trouve un job rapidement : ${link}`;
  
  document.getElementById('share-wa').href = 'https://wa.me/?text=' + encodeURIComponent(message);
  document.getElementById('share-fb').href = 'https://www.facebook.com/sharer/sharer.php?u=' + encodeURIComponent(link) + '&quote=' + encodeURIComponent(message);
  document.getElementById('share-sms').href = 'sms:?body=' + encodeURIComponent(message);
  document.getElementById('share-tw').href = 'https://twitter.com/intent/tweet?text=' + encodeURIComponent(message);
}

function copyLink() {
  const link = document.getElementById('referral-link');
  link.select();
  link.setSelectionRange(0, 99999);
  
  try { document.execCommand('copy'); }
  catch(e) {
    if (navigator.clipboard) navigator.clipboard.writeText(link.value);
  }
  
  const btn = document.querySelector('.btn-copy');
  btn.classList.add('copied');
  btn.textContent = '✓ Copié !';
  toast('🎉 Lien copié dans le presse-papier');
  
  setTimeout(() => {
    btn.classList.remove('copied');
    btn.textContent = '📋 Copier';
  }, 2000);
}

// =================================================================
// PAYWALL ACTION
// =================================================================

function activerAbonnement() {
  // TODO : intégrer le paiement plus tard
  toast('💬 Contactez-nous pour activer votre abonnement');
  // Optionnel : rediriger vers la page principale
  setTimeout(() => { window.location = '/#abonnements'; }, 1500);
}

// =================================================================
// HELPERS
// =================================================================

function showMsg(id, text, type) {
  const el = document.getElementById(id);
  el.textContent = text;
  el.className = 'msg show ' + type;
}

function toast(msg) {
  const t = document.getElementById('toast');
  t.textContent = msg;
  t.classList.add('show');
  setTimeout(() => t.classList.remove('show'), 2800);
}

// =================================================================
// INIT
// =================================================================

if (token) {
  const saved = localStorage.getItem('gabjob_user');
  if (saved) currentUser = JSON.parse(saved);
  checkSubscription();
} else {
  showLogin();
}
