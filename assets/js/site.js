/* Progressive enhancements. All restaurant data remains readable without JS. */
(() => {
  'use strict';
  const $ = selector => document.querySelector(selector);
  const $$ = selector => [...document.querySelectorAll(selector)];
  const params = new URLSearchParams(location.search);
  const includes = (values, value) => !value || !values || values.split(' ').includes(value);
  const download = (value, name, type) => {
    const url = URL.createObjectURL(new Blob([value], { type }));
    const link = document.createElement('a');
    link.href = url; link.download = name; document.body.append(link);
    link.click(); link.remove(); setTimeout(() => URL.revokeObjectURL(url), 10000);
  };
  const picker = $('#location-context');
  if (picker) {
    $('.context-picker').hidden = false;
    if ([...picker.options].some(o => o.value === params.get('location'))) picker.value = params.get('location');
  }
  const service = $('#service-context');
  if (service && [...service.options].some(o => o.value === params.get('service'))) service.value = params.get('service');
  if ($('.service-picker')) $('.service-picker').hidden = false;
  function context() {
    const loc = picker ? picker.value : document.body.dataset.locationDefault || params.get('location') || '';
    const svc = service ? service.value : params.get('service') || '';
    $$('[data-location-card]').forEach(card => {
      card.hidden = !includes(card.dataset.locationCard, loc) || !includes(card.dataset.serviceCard, svc);
    });
    $$('[data-context-link]').forEach(link => {
      const url = new URL(link.href, location.href);
      if (url.origin !== location.origin) return;
      if (loc) url.searchParams.set('location', loc); else url.searchParams.delete('location');
      if (svc) url.searchParams.set('service', svc); else url.searchParams.delete('service');
      link.href = url.href;
    });
    if ($('#context-status')) $('#context-status').textContent = loc ? `Showing ${picker.selectedOptions[0].textContent}.` : 'Showing all locations.';
    menu();
  }
  const filters = $('.menu-filters');
  const query = $('#menu-query');
  let category = 'all';
  function menu() {
    if (!filters) return;
    const needle = (query.value || '').trim().toLocaleLowerCase();
    const loc = picker ? picker.value : '';
    const svc = service ? service.value : '';
    let count = 0;
    $$('[data-category]').forEach(section => {
      let visible = 0;
      [...section.querySelectorAll('[data-menu-item]')].forEach(item => {
        const match = (category === 'all' || section.dataset.category === category) &&
          includes(item.dataset.locations, loc) && includes(item.dataset.services, svc) &&
          item.dataset.search.toLocaleLowerCase().includes(needle);
        item.hidden = !match;
        if (match) { visible++; count++; }
      });
      section.hidden = visible === 0;
    });
    $('#menu-status').textContent = count ? `${count} dishes shown.` : 'No matching dishes. Clear the search or choose another location, service, or category.';
  }
  if (filters) {
    $('.menu-tools').hidden = false;
    filters.addEventListener('click', event => {
      const button = event.target.closest('button[data-filter]');
      if (!button) return;
      category = button.dataset.filter;
      filters.querySelectorAll('button').forEach(b => b.setAttribute('aria-pressed', String(b === button)));
      menu();
    });
    query.addEventListener('input', menu);
    // A dish permalink must reveal that dish, even if contextual filters would hide it.
    const reveal = () => {
      let id;
      try { id = decodeURIComponent(location.hash.slice(1)); } catch { return; }
      const item = document.getElementById(id);
      if (!item || !item.matches('[data-menu-item]')) return;
      category = 'all'; query.value = ''; service.value = '';
      if (picker) picker.value = '';
      const url = new URL(location.href); url.searchParams.delete('location'); url.searchParams.delete('service');
      history.replaceState(null, '', url);
      filters.querySelectorAll('button').forEach(b => b.setAttribute('aria-pressed', String(b.dataset.filter === 'all')));
      context(); item.scrollIntoView({ block: 'center' });
    };
    window.addEventListener('hashchange', reveal);
    menu(); if (location.hash) reveal();
  }
  if (service) service.addEventListener('change', () => {
    const url = new URL(location.href);
    if (service.value) url.searchParams.set('service', service.value); else url.searchParams.delete('service');
    history.replaceState(null, '', url); context();
  });
  if (picker) picker.addEventListener('change', () => {
    const url = new URL(location.href);
    if (picker.value) url.searchParams.set('location', picker.value); else url.searchParams.delete('location');
    history.replaceState(null, '', url); context();
  });
  context();

  const search = $('.directory-search');
  if (search) {
    search.hidden = false;
    search.querySelector('input').addEventListener('input', event => {
      const words = event.target.value.trim().toLocaleLowerCase().split(/\s+/).filter(Boolean);
      let count = 0;
      $$('[data-search-text]').forEach(card => {
        card.hidden = !words.every(word => card.dataset.searchText.toLocaleLowerCase().includes(word));
        if (!card.hidden) count++;
      });
      $$('.directory-group').forEach(group => { group.hidden = ![...group.querySelectorAll('[data-search-text]')].some(card => !card.hidden); });
      $('#search-status').textContent = count ? `${count} pages found.` : 'No matches. Try a shorter term or clear the search.';
    });
  }
  $$('.explore-nav').forEach(details => {
    details.addEventListener('keydown', event => {
      if (event.key === 'Escape') { details.open = false; details.querySelector('summary').focus(); }
    });
    document.addEventListener('click', event => { if (!details.contains(event.target)) details.open = false; });
    details.addEventListener('focusout', event => {
      if (event.relatedTarget && !details.contains(event.relatedTarget)) details.open = false;
    });
  });

  // Print expanded answers and complete editable text, then restore the screen state.
  let printDetails = [];
  let printFields = [];
  let printScopeNote;
  let printing = false;
  window.addEventListener('beforeprint', () => {
    if (printing) return;
    printing = true;
    printDetails = $$('main details').map(details => [details, details.open]);
    printDetails.forEach(([details]) => { details.open = true; });
    printFields = $$('main textarea').map(field => {
      const text = document.createElement('p');
      text.className = 'print-field-value';
      text.textContent = field.value || 'Not specified';
      field.after(text); field.classList.add('print-field-source');
      return [field, text];
    });
    const identity = $('.menu-print-identity');
    if (identity) {
      printScopeNote = document.createElement('p');
      printScopeNote.className = 'menu-print-scope';
      printScopeNote.textContent = document.body.dataset.printScope === 'selection'
        ? `Current selection · ${$('#menu-status')?.textContent || 'Current visible dishes'}`
        : 'Full menu · All locations and services';
      identity.after(printScopeNote);
    }
  });
  window.addEventListener('afterprint', () => {
    printDetails.forEach(([details, open]) => { details.open = open; });
    printFields.forEach(([field, text]) => { field.classList.remove('print-field-source'); text.remove(); });
    printScopeNote?.remove();
    printDetails = []; printFields = []; printScopeNote = undefined;
    printing = false;
    delete document.body.dataset.printScope;
  });
  const printControls = $('.print-controls');
  if (printControls) {
    printControls.hidden = false;
    printControls.addEventListener('click', event => {
      const button = event.target.closest('[data-print]');
      if (!button) return;
      document.body.dataset.printScope = button.dataset.print;
      window.print();
    });
  }

  function refreshTime() {
    $$('.location-hours').forEach(panel => {
    if (panel.dataset.reviewed !== 'true') return;
    try {
      const parts = Object.fromEntries(new Intl.DateTimeFormat('en-CA', { timeZone: panel.dataset.timezone, year: 'numeric', month: '2-digit', day: '2-digit', hour: '2-digit', minute: '2-digit', hourCycle: 'h23' }).formatToParts(new Date()).filter(p => p.type !== 'literal').map(p => [p.type, p.value]));
      const date = `${parts.year}-${parts.month}-${parts.day}`;
      const day = (new Date(`${date}T12:00:00Z`).getUTCDay() + 6) % 7;
      const exception = JSON.parse(panel.dataset.exceptions).find(e => e.date === date);
      const weekly = JSON.parse(panel.dataset.hours).find(e => e.day === day);
      const schedule = exception || weekly;
      if (!schedule) { panel.querySelector('.hours-status').textContent = `Hours unknown for today · ${panel.dataset.timezone}`; return; }
      const now = `${parts.hour}:${parts.minute}`;
      const open = schedule.intervals.some(([start, end]) => now >= start && now < end);
      panel.querySelector('.hours-status').textContent = `${open ? 'Open now' : 'Closed now'} · ${panel.dataset.timezone}${exception ? ' · Special schedule' : ''}`;
    } catch { /* The complete written schedule remains the fallback. */ }
    });
    $$('[data-expiring], .record[data-end]').forEach(element => {
    if (!element.dataset.end || new Date(element.dataset.end).getTime() > Date.now()) return;
    if (element.hasAttribute('data-expiring')) element.hidden = true;
    else {
      element.dataset.recordState = 'expired';
      element.querySelector('.state-badge').textContent = 'Expired';
      element.querySelectorAll('.calendar-download, a.text-link').forEach(control => { control.hidden = true; });
    }
    });
  }
  refreshTime();
  setInterval(refreshTime, 60000);
  document.addEventListener('visibilitychange', () => { if (!document.hidden) refreshTime(); });
  const icsEscape = value => String(value || '').replace(/\\/g, '\\\\').replace(/\r?\n/g, '\\n').replace(/,/g, '\\,').replace(/;/g, '\\;');
  const stamp = value => new Date(value).toISOString().replace(/[-:]/g, '').replace(/\.\d{3}Z$/, 'Z');
  // Fold by UTF-8 octets, preserving Unicode code points (RFC 5545).
  const fold = line => {
    let result = '', chunk = '', bytes = 0;
    for (const c of line) {
      const n = new TextEncoder().encode(c).length;
      if (bytes + n > 73) { result += chunk + '\r\n '; chunk = ''; bytes = 1; }
      chunk += c; bytes += n;
    }
    return result + chunk;
  };
  $$('.calendar-download').forEach(button => {
    if (button.closest('.record').dataset.recordState === 'expired') return;
    button.hidden = false;
    button.addEventListener('click', () => {
      const d = button.dataset;
      const lines = ['BEGIN:VCALENDAR', 'VERSION:2.0', 'PRODID:-//Hot Eats//Restaurant calendar//EN', 'BEGIN:VEVENT', `UID:${icsEscape(d.id)}@${location.hostname}`, `DTSTAMP:${stamp(new Date())}`, `DTSTART:${stamp(d.start)}`, `DTEND:${stamp(d.end)}`, `SUMMARY:${icsEscape(d.title)}`, `LOCATION:${icsEscape(d.venue)}`, 'END:VEVENT', 'END:VCALENDAR'];
      download(lines.map(fold).join('\r\n') + '\r\n', `${d.id}.ics`, 'text/calendar;charset=utf-8');
    });
  });

  const form = $('#gathering-planner');
  if (!form) return;
  const panel = $('.brief-panel'); const output = $('#brief-output'); const status = $('#brief-status');
  const fields = ['occasion', 'location', 'date', 'guests', 'budget', 'notes'];
  let prepared = false;
  $('#prepare-brief').hidden = false; $('.draft-import').hidden = false;
  for (const key of ['occasion', 'location']) {
    const select = form.elements.namedItem(key); const value = params.get(key);
    if (value && [...select.options].some(o => o.value === value)) select.value = value;
  }
  const updateMail = () => {
    const link = $('#email-brief'); if (!link) return;
    // Avoid silently truncating a long body in mail clients; full text remains exportable.
    if (output.value.length > 1800) { link.hidden = true; return; }
    link.hidden = false;
    link.href = `mailto:${link.dataset.recipient}?subject=${encodeURIComponent('Gathering inquiry')}&body=${encodeURIComponent(output.value)}`;
  };
  form.addEventListener('submit', event => {
    event.preventDefault(); if (!form.reportValidity()) return;
    const data = new FormData(form);
    const readableDate = data.get('date') ? new Intl.DateTimeFormat(document.documentElement.lang || 'en', { dateStyle: 'long' }).format(new Date(`${data.get('date')}T12:00:00`)) : 'Flexible / not specified';
    output.value = ['Gathering inquiry — availability and pricing to be confirmed', '', `Service: ${form.elements.namedItem('occasion').selectedOptions[0]?.textContent || 'To be discussed'}`, `Location: ${form.elements.namedItem('location').selectedOptions[0]?.textContent || 'To be discussed'}`, `Preferred date: ${readableDate}`, `Approximate guests: ${data.get('guests') || 'Not specified'}`, `Budget: ${data.get('budget') || 'To be discussed'}`, '', 'Notes and questions:', data.get('notes') || 'None yet.', '', 'Please confirm availability, pricing, and next steps.'].join('\n');
    prepared = true; panel.hidden = false; status.textContent = 'Brief prepared. Nothing has been sent or saved automatically.'; updateMail(); output.focus();
  });
  form.addEventListener('input', () => { if (prepared) status.textContent = 'Planning details changed. Prepare again to include them; this replaces edits in the brief. Save a draft first to keep those edits.'; });
  output.addEventListener('input', updateMail);
  $('#copy-brief').addEventListener('click', async () => {
    try { await navigator.clipboard.writeText(output.value); status.textContent = 'Copied to your clipboard.'; }
    catch { output.focus(); output.select(); status.textContent = 'Clipboard access was unavailable. The brief is selected for your usual copy command. Download is also available.'; }
  });
  $('#download-brief').addEventListener('click', () => { download(output.value, 'gathering-brief.txt', 'text/plain;charset=utf-8'); status.textContent = 'Text download requested. Check your browser downloads.'; });
  $('#save-brief').addEventListener('click', () => {
    const data = Object.fromEntries(fields.map(key => [key, form.elements.namedItem(key).value]));
    download(JSON.stringify({ version: 1, fields: data, brief: output.value }, null, 2), 'gathering-draft.json', 'application/json'); status.textContent = 'Draft download requested. Keep this file private if it contains personal details.';
  });
  $('#import-brief').addEventListener('change', async event => {
    try {
      const file = event.target.files[0]; if (!file) return;
      if (file.size > 65536) throw new Error('Draft must be under 64 KB.');
      const data = JSON.parse(await file.text());
      if (data.version !== 1 || typeof data.brief !== 'string' || data.brief.length > 10000 || !data.fields) throw new Error('Unrecognized draft format.');
      for (const key of fields) {
        if (typeof data.fields[key] !== 'string' || data.fields[key].length > (key === 'notes' ? 2000 : 120)) throw new Error(`Invalid ${key} value.`);
        const field = form.elements.namedItem(key);
        if (field.tagName === 'SELECT' && ![...field.options].some(o => o.value === data.fields[key])) throw new Error(`The saved ${key} is unavailable in this restaurant.`);
        const probe = field.cloneNode(true); probe.value = data.fields[key];
        if (probe.value !== data.fields[key] || !probe.checkValidity()) throw new Error(`Invalid ${key} value.`);
      }
      for (const key of fields) form.elements.namedItem(key).value = data.fields[key];
      output.value = data.brief; prepared = true; panel.hidden = false; updateMail(); output.focus(); status.textContent = 'Draft restored locally. Review the details before sharing.';
    } catch (error) { panel.hidden = false; status.textContent = `Draft not opened: ${error.message}`; }
    event.target.value = '';
  });
  $('#clear-brief').addEventListener('click', () => { form.reset(); output.value = ''; panel.hidden = true; prepared = false; status.textContent = ''; $('#event-type').focus(); });
  $('#planner-fields').disabled = false;
})();
