let currentTpl = 't1';
let photoMode = 'none';
let photoShape = 'round';
let photoData = '';
let experiences = [{poste:'', entreprise:'', date:'', desc:''}];
let formations = [{diplome:'', ecole:'', date:''}];

function selTemplate(tpl, el) {
  currentTpl = tpl;
  document.querySelectorAll('.tpl').forEach(t => t.classList.remove('active'));
  el.classList.add('active');
  render();
}

function setPhotoMode(mode, el) {
  photoMode = mode;
  document.querySelectorAll('.photo-options .photo-opt').forEach(o => o.classList.remove('active'));
  el.classList.add('active');
  if (mode === 'add') {
    document.getElementById('photo-shape-pick').classList.add('show');
    document.getElementById('photo-zone').classList.remove('hidden');
  } else {
    document.getElementById('photo-shape-pick').classList.remove('show');
    document.getElementById('photo-zone').classList.add('hidden');
    document.getElementById('photo-preview-wrap').classList.remove('show');
    photoData = '';
  }
  render();
}

function setPhotoShape(shape, el) {
  photoShape = shape;
  document.querySelectorAll('.photo-shape-pick .photo-opt').forEach(o => o.classList.remove('active'));
  el.classList.add('active');
  const preview = document.getElementById('photo-preview');
  if (shape === 'square') preview.classList.add('square'); else preview.classList.remove('square');
  render();
}

function handlePhoto(e) {
  const file = e.target.files[0];
  if (!file) return;
  if (file.size > 3 * 1024 * 1024) { alert('Photo trop lourde (max 3MB)'); return; }
  const reader = new FileReader();
  reader.onload = ev => {
    photoData = ev.target.result;
    document.getElementById('photo-preview').src = photoData;
    document.getElementById('photo-zone').classList.add('hidden');
    document.getElementById('photo-preview-wrap').classList.add('show');
    render();
  };
  reader.readAsDataURL(file);
}

function removePhoto() {
  photoData = '';
  document.getElementById('photo-preview-wrap').classList.remove('show');
  document.getElementById('photo-zone').classList.remove('hidden');
  render();
}

function toggleSection(el) {
  const block = el.parentElement;
  block.classList.toggle('open');
  el.querySelector('.section-toggle').textContent = block.classList.contains('open') ? '−' : '+';
}

function renderExpList() {
  const container = document.getElementById('exp-list');
  container.innerHTML = experiences.map((e, i) => 
    '<div class="item-card">' +
    (experiences.length > 1 ? '<button class="btn-del" onclick="delExp(' + i + ')">✕</button>' : '') +
    '<div class="fg"><label>Poste</label><input type="text" value="' + e.poste + '" placeholder="Comptable Senior" oninput="updExp(' + i + ',\'poste\',this.value)"></div>' +
    '<div class="fg"><label>Entreprise</label><input type="text" value="' + e.entreprise + '" placeholder="BGFI Bank Gabon" oninput="updExp(' + i + ',\'entreprise\',this.value)"></div>' +
    '<div class="fg"><label>Période</label><input type="text" value="' + e.date + '" placeholder="Jan 2022 — Présent" oninput="updExp(' + i + ',\'date\',this.value)"></div>' +
    '<div class="fg"><label>Description</label><textarea rows="2" placeholder="Gestion de la comptabilité..." oninput="updExp(' + i + ',\'desc\',this.value)">' + e.desc + '</textarea></div>' +
    '</div>'
  ).join('');
}

function addExp() { experiences.push({poste:'',entreprise:'',date:'',desc:''}); renderExpList(); render(); }
function delExp(i) { experiences.splice(i,1); renderExpList(); render(); }
function updExp(i, field, val) { experiences[i][field] = val; render(); }

function renderFormList() {
  const container = document.getElementById('form-list');
  container.innerHTML = formations.map((f, i) => 
    '<div class="item-card">' +
    (formations.length > 1 ? '<button class="btn-del" onclick="delForm(' + i + ')">✕</button>' : '') +
    '<div class="fg"><label>Diplôme</label><input type="text" value="' + f.diplome + '" placeholder="Licence en Comptabilité" oninput="updForm(' + i + ',\'diplome\',this.value)"></div>' +
    '<div class="fg"><label>Établissement</label><input type="text" value="' + f.ecole + '" placeholder="Université Omar Bongo" oninput="updForm(' + i + ',\'ecole\',this.value)"></div>' +
    '<div class="fg"><label>Année</label><input type="text" value="' + f.date + '" placeholder="2018 — 2021" oninput="updForm(' + i + ',\'date\',this.value)"></div>' +
    '</div>'
  ).join('');
}

function addForm() { formations.push({diplome:'',ecole:'',date:''}); renderFormList(); render(); }
function delForm(i) { formations.splice(i,1); renderFormList(); render(); }
function updForm(i, field, val) { formations[i][field] = val; render(); }

