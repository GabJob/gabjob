
  const API = '';
  let userTel = '';
  let currentType = 'candidat';
  let ctaType = 'candidat';

  function selType(type) {
    currentType = type;
    ['candidat','recruteur','technicien'].forEach(t => {
      document.getElementById('tab-'+t).classList.remove('active');
    });
    document.getElementById('tab-'+type).classList.add('active');
    const spec = document.getElementById('fg-specialite');
    const q = document.getElementById('fg-quartier');
    if (type === 'technicien') { spec.style.display='block'; }
    else { spec.style.display='none'; }
  }

  function selCta(type) {
    ctaType = type;
    ['candidat','recruteur','technicien'].forEach(t => {
      document.getElementById('cta-'+t).classList.remove('sel');
    });
    document.getElementById('cta-'+type).classList.add('sel');
    const labels = { candidat:'Je cherche un emploi', recruteur:'Je recrute', technicien:'Je suis technicien' };
  }

  function openModalFromCta() { openModal(ctaType); }

  function openModal(type) {
    currentType = type || 'candidat';
    selType(currentType);
    document.getElementById('step1').style.display='block';
    document.getElementById('step2').style.display='none';
    document.getElementById('step3').style.display='none';
    document.getElementById('modal').classList.add('open');
  }

  function closeModal() { document.getElementById('modal').classList.remove('open'); }
  document.getElementById('modal').addEventListener('click', e => { if(e.target.id==='modal') closeModal(); });

  async function inscrire() {
    const nom = document.getElementById('r-nom').value.trim();
    const tel = document.getElementById('r-tel').value.trim();
    if (!nom || !tel) { showMsg('msg1','Nom et téléphone sont obligatoires.','err'); return; }
    const btn = document.querySelector('#step1 .btn-modal');
    btn.disabled = true; btn.textContent = 'Chargement...';
    try {
      const body = { nom, telephone: tel, type: currentType, email: document.getElementById('r-email').value, quartier: document.getElementById('r-quartier').value };
      if (currentType === 'technicien') {
        const spec = document.getElementById('r-spec').value;
        if (!spec) { showMsg('msg1','Choisissez votre spécialité.','err'); btn.disabled=false; btn.textContent='Créer mon compte →'; return; }
        body.specialite = spec;
      }
      const res = await fetch(API + '/api/auth/inscription', { method:'POST', headers:{'Content-Type':'application/json'}, body: JSON.stringify(body) });
      const data = await res.json();
      if (res.ok || res.status === 409) {
        userTel = tel;
        await fetch(API + '/api/auth/envoyer-otp', { method:'POST', headers:{'Content-Type':'application/json'}, body: JSON.stringify({telephone: tel}) });
        document.getElementById('step1').style.display='none';
        document.getElementById('step2').style.display='block';
        document.getElementById('otp-tel').textContent = tel;
        document.getElementById('o1').focus();
      } else { showMsg('msg1', data.erreur || 'Erreur.', 'err'); }
    } catch(e) { showMsg('msg1','Serveur indisponible — réessayez.','err'); }
    btn.disabled=false; btn.textContent='Créer mon compte →';
  }

  function nextOtp(el, nextId) {
    if (el.value.length === 1 && nextId) document.getElementById(nextId)?.focus();
  }

  async function verifyOtp() {
    const code = ['o1','o2','o3','o4','o5','o6'].map(id => document.getElementById(id).value).join('');
    if (code.length < 6) return;
    try {
      const res = await fetch(API + '/api/auth/verifier-otp', { method:'POST', headers:{'Content-Type':'application/json'}, body: JSON.stringify({telephone: userTel, code}) });
      const data = await res.json();
      if (res.ok) {
        localStorage.setItem('gabjob_token', data.token);
        localStorage.setItem('gabjob_user', JSON.stringify(data.utilisateur));
        document.getElementById('step2').style.display='none';
        document.getElementById('step3').style.display='block';
        const urls = { recruteur:'/dashboard-recruteur', technicien:'/depannage', candidat:'/dashboard' };
        document.getElementById('btn-dashboard').onclick = () => window.location = urls[data.utilisateur.type] || '/dashboard';
        toast('🎉 Bienvenue sur GabJob, ' + data.utilisateur.nom + ' !');
      } else { showMsg('msg2', data.erreur || 'Code incorrect.', 'err'); }
    } catch(e) { showMsg('msg2','Erreur vérification.','err'); }
  }

  function showMsg(id, txt, type) {
    const el = document.getElementById(id);
    el.textContent = txt; el.className = 'msg ' + type;
  }

  function toast(msg) {
    const t = document.getElementById('toast');
    t.textContent = msg; t.classList.add('show');
    setTimeout(() => t.classList.remove('show'), 4000);
  }

  // ── NOTIFICATIONS ANIMÉES ──
  const notifData = [
    { icon:'💼', bg:'#fff7ed', color:'#ea580c', title:'Nouvelle offre publiee', desc:'Total Gabon - Comptable Senior - 450 000 FCFA/mois', time:'Il y a 2 min' },
    { icon:'🎉', bg:'#f0fdf4', color:'#16a34a', title:'Candidat recrute !', desc:'Jean Ondo vient detre recrute chez BGFI Bank', time:'Il y a 5 min' },
    { icon:'🔧', bg:'#fff7ed', color:'#ea580c', title:'Technicien disponible', desc:'Pierre Moussavou - Plombier - 4.9 etoiles - Libreville', time:'Maintenant' },
    { icon:'👤', bg:'#eff6ff', color:'#2563eb', title:'Nouveau candidat inscrit', desc:'Marie Obame - Comptable - 5 ans experience', time:'Il y a 8 min' },
    { icon:'⭐', bg:'#fefce8', color:'#d97706', title:'Avis 5 etoiles recu', desc:'Excellent technicien ! Probleme resolu en 30 min.', time:'Il y a 12 min' },
    { icon:'💬', bg:'#f0fdf4', color:'#16a34a', title:'Contact WhatsApp', desc:'Un recruteur vient de contacter Alain Biyogo', time:'Il y a 15 min' },
    { icon:'💳', bg:'#fff7ed', color:'#ea580c', title:'Abonnement active', desc:'Marc Nguema - Technicien climatisation - Actif', time:'Il y a 20 min' },
    { icon:'📋', bg:'#eff6ff', color:'#2563eb', title:'Offre pourvue !', desc:'Assistant RH chez Gabon Telecom - Poste pourvu', time:'Il y a 25 min' },
    { icon:'🏆', bg:'#fefce8', color:'#d97706', title:'Profil Premium active', desc:'Fatou Ella - Badge Premium - Profil mis en avant', time:'Il y a 30 min' },
    { icon:'📱', bg:'#f0fdf4', color:'#16a34a', title:'CV genere avec succes', desc:'Serge Mba - CV professionnel telecharge', time:'Il y a 35 min' },
  ];

  let nIdx = 0;

  function buildNotif(n) {
    var el = document.createElement('div');
    el.style.cssText = 'background:white;border-radius:14px;padding:13px 16px;box-shadow:0 8px 32px rgba(0,0,0,0.15);display:flex;align-items:flex-start;gap:10px;opacity:0;transform:translateX(60px);transition:all 0.5s cubic-bezier(0.22,1,0.36,1);margin-bottom:10px;border-left:3px solid '+n.color+';';
    el.innerHTML = '<div style="width:36px;height:36px;border-radius:9px;background:'+n.bg+';display:flex;align-items:center;justify-content:center;font-size:1.1rem;flex-shrink:0;">'+n.icon+'</div>'
      + '<div style="flex:1;min-width:0;">'
      + '<div style="font-family:Syne,sans-serif;font-size:0.78rem;font-weight:700;color:#111;margin-bottom:2px;">'+n.title+'</div>'
      + '<div style="font-size:0.68rem;color:#6b7280;line-height:1.4;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;">'+n.desc+'</div>'
      + '<div style="font-size:0.62rem;color:#9ca3af;margin-top:3px;">'+n.time+'</div>'
      + '</div>';
    return el;
  }

  function fireNotif() {
    var container = document.getElementById('notif-stream');
    if (!container) return;
    var n = notifData[nIdx % notifData.length];
    nIdx++;
    var el = buildNotif(n);
    container.appendChild(el);
    // Supprimer si plus de 3
    while (container.children.length > 3) {
      var first = container.children[0];
      first.style.opacity = '0';
      first.style.transform = 'translateX(-40px)';
      setTimeout(function(f){ f.remove(); }, 500, first);
    }
    // Animer l'entrée
    setTimeout(function() {
      el.style.opacity = '1';
      el.style.transform = 'translateX(0)';
    }, 50);
    // Animer la sortie après 4s
    setTimeout(function() {
      el.style.opacity = '0';
      el.style.transform = 'translateX(60px)';
      setTimeout(function() { if(el.parentNode) el.remove(); }, 500);
    }, 4500);
  }

  // Lancer les 3 premières au chargement
  setTimeout(function(){ fireNotif(); }, 1000);
  setTimeout(function(){ fireNotif(); }, 2200);
  setTimeout(function(){ fireNotif(); }, 3400);

  // Ensuite une nouvelle toutes les 3 secondes
  setInterval(function(){ fireNotif(); }, 3000);

