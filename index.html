
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>Investigator Desk</title>
  <link rel="stylesheet" href="styles.css" />
  <!-- Libraries (CDN) -->
  <script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.1/dist/chart.umd.min.js"></script>
  <script src="https://cdn.jsdelivr.net/npm/vis-network@9.1.2/dist/vis-network.min.js"></script>
  <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/vis-network/styles/vis-network.min.css" />
</head>
<body>
  <header class="app-header">
    <div class="brand">
      <h1>Investigator Desk</h1>
      <p class="sub">Cases, evidence, link analysis, timelines, and records requests.</p>
    </div>
    <div class="meta">
      <span id="last-save">Last save: —</span>
    </div>
  </header>

  <main class="grid">
    <!-- Case panel -->
    <section class="panel">
      <h2>Case overview</h2>
      <div class="case-row">
        <label>
          <span class="label">Case ID</span>
          <input id="case-id" placeholder="e.g., R-2025-001" />
        </label>
        <label>
          <span class="label">Title</span>
          <input id="case-title" placeholder="e.g., Procurement irregularities (FY2024)" />
        </label>
        <label class="wide">
          <span class="label">Description</span>
          <textarea id="case-desc" rows="2" placeholder="Purpose, scope, alleged actors, jurisdictions..."></textarea>
        </label>
      </div>
      <div class="row-actions">
        <button id="new-case">New case</button>
        <button id="save-case">Save</button>
        <button id="export-case">Export JSON</button>
        <input type="file" id="import-file" accept="application/json" />
        <button id="import-case">Import JSON</button>
      </div>
    </section>

    <!-- Evidence panel -->
    <section class="panel">
      <h2>Evidence ingest</h2>
      <div class="evidence-actions">
        <input type="file" id="evidence-file" multiple />
        <input id="evidence-url" placeholder="Paste URL" />
        <button id="add-evidence">Add</button>
      </div>
      <div class="evidence-list">
        <table>
          <thead>
            <tr>
              <th>Type</th><th>Label</th><th>Source</th><th>Date</th><th>Hash</th><th>Actions</th>
            </tr>
          </thead>
          <tbody id="evidence-tbody"></tbody>
        </table>
      </div>
    </section>

    <!-- Entities and link analysis -->
    <section class="panel">
      <h2>Entities & link graph</h2>
      <div class="entities-row">
        <label>
          <span class="label">Entity name</span>
          <input id="entity-name" placeholder="e.g., John Doe, ACME LLC" />
        </label>
        <label>
          <span class="label">Type</span>
          <select id="entity-type">
            <option value="person">Person</option>
            <option value="org">Organization</option>
            <option value="asset">Asset</option>
            <option value="location">Location</option>
            <option value="account">Account</option>
          </select>
        </label>
        <button id="add-entity">Add entity</button>
      </div>
      <div class="link-row">
        <label>
          <span class="label">Link from</span>
          <select id="link-from"></select>
        </label>
        <label>
          <span class="label">Link to</span>
          <select id="link-to"></select>
        </label>
        <label>
          <span class="label">Relation</span>
          <input id="link-relation" placeholder="e.g., controls, funds, located-at" />
        </label>
        <button id="add-link">Add link</button>
      </div>
      <div class="graph-wrap">
        <div id="graph" style="height: 300px;"></div>
      </div>
    </section>

    <!-- Timeline -->
    <section class="panel">
      <h2>Timeline</h2>
      <div class="timeline-row">
        <label>
          <span class="label">Event</span>
          <input id="event-title" placeholder="e.g., Contract awarded" />
        </label>
        <label>
          <span class="label">Date</span>
          <input id="event-date" type="date" />
        </label>
        <label class="wide">
          <span class="label">Notes</span>
          <textarea id="event-notes" rows="2"></textarea>
        </label>
        <button id="add-event">Add event</button>
      </div>
      <div class="timeline-chart">
        <canvas id="timelineChart" height="100"></canvas>
      </div>
      <ul id="timeline-list"></ul>
    </section>

    <!-- Records request generator -->
    <section class="panel">
      <h2>Public records request generator</h2>
      <div class="foia-row">
        <label class="wide">
          <span class="label">Jurisdiction</span>
          <input id="foia-juris" placeholder="e.g., Arizona (state agency) or City of Phoenix" />
        </label>
        <label class="wide">
          <span class="label">Target agency</span>
          <input id="foia-agency" placeholder="e.g., Procurement Office" />
        </label>
        <label class="wide">
          <span class="label">Records description</span>
          <textarea id="foia-desc" rows="3" placeholder="Contracts, emails, bid evaluations, invoices, communications between A and B from Jan–Mar 2024..."></textarea>
        </label>
        <div class="row-actions">
          <button id="generate-foia">Generate letter</button>
          <button id="download-foia">Download .txt</button>
        </div>
      </div>
      <pre id="foia-output" class="doc"></pre>
    </section>

    <!-- Chain of custody -->
    <section class="panel">
      <h2>Chain of custody</h2>
      <div class="coc-row">
        <label>
          <span class="label">Item</span>
          <input id="coc-item" placeholder="e.g., USB drive #A1" />
        </label>
        <label>
          <span class="label">Action</span>
          <input id="coc-action" placeholder="e.g., received, transferred, sealed" />
        </label>
        <label>
          <span class="label">By</span>
          <input id="coc-by" placeholder="e.g., Investigator Ryle" />
        </label>
        <label>
          <span class="label">Date/time</span>
          <input id="coc-date" type="datetime-local" />
        </label>
        <button id="add-coc">Log step</button>
      </div>
      <ul id="coc-list"></ul>
    </section>
  </main>

  <footer class="app-footer">
    <span>Client-side investigative toolkit • Exportable JSON • Deploy via GitHub Pages.</span>
  </footer>

  <script src="app.js"></script>
</body>
</html>