function getData() {
  return {
    prenom: document.getElementById('cv-prenom').value || 'Votre Prénom',
    nom: document.getElementById('cv-nom').value || 'Nom',
    titre: document.getElementById('cv-titre').value || 'Votre poste recherché',
    tel: document.getElementById('cv-tel').value,
    email: document.getElementById('cv-email').value,
    ville: document.getElementById('cv-ville').value,
    linkedin: document.getElementById('cv-linkedin').value,
    resume: document.getElementById('cv-resume').value || 'Professionnel motivé avec une solide expérience. Rédigez votre pitch ici.',
    skills: (document.getElementById('cv-skills').value || 'Compétence 1, Compétence 2, Compétence 3').split(',').map(s => s.trim()).filter(Boolean),
    langues: document.getElementById('cv-langues').value || 'Français (natif), Anglais (courant)',
  };
}

function photoHtml(cls) {
  const shapeCls = photoShape === 'square' ? ' square' : '';
  if (photoData) return '<img class="' + cls + shapeCls + '" src="' + photoData + '" alt="Photo">';
  return '';
}

function initialsHtml(cls, d) {
  const initials = ((d.prenom[0] || '?') + (d.nom[0] || '')).toUpperCase();
  const shapeCls = photoShape === 'square' ? ' square' : '';
  return '<div class="' + cls + '-placeholder' + shapeCls + '">' + initials + '</div>';
}

function renderT1(d) {
  const photo = (photoMode === 'add') ? (photoData ? photoHtml('t1-photo') : initialsHtml('t1-photo', d)) : '';
  let html = '<div class="t1-header">' + photo + '<div>' +
    '<h1>' + d.prenom + ' ' + d.nom + '</h1>' +
    '<div class="t1-title">' + d.titre + '</div>' +
    '<div class="t1-contacts">' +
    (d.tel ? '<span>📱 ' + d.tel + '</span>' : '') +
    (d.email ? '<span>✉️ ' + d.email + '</span>' : '') +
    (d.ville ? '<span>📍 ' + d.ville + '</span>' : '') +
    (d.linkedin ? '<span>💼 ' + d.linkedin + '</span>' : '') +
    '</div></div></div>';

  html += '<div class="t1-body">';
  html += '<div class="t1-section"><h2>Profil</h2><div class="t1-summary">' + d.resume + '</div></div>';

  html += '<div class="t1-section"><h2>Expérience professionnelle</h2>';
  experiences.forEach(e => {
    if (e.poste || e.entreprise) {
      html += '<div class="t1-item">' +
        '<div class="t1-item-head"><div class="t1-item-title">' + (e.poste || 'Poste') + '</div>' +
        '<div class="t1-item-date">' + (e.date || '') + '</div></div>' +
        '<div class="t1-item-company">' + (e.entreprise || '') + '</div>' +
        (e.desc ? '<div class="t1-item-desc">' + e.desc + '</div>' : '') +
        '</div>';
    }
  });
  html += '</div>';

  html += '<div class="t1-2col"><div class="t1-section"><h2>Formation</h2>';
  formations.forEach(f => {
    if (f.diplome || f.ecole) {
      html += '<div class="t1-item"><div class="t1-item-title">' + (f.diplome || '') + '</div>' +
        '<div class="t1-item-company">' + (f.ecole || '') + '</div>' +
        '<div class="t1-item-date">' + (f.date || '') + '</div></div>';
    }
  });
  html += '</div><div class="t1-section"><h2>Langues</h2><div class="t1-summary">' + d.langues + '</div></div></div>';

  html += '<div class="t1-section"><h2>Compétences</h2><div class="t1-skills">';
  d.skills.forEach(s => { html += '<span class="t1-skill">' + s + '</span>'; });
  html += '</div></div></div>';
  return html;
}

