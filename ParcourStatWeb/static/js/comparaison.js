/* trois variables qui persite pendat toute la session , elles constituent l'etat de la page */

let formationRows = [];
let rowCounter    = 0;
let panelOpen     = true;

/* lignes de formations
formationRows represente les lignes du formulaire en tableau et chaque element est un objet 
rowcounter s'incremente a chaque nouvelle ligne pour generer des ids uniques et ne pas reutiliser des ids si on supprime une ligne pour prevenir les conflits
panelOpen indique si le volet de filtres est ouvert ou non */

/* ajoute une nouvelle ligne vide dans le formulaire avec un blocage a partir de 5. ++rowCounter permet d'incrementer le compteur avant de l'utiliser. Renderformationrows() redessine le html  */
function addFormationRow() {
  if (formationRows.length >= 5) return;
  formationRows.push({ id: ++rowCounter, formationId: null });
  renderFormationRows();
  updateSummary();
}

/* supprime la ligne dont l'id correspond */
function removeFormationRow(id) {
  if (formationRows.length <= 1) return;
  formationRows = formationRows.filter(r => r.id !== id);
  renderFormationRows();
  updateSummary();
}
/* reconstruit le html du formulairea chaque ajout ou suppression de ligne */
function renderFormationRows() {
  const container = document.getElementById('formationRows');
  container.innerHTML = '';

  formationRows.forEach((row, idx) => {
    const div = document.createElement('div');
    div.className = 'input-group input-group-sm mb-1';

    // Construire les options groupees par etablissement à partir de GROUPES
    const optionsHtml = GROUPES.map(g => `
      <optgroup label="${g.etablissement}">
        ${g.formations.map(f =>
          `<option value="${f.id}" ${row.formationId == f.id ? 'selected' : ''}>${f.nom}</option>`
        ).join('')}
      </optgroup>
    `).join('');

    div.innerHTML = `
      <span class="input-group-text text-muted"
            style="font-size:.65rem; min-width:2rem; justify-content:center;">
        ${String(idx + 1).padStart(2, '0')}
      </span>
      <select class="form-select form-select-sm"
              onchange="onFormationChange(${row.id}, this.value)">
        <option value="">— Choisir une formation —</option>
        ${optionsHtml}
      </select>
      ${formationRows.length > 1
        ? `<button class="btn btn-outline-danger btn-sm"
                   onclick="removeFormationRow(${row.id})">×</button>`
        : ''}`;
    container.appendChild(div);
  });
/*mets a jour le compteur et desactive le bouton ajout a partir de 5*/
  const count = formationRows.length;
  document.getElementById('formCountBadge').textContent = `${count} / 5`;
  document.getElementById('formCountBadge').className =
    count >= 5 ? 'badge bg-danger' : 'badge bg-secondary';
  document.getElementById('addFormBtn').disabled = count >= 5;
}

function onFormationChange(rowId, value) {
  const row = formationRows.find(r => r.id === rowId);
  if (row) row.formationId = value ? parseInt(value) : null;
  updateSummary();
}

/*Resume et validation */

function updateSummary() {
  const summaryEl = document.getElementById('selectionSummary');
  const msgEl     = document.getElementById('validationMsg');
  const btnEl     = document.getElementById('btnGenerate');

  // Chercher dans tous les groupes (flatMap)
  const toutesFormations = GROUPES.flatMap(g => g.formations);

  const selFormations = formationRows
    .filter(r => r.formationId)
    .map(r => {
      const f = toutesFormations.find(x => x.id === r.formationId);
      return f ? f.nom : null;
    })
    .filter(Boolean);

  const checkedCriteria = [
    ...document.querySelectorAll('input[name="criterion"]:checked')
  ];

  const formPills = selFormations.map(nom =>
    `<span class="badge bg-dark" style="font-size:.65rem;" title="${nom}">
       ${nom.length > 22 ? nom.slice(0, 22) + '…' : nom}
     </span>`
  ).join('');

  const critPills = checkedCriteria.map(cb => {
    const label = cb.closest('.col-12')
                    .querySelector('span[style]').textContent.trim();
    return `<span class="badge bg-success" style="font-size:.65rem;">${label}</span>`;
  }).join('');

  summaryEl.innerHTML = (formPills + critPills) ||
    '<span class="text-muted" style="font-size:.75rem;">Aucune sélection</span>';

  const hasFormations = selFormations.length >= 1;
  const hasCrits      = checkedCriteria.length >= 1;

  msgEl.textContent = !hasFormations ? 'Sélectionnez au moins 1 formation'
                    : !hasCrits      ? 'Choisissez au moins 1 critère'
                    : '';
  btnEl.disabled = !(hasFormations && hasCrits);
}

