const api = {
  base: '',
  token: () => localStorage.getItem('automa_token') || '',
  headers() {
    const h = { 'Content-Type': 'application/json' };
    const t = this.token();
    if (t) h['Authorization'] = `Bearer ${t}`;
    return h;
  },
  async get(path) {
    const r = await fetch(`${this.base}${path}`, { headers: this.headers() });
    if (!r.ok) throw new Error(await r.text());
    return r.json();
  },
  async post(path, data, asForm = false) {
    let init;
    if (asForm) {
      init = { method: 'POST', headers: { 'Content-Type': 'application/x-www-form-urlencoded' }, body: new URLSearchParams(data) };
    } else {
      init = { method: 'POST', headers: this.headers(), body: JSON.stringify(data) };
    }
    const r = await fetch(`${this.base}${path}`, init);
    if (!r.ok) throw new Error(await r.text());
    return r.json();
  }
};

function setText(el, text, cls) {
  el.textContent = text;
  el.classList.remove('ok','warn','err');
  if (cls) el.classList.add(cls);
}

async function refreshHealth() {
  const pill = document.getElementById('health');
  try {
    const data = await api.get('/api/v1/health');
    setText(pill, `OK`, 'ok');
  } catch (e) {
    setText(pill, 'DOWN', 'err');
  }
}

async function refreshMe() {
  const box = document.getElementById('me');
  if (!api.token()) { box.classList.add('hide'); box.textContent = ''; return; }
  try {
    const data = await api.get('/api/v1/users/me');
    box.classList.remove('hide');
    box.textContent = `Prihlásený: ${data.email} ${data.is_admin ? '(admin)' : ''}`;
  } catch (e) {
    localStorage.removeItem('automa_token');
    box.classList.add('hide');
  }
}

async function refreshAgents() {
  const ul = document.getElementById('agents');
  const list = await api.get('/api/v1/agents');
  ul.innerHTML = '';
  for (const a of list) {
    const li = document.createElement('li');
    li.textContent = `${a.id} • ${a.name} — ${a.description || ''}`;
    ul.appendChild(li);
  }
}

async function refreshScripts() {
  const ul = document.getElementById('scripts');
  const list = await api.get('/api/v1/scripts');
  ul.innerHTML = '';
  for (const s of list) {
    const li = document.createElement('li');
    li.textContent = `${s.id} • ${s.name} — ${s.path}`;
    ul.appendChild(li);
  }
}

async function refreshJobs() {
  const ul = document.getElementById('jobs');
  const list = await api.get('/api/v1/jobs');
  ul.innerHTML = '';
  for (const j of list) {
    const li = document.createElement('li');
    li.textContent = `${j.id} • status=${j.status}${j.last_run_at ? ' • last=' + j.last_run_at : ''}`;
    ul.appendChild(li);
  }
}

function wireAuth() {
  const form = document.getElementById('login-form');
  const status = document.getElementById('login-status');
  form.addEventListener('submit', async (e) => {
    e.preventDefault();
    status.textContent = '…';
    const fd = new FormData(form);
    const username = fd.get('username');
    const password = fd.get('password');
    try {
      const data = await api.post('/api/v1/auth/token', { username, password }, true);
      localStorage.setItem('automa_token', data.access_token);
      status.textContent = 'OK';
      await refreshMe();
      await Promise.all([refreshAgents(), refreshScripts(), refreshJobs()]);
    } catch (err) {
      status.textContent = 'Chyba prihlásenia';
    }
  });
}

function wireForms() {
  document.getElementById('agent-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    const fd = new FormData(e.target);
    try {
      await api.post('/api/v1/agents', { name: fd.get('name'), description: fd.get('description') });
      e.target.reset();
      refreshAgents();
    } catch (err) { alert('Chyba pri vytváraní agenta'); }
  });

  document.getElementById('script-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    const fd = new FormData(e.target);
    try {
      await api.post('/api/v1/scripts', { name: fd.get('name'), path: fd.get('path'), description: fd.get('description') });
      e.target.reset();
      refreshScripts();
    } catch (err) { alert('Chyba pri vytváraní skriptu'); }
  });

  document.getElementById('job-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    const fd = new FormData(e.target);
    const script_id = fd.get('script_id');
    const when = fd.get('when');
    let payload = {};
    if (script_id) payload.script_id = Number(script_id);
    if (when) payload.when = new Date(when).toISOString();
    try {
      await api.post('/api/v1/jobs', payload);
      e.target.reset();
      refreshJobs();
    } catch (err) { alert('Chyba pri vytváraní jobu'); }
  });
}

async function boot() {
  wireAuth();
  wireForms();
  await refreshHealth();
  await refreshMe();
  await Promise.all([refreshAgents(), refreshScripts(), refreshJobs()]);
}

boot();