function renderT2(d) {
  const photo = (photoMode === 'add') ? (photoData ? photoHtml('t2-photo') : initialsHtml('t2-photo', d)) : '';
  let html = '<div class="t2-side">' + photo +
    '<h3>Contact</h3>' +
    (d.tel ? '<div class="t2-contact-item">📱 ' + d.tel + '</div>' : '') +
    (d.email ? '<div class="t2-contact-item">✉️ ' + d.email + '</div>' : '') +
    (d.ville ? '<div class="t2-contact-item">📍 ' + d.ville + '</div>' : '') +
    (d.linkedin ? '<div class="t2-contact-item">💼 ' + d.linkedin + '</div>' : '') +
    '<h3>Compétences</h3>';
  d.skills.forEach(s => { html += '<div class="t2-skill-item">' + s + '</div>'; });
  html += '<h3>Langues</h3><div class="t2-skill-item" style="padding-left:0;">' + d.langues + '</div></div>';

  html += '<div class="t2-main"><h1>' + d.prenom + ' ' + d.nom + '</h1>' +
    '<div class="t2-title">' + d.titre + '</div>' +
    '<h2>Profil</h2><div class="t2-summary">' + d.resume + '</div>' +
    '<h2>Expérience</h2>';
  experiences.forEach(e => {
    if (e.poste || e.entreprise) {
      html += '<div class="t2-item">' +
        '<div class="t2-item-title">' + (e.poste || 'Poste') + '</div>' +
        '<div class="t2-item-company">' + (e.entreprise || '') + '</div>' +
        '<div class="t2-item-date">' + (e.date || '') + '</div>' +
        (e.desc ? '<div class="t2-item-desc">' + e.desc + '</div>' : '') +
        '</div>';
    }
  });
  html += '<h2>Formation</h2>';
  formations.forEach(f => {
    if (f.diplome || f.ecole) {
      html += '<div class="t2-item">' +
        '<div class="t2-item-title">' + (f.diplome || '') + '</div>' +
        '<div class="t2-item-company">' + (f.ecole || '') + '</div>' +
        '<div class="t2-item-date">' + (f.date || '') + '</div></div>';
    }
  });
  html += '</div>';
  return html;
}

function renderT3(d) {
  const photo = (photoMode === 'add') ? (photoData ? photoHtml('t3-photo') : initialsHtml('t3-photo', d)) : '';
  let html = '<div class="t3-header">' + photo +
    '<h1>' + d.prenom + ' ' + d.nom + '</h1>' +
    '<div class="t3-title">' + d.titre + '</div>' +
    '<div class="t3-contacts">' +
    (d.tel ? '<span>📱 ' + d.tel + '</span>' : '') +
    (d.email ? '<span>✉️ ' + d.email + '</span>' : '') +
    (d.ville ? '<span>📍 ' + d.ville + '</span>' : '') +
    (d.linkedin ? '<span>💼 ' + d.linkedin + '</span>' : '') +
    '</div></div>';

  html += '<div class="t3-body"><h2>Profil</h2><div class="t3-summary">"' + d.resume + '"</div>' +
    '<h2>Expérience Professionnelle</h2>';
  experiences.forEach(e => {
    if (e.poste || e.entreprise) {
      html += '<div class="t3-item">' +
        '<div class="t3-item-head"><div class="t3-item-title">' + (e.poste || 'Poste') + '</div>' +
        '<div class="t3-item-date">' + (e.date || '') + '</div></div>' +
        '<div class="t3-item-company">' + (e.entreprise || '') + '</div>' +
        (e.desc ? '<div class="t3-item-desc">' + e.desc + '</div>' : '') +
        '</div>';
    }
  });

  html += '<div class="t3-2col"><div><h2>Formation</h2>';
  formations.forEach(f => {
    if (f.diplome || f.ecole) {
      html += '<div class="t3-item">' +
        '<div class="t3-item-title">' + (f.diplome || '') + '</div>' +
        '<div class="t3-item-company">' + (f.ecole || '') + '</div>' +
        '<div class="t3-item-date">' + (f.date || '') + '</div></div>';
    }
  });
  html += '</div><div><h2>Langues</h2><div class="t3-summary" style="text-align:center;">' + d.langues + '</div></div></div>';

  html += '<h2>Compétences</h2><div class="t3-skills">';
  d.skills.forEach(s => { html += '<span class="t3-skill">' + s + '</span>'; });
  html += '</div></div>';
  return html;
}

function render() {
  const d = getData();
  const cvEl = document.getElementById('cv-render');
  cvEl.className = 'cv ' + currentTpl;
  if (currentTpl === 't1') cvEl.innerHTML = renderT1(d);
  else if (currentTpl === 't2') cvEl.innerHTML = renderT2(d);
  else cvEl.innerHTML = renderT3(d);
}

function downloadPDF() {
  const d = getData();
  const element = document.querySelector('.cv-paper');
  const filename = ('CV_' + d.prenom + '_' + d.nom + '.pdf').replace(/\s+/g, '_');
  const opt = {
    margin: 0,
    filename: filename,
    image: { type: 'jpeg', quality: 0.98 },
    html2canvas: { scale: 2, useCORS: true, logging: false },
    jsPDF: { unit: 'mm', format: 'a4', orientation: 'portrait' }
  };
  html2pdf().set(opt).from(element).save();
}

function payerEtDebloquer() {
  document.getElementById('paywall').classList.add('hidden');
  localStorage.setItem('cv_unlocked', 'true');
}

if (localStorage.getItem('cv_unlocked') === 'true') {
  document.getElementById('paywall').classList.add('hidden');
}
renderExpList();
renderFormList();
render();