/* panneau lateral de filtres */

function togglePanel() {
  panelOpen = !panelOpen;
  document.getElementById('panelBody').style.display    = panelOpen ? '' : 'none';
  document.getElementById('btnTogglePanel').textContent = panelOpen ? '◀' : '▶';
  document.getElementById('filterCol').className =
    panelOpen ? 'col-md-4 col-lg-3' : 'col-auto';
}

/* Generer */

function generate() {
  if (panelOpen) togglePanel();

  document.getElementById('compEmpty').style.display  = 'none';
  document.getElementById('chartsZone').style.display = 'block';
  document.getElementById('chartsZone').innerHTML = `
    <div class="text-center text-muted py-5">
      <div class="spinner-border text-secondary mb-3" role="status"></div>
      <p>Génération du graphique…</p>
    </div>`;

  const payload = {
    ids:      formationRows.filter(r => r.formationId).map(r => r.formationId),
    criteria: [...document.querySelectorAll('input[name="criterion"]:checked')]
                .map(cb => cb.value),
  };

  fetch('/api/chart-data', {
    method:  'POST',
    headers: { 'Content-Type': 'application/json' },
    body:    JSON.stringify(payload),
  })
  .then(r => r.json())
  .then(data => {
    if (data.error) {
      document.getElementById('chartsZone').innerHTML =
        `<div class="alert alert-danger">${data.error}</div>`;
      return;
    }
    renderResults(data);
  })
  .catch(() => {
    document.getElementById('chartsZone').innerHTML =
      '<div class="alert alert-danger">Erreur lors de la génération.</div>';
  });
}

/* Affichage des resultats */

function renderResults(data) {

  const retourHtml = `
    <div class="text-end mb-3">
      <button class="btn btn-outline-secondary btn-sm" onclick="togglePanel()">
        ◀ Modifier les filtres
      </button>
    </div>`;

  const graphHtml = `
    <div class="card shadow-sm mb-4">
      <div class="card-header bg-dark text-white">
        <h5 class="mb-0">📊 ${data.critere} — 2018 vs 2024</h5>
      </div>
      <div class="card-body text-center p-2">
        <img src="${data.image}"
             class="img-fluid rounded"
             alt="Graphique ${data.critere}"/>
      </div>
    </div>`;

  const syntheseItems = data.synthese.map(s => `
    <div class="card shadow-sm mb-3">
      <div class="card-header bg-secondary text-white py-2">
        <strong>${s.nom}</strong>
      </div>
      <div class="card-body py-3">
        <p class="mb-0" style="font-size:.9rem; line-height:1.8;">
          ${s.texte}
        </p>
      </div>
    </div>`).join('');

  const syntheseHtml = `
    <div class="card shadow-sm mb-4">
      <div class="card-header bg-dark text-white">
        <h5 class="mb-0">📝 Synthèse</h5>
      </div>
      <div class="card-body">
        ${syntheseItems}
      </div>
    </div>`;

  document.getElementById('chartsZone').innerHTML =
    retourHtml + graphHtml + syntheseHtml;
}

/* initialisation */
addFormationRow();
updateSummary();
