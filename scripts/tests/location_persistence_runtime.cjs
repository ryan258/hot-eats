'use strict';
// Limited test adapter: real generated HTML tree + entire actual production JS.
// Implements only the menu-used DOM properties/selectors/events. No browser,
// remote resources, native storage/layout/focus or general DOM-conformance claim.
const assert = require('node:assert/strict');
const fs = require('node:fs');
const vm = require('node:vm');
const input = JSON.parse(fs.readFileSync(0, 'utf8'));

function simpleMatch(element, selector) {
  let rest = selector;
  const tag = rest.match(/^(\*|[a-zA-Z][\w:-]*)/);
  if (tag) { if (tag[1] !== '*' && element.tag !== tag[1].toLowerCase()) return false; rest = rest.slice(tag[0].length); }
  while (rest) {
    let token;
    if ((token = rest.match(/^#([\w-]+)/))) { if (element.id !== token[1]) return false; }
    else if ((token = rest.match(/^\.([\w-]+)/))) { if (!element.className.split(/\s+/).includes(token[1])) return false; }
    else if ((token = rest.match(/^\[([\w-]+)(?:=(?:"([^"]*)"|'([^']*)'|([^\]]*)))?\]/))) {
      if (!element.hasAttribute(token[1])) return false;
      if (token[2] !== undefined || token[3] !== undefined || token[4] !== undefined) {
        if (element.getAttribute(token[1]) !== (token[2] ?? token[3] ?? token[4])) return false;
      }
    } else throw new Error(`Unsupported selector in limited adapter: ${selector}`);
    rest = rest.slice(token[0].length);
  }
  return true;
}

function matches(element, selector) {
  return selector.split(',').some(alternative => {
    const parts = alternative.trim().split(/\s+(?![^\[]*\])/);
    let current = element;
    if (!simpleMatch(current, parts.pop())) return false;
    while (parts.length) {
      const ancestor = parts.pop();
      current = current.parentElement;
      while (current && !simpleMatch(current, ancestor)) current = current.parentElement;
      if (!current) return false;
    }
    return true;
  });
}

class Element {
  constructor(tree, doc, parent = null) {
    this.tag = tree.tag; this.tagName = tree.tag.toUpperCase();
    this.attrs = { ...tree.attrs }; this.document = doc; this.parentElement = parent;
    this.listeners = new Map(); this.hidden = this.hasAttribute('hidden');
    this.dataset = Object.fromEntries(Object.entries(this.attrs).filter(([key]) => key.startsWith('data-')).map(([key, value]) => [key.slice(5).replace(/-([a-z])/g, (_, c) => c.toUpperCase()), value]));
    this.childNodes = tree.children.map(child => typeof child === 'string' ? child : new Element(child, doc, this));
    this.classList = { add: value => { this.className = `${this.className} ${value}`.trim(); }, remove: value => { this.className = this.className.split(/\s+/).filter(item => item !== value).join(' '); } };
  }
  get id() { return this.attrs.id || ''; }
  get className() { return this.attrs.class || ''; }
  set className(value) { this.attrs.class = value; }
  get children() { return this.childNodes.filter(child => child instanceof Element); }
  get textContent() { return this.childNodes.map(child => typeof child === 'string' ? child : child.textContent).join(''); }
  set textContent(value) { this.childNodes = [String(value)]; }
  hasAttribute(name) { return Object.hasOwn(this.attrs, name); }
  getAttribute(name) { return this.attrs[name] ?? null; }
  setAttribute(name, value) { this.attrs[name] = String(value); }
  matches(selector) { return matches(this, selector); }
  querySelectorAll(selector) {
    const output = [];
    const visit = node => { for (const child of node.children) { if (matches(child, selector)) output.push(child); visit(child); } };
    visit(this); return output;
  }
  querySelector(selector) { return this.querySelectorAll(selector)[0] || null; }
  closest(selector) { let item = this; while (item) { if (matches(item, selector)) return item; item = item.parentElement; } return null; }
  contains(element) { let item = element; while (item) { if (item === this) return true; item = item.parentElement; } return false; }
  get options() { return this.querySelectorAll('option'); }
  get value() {
    if (this.tag === 'select') return this._value ?? (this.options.find(option => option.hasAttribute('selected')) ?? this.options[0])?.value ?? '';
    return this._value ?? this.attrs.value ?? (this.tag === 'option' || this.tag === 'textarea' ? this.textContent : '');
  }
  set value(value) {
    const string = String(value);
    this._value = this.tag === 'select' && !this.options.some(option => option.value === string) ? '' : string;
  }
  get selectedOptions() { return this.options.filter(option => option.value === this.value); }
  get href() { return new URL(this.attrs.href || '', this.document.location.href).href; }
  set href(value) { this.attrs.href = String(value); }
  addEventListener(type, callback) { if (!this.listeners.has(type)) this.listeners.set(type, []); this.listeners.get(type).push(callback); }
  dispatchEvent(event) { event.target ??= this; for (const callback of this.listeners.get(event.type) || []) callback.call(this, event); return true; }
  focus() { this.document.activeElement = this; }
}

function openDocument(preset, storage, query = '', pageName = 'menu') {
  const source = input.documents[preset][pageName];
  const location = new URL(`https://synthetic.example.invalid${source.route}${query}`);
  const doc = { location, hidden: false, listeners: new Map() };
  const tree = new Element(source.tree, doc);
  doc.querySelectorAll = selector => tree.querySelectorAll(selector);
  doc.querySelector = selector => doc.querySelectorAll(selector)[0] || null;
  doc.getElementById = id => doc.querySelectorAll('[id]').find(element => element.id === id) || null;
  doc.body = doc.querySelector('body'); doc.documentElement = doc.querySelector('html');
  doc.addEventListener = (type, callback) => { if (!doc.listeners.has(type)) doc.listeners.set(type, []); doc.listeners.get(type).push(callback); };
  const windowListeners = new Map();
  const deny = () => { throw new Error('Network/unsupported platform operation forbidden in source-runtime test'); };
  const sandbox = {
    document: doc, location, URL, URLSearchParams, TextEncoder, Blob, console,
    localStorage: { getItem: key => storage.get(key) ?? null, setItem: (key, value) => storage.set(key, String(value)), removeItem: key => storage.delete(key) },
    history: { replaceState: (_state, _title, value) => { const next = new URL(value, location); assert.equal(next.origin, location.origin); location.href = next.href; } },
    window: { addEventListener: (type, callback) => { if (!windowListeners.has(type)) windowListeners.set(type, []); windowListeners.get(type).push(callback); }, print: deny },
    setInterval: () => 1, setTimeout: () => 1, fetch: deny, XMLHttpRequest: deny, WebSocket: deny,
  };
  vm.runInNewContext(input.source, sandbox, { filename: input.scriptPath, timeout: 2000 });
  const picker = doc.querySelector('#location-context');
  if (pageName === 'menu') assert.ok(picker, 'Actual generated menu must contain location picker');
  else assert.equal(picker, null, 'Cross-route fixture must be an actual page without a location picker');
  const menuPicker = picker || new Element(input.documents[preset].menu.tree, doc).querySelector('#location-context');
  const choices = menuPicker.options.map(option => option.value).filter(Boolean);
  assert.equal(new Set(choices).size, choices.length, 'Actual menu location IDs must be unique');
  assert.ok(choices.length >= 2, 'Synthetic fixture must exercise two valid locations');
  const anchors = doc.querySelectorAll('[data-location-option]');
  if (preset === 'food-truck') {
    assert.equal(anchors.length, 0, 'Disabled location route must not return navigation anchors');
    assert.equal(doc.querySelectorAll('a[href]').some(link => /\/locations\//.test(new URL(link.href).pathname)), false, 'No links to disabled location routes');
  } else assert.ok(choices.every(id => anchors.some(anchor => anchor.dataset.locationOption === id)), 'Enabled branch retains each location anchor');
  return { doc, picker, choices, location, storage, pageName };
}

function assertState(page, expected) {
  assert.equal(page.picker.value, expected, 'Menu select must show expected location');
  assert.equal(page.storage.get('he-location') || '', expected, 'Remembered location must agree');
  const status = page.doc.querySelector('#context-status').textContent;
  assert.equal(status, expected ? `Showing ${page.picker.selectedOptions[0].textContent}.` : 'Showing all locations.');
  const items = page.doc.querySelectorAll('[data-menu-item]');
  assert.ok(items.length >= 2, 'Actual rendered fixture needs location-specific dishes');
  for (const item of items) {
    const shouldShow = !expected || !item.dataset.locations || item.dataset.locations.split(' ').includes(expected);
    assert.equal(item.hidden, !shouldShow, `Dish ${item.id} must follow location filter`);
  }
  const contextLinks = page.doc.querySelectorAll('[data-context-link]');
  assert.ok(contextLinks.length > 0);
  for (const link of contextLinks) {
    const url = new URL(link.href);
    assert.equal(url.origin, page.location.origin);
    assert.equal(url.searchParams.get('location') || '', expected, 'Context links follow restored menu choice');
  }
  const visible = items.filter(item => !item.hidden).length;
  assert.equal(page.doc.querySelector('#menu-status').textContent, `${visible} dishes shown.`);
}

const scenarios = {
  roundtrip_first(preset) {
    const storage = new Map(); const first = openDocument(preset, storage); const chosen = first.choices[0];
    first.picker.value = chosen; first.picker.dispatchEvent({ type: 'change' }); assertState(first, chosen);
    assert.equal(first.location.searchParams.get('location'), chosen);
    const reopened = openDocument(preset, storage); assert.equal(reopened.location.search, '', 'Revisit must be query-free'); assertState(reopened, chosen);
  },
  roundtrip_second(preset) {
    const storage = new Map(); const first = openDocument(preset, storage); const chosen = first.choices[1];
    first.picker.value = chosen; first.picker.dispatchEvent({ type: 'change' }); assertState(first, chosen);
    assert.equal(first.location.searchParams.get('location'), chosen);
    const reopened = openDocument(preset, storage); assert.equal(reopened.location.search, '', 'Revisit must be query-free'); assertState(reopened, chosen);
  },
  invalid_saved(preset) {
    const storage = new Map([['he-location', 'not-a-valid-location']]); const page = openDocument(preset, storage); assertState(page, ''); assert.equal(storage.has('he-location'), false);
  },
  valid_query_override(preset) {
    const probe = openDocument(preset, new Map()); const storage = new Map([['he-location', probe.choices[0]]]);
    const page = openDocument(preset, storage, `?location=${encodeURIComponent(probe.choices[1])}`); assertState(page, probe.choices[1]);
  },
  invalid_and_empty_query(preset) {
    const probe = openDocument(preset, new Map());
    for (const query of ['?location=not-a-valid-location', '?location=']) {
      const storage = new Map([['he-location', probe.choices[0]]]); const page = openDocument(preset, storage, query); assertState(page, ''); assert.equal(storage.has('he-location'), false);
    }
  },
};

function crossRoute(preset, routeName, choiceIndex) {
  const storage = new Map();
  const start = openDocument(preset, storage);
  const invalid = choiceIndex === 'invalid';
  const selected = invalid ? 'unknown-stored-location' : start.choices[choiceIndex];
  if (invalid) {
    assert.ok(!start.choices.includes(selected));
    storage.set('he-location', selected); // Deliberately corrupted saved value.
  } else {
    start.picker.value = selected;
    start.picker.dispatchEvent({ type: 'change' });
    assertState(start, selected);
  }
  const expectedPath = input.documents[preset][routeName].route;
  const outward = start.doc.querySelectorAll('a[href]').find(link => new URL(link.href).pathname === expectedPath);
  assert.ok(outward, `Actual Menu must link to the ${routeName} route`);
  if (routeName === 'privacy') assert.equal(new URL(outward.href).search, '', 'Footer Privacy navigation is query-free');
  // Exercise clean entry to an actual no-selector route. Gallery has a contextual
  // link, so this explicitly models its clean URL; Privacy's footer is already clean.
  const intermediate = openDocument(preset, storage, '', routeName);
  assert.equal(intermediate.location.pathname, new URL(outward.href).pathname);
  assert.equal(intermediate.location.search, '');
  const hasHeaderAuthority = intermediate.doc.querySelectorAll('[data-location-option]').length > 0;
  assert.equal(hasHeaderAuthority, preset === 'kitchen-sink');
  const middleValue = invalid && hasHeaderAuthority ? '' : selected;
  assert.equal(storage.get('he-location') || '', middleValue, invalid
    ? 'No-authority page must defer invalid-value validation; authoritative header must reject it'
    : 'Valid menu selection must survive the no-selector route');
  const menuPath = input.documents[preset].menu.route;
  const back = intermediate.doc.querySelectorAll('[data-context-link]').find(link => new URL(link.href).pathname === menuPath);
  assert.ok(back, 'Actual intermediate page must link back to Menu');
  const backUrl = new URL(back.href);
  assert.equal(backUrl.searchParams.get('location') || '', middleValue, 'Actual return link follows deferred context');
  const expected = invalid ? '' : selected;
  const returned = openDocument(preset, storage, backUrl.search);
  assertState(returned, expected);
  if (invalid) assert.equal(storage.has('he-location'), false, 'Menu must reject the deferred invalid stored value');
  const clean = openDocument(preset, storage);
  assert.equal(clean.location.search, '', 'Final independent Menu revisit must be query-free');
  assertState(clean, expected);
}

const results = [];
for (const preset of ['food-truck', 'kitchen-sink']) {
  for (const [name, run] of Object.entries(scenarios)) {
    const id = `${preset}:${name}`;
    try { run(preset); results.push({ id, status: 'pass' }); }
    catch (error) { results.push({ id, status: 'fail', message: error.message, stack: error.stack }); }
  }
  for (const routeName of ['privacy', 'gallery']) {
    for (const choice of [0, 1, 'invalid']) {
      const id = `${preset}:menu_${routeName}_menu_${choice === 'invalid' ? 'invalid' : choice === 0 ? 'first' : 'second'}`;
      try { crossRoute(preset, routeName, choice); results.push({ id, status: 'pass' }); }
      catch (error) { results.push({ id, status: 'fail', message: error.message, stack: error.stack }); }
    }
  }
}
const failed = results.filter(result => result.status === 'fail').length;
console.log(JSON.stringify({ status: failed ? 'fail' : 'pass', runtimeCases: results.length, existingMenuCases: 10, crossRouteCases: 12, passed: results.length - failed, failed, queryClearSubcasesPerMount: 2, crossRoutePages: ['privacy', 'gallery'], actualEntireScript: true, actualGeneratedHtml: true, browserExecuted: false, adapterLimits: 'Minimal element/query/select/direct-event/storage/history adapter; no native DOM, layout, focus, native storage, external-resource or browser acceptance. Cross-route cases enter actual Privacy and Gallery at their clean URLs, follow the actual contextual Menu return link, and independently revisit clean Menu.', results }, null, 2));
process.exitCode = failed ? 1 : 0;
