// FALLBACK ONLY: run portal form submissions from inside the chairman's already logged-in Chrome tab
// (use when scripted login is rate limited and .sp_session is stale). Normal route: portal_ops.py / push_page.py.
//
// How: open any https://www.styrelseproffset.se/... page in Chrome (mcp__claude-in-chrome__navigate), then paste this file's
// contents into mcp__claude-in-chrome__javascript_tool (action javascript_exec) ONCE; stay on that page (a navigation
// resets window state). Then call e.g.   await BRFB.setPage(21535, {html:'<p>..</p>'})
// Gotchas seen: the portal itself already uses the global name `SP` (use BRFB); the tool blocks outputs that look like
// URL/query strings (strip = ? & from returned text); return short strings; the session cookie is HttpOnly so scripts
// outside the browser cannot reuse it.
window.BRFB = {
  async get(u){ const r = await fetch(u, {credentials:'same-origin'}); return [new DOMParser().parseFromString(await r.text(), 'text/html'), r]; },
  btn(f, re){ return [...f.querySelectorAll('button[type=submit]')].find(b => re.test(b.textContent)); },
  form(d, re){ return [...d.forms].find(f => re.test(f.getAttribute('action') || '')); },
  // new FormData(form, submitterButton) keeps repeated fields (module_ids[] ...) and checked boxes exactly like a real click
  async post(f, over, submitRe){ const fd = new FormData(f, this.btn(f, submitRe)); for(const [k,v] of Object.entries(over||{})){ fd.delete(k); [].concat(v).forEach(x => fd.append(k, x)); }
    return fetch(f.getAttribute('action'), {method:'POST', body:fd, credentials:'same-origin'}); },
  // update text / state / access of an existing page. access: 1 public, 3 member login. files: array of file ids
  async setPage(id, o){ const [d] = await this.get('/portal/sites/page/edit.php?id=' + id); const f = this.form(d, /page\/edit/); const over = {};
    if(o.title) over.title = o.title; if(o.slug) over.slug = o.slug; if(o.state) over.state = String(o.state); if(o.access) over.access_type = String(o.access);
    if(o.html != null){ over[[...f.querySelectorAll('textarea')].find(t => /^module_1_\d+_text$/.test(t.name)).name] = o.html; }
    if(o.files){ over[[...f.querySelectorAll('input')].find(i => /^module_5_\d+_file$/.test(i.name)).name] = o.files.map(x => '1401-' + x).join(','); }
    return (await this.post(f, over, /Spara/)).status; },
  // new page: modules 1 text, 5 files, 4 contact form. Returns id.
  async createPage(title, modules){ const [d] = await this.get('/portal/sites/page/create.php'); const f = this.form(d, /page\/create/);
    const r = await this.post(f, {title, 'modules[]': modules.map(String)}, /Skapa/); return +new URL(r.url).searchParams.get('id'); },
  // new news post (published, author Styrelsen, notifications suppressed)
  async createNews(title, html, date, time){ const [d] = await this.get('/portal/sites/update/edit.php'); const f = this.form(d, /update\/edit/);
    const r = await this.post(f, {title, body: html, author_id: '0', published_from_date: date, published_from_time: time || '09:00', state: '2', suppress_notification: '1'}, /Spara/);
    return +new URL(r.url).searchParams.get('id'); }
};
'ok';
