/* Local guide tools. Component markup remains usable without this enhancement. */
(() => {
  'use strict';
  const guide = document.querySelector('.style-guide');
  if (!guide) return;
  const cards = [...guide.querySelectorAll('[data-kit-component]')];
  const query = guide.querySelector('#component-query');
  const groups = [...guide.querySelectorAll('[data-kit-group]')];
  const palette = guide.querySelector('#kit-palette');
  const width = guide.querySelector('#kit-width');
  const status = guide.querySelector('#component-status');
  let group = 'All';

  function showLayouts(card) {
    const choice = card.querySelector('[data-layout-choice]');
    const compare = card.querySelector('[data-layout-compare]').getAttribute('aria-pressed') === 'true';
    const panels = [...card.querySelectorAll('[data-layout-panel]')];
    panels.forEach(panel => { panel.hidden = !compare && panel.dataset.layoutPanel !== choice.value; });
    card.querySelector('[data-layout-status]').textContent = compare
      ? `Showing all ${panels.length} layouts.` : `${choice.selectedOptions[0].textContent} layout shown.`;
  }
  cards.forEach(card => {
    const choice = card.querySelector('[data-layout-choice]');
    const compare = card.querySelector('[data-layout-compare]');
    choice.addEventListener('change', () => {
      compare.setAttribute('aria-pressed', 'false'); showLayouts(card);
    });
    compare.addEventListener('click', () => {
      compare.setAttribute('aria-pressed', String(compare.getAttribute('aria-pressed') !== 'true'));
      showLayouts(card);
    });
    card.querySelector('[data-layout-controls]').hidden = false;
    showLayouts(card);
  });

  function filter() {
    const words = query.value.trim().toLocaleLowerCase().split(/\s+/).filter(Boolean);
    let count = 0;
    cards.forEach(card => {
      card.hidden = !(group === 'All' || group === card.dataset.group) ||
        !words.every(word => card.dataset.search.toLocaleLowerCase().includes(word));
      if (!card.hidden) count++;
    });
    groups.forEach(button => button.setAttribute('aria-pressed', String(button.dataset.kitGroup === group)));
    status.textContent = `${count} of ${cards.length} components shown${group === 'All' ? '' : ` in ${group}`}.`;
    guide.querySelector('[data-kit-empty]').hidden = count !== 0;
  }
  function preview() {
    guide.querySelectorAll('.sg-demo').forEach(demo => { demo.dataset.accent = palette.value; });
    guide.dataset.previewWidth = width.value;
  }
  function reset() {
    query.value = ''; group = 'All'; palette.value = ''; width.value = 'roomy';
    cards.forEach(card => {
      card.querySelector('[data-layout-choice]').value = card.dataset.presetLayout || 'default';
      card.querySelector('[data-layout-compare]').setAttribute('aria-pressed', 'false');
      showLayouts(card);
    });
    filter(); preview();
  }
  query.addEventListener('input', filter);
  groups.forEach(button => button.addEventListener('click', () => { group = button.dataset.kitGroup; filter(); }));
  palette.addEventListener('change', preview);
  width.addEventListener('change', preview);
  guide.querySelectorAll('[data-kit-reset]').forEach(button => button.addEventListener('click', () => {
    reset(); query.focus();
  }));

  // Direct links reveal both filtered components and unselected layouts.
  function revealTarget(id) {
    const target = document.getElementById(id);
    const card = target?.closest('[data-kit-component]');
    if (!card) return;
    if (card.hidden) { query.value = ''; group = 'All'; filter(); }
    const panel = target.closest('[data-layout-panel]');
    if (panel?.hidden) {
      card.querySelector('[data-layout-choice]').value = panel.dataset.layoutPanel;
      card.querySelector('[data-layout-compare]').setAttribute('aria-pressed', 'false');
      showLayouts(card);
    }
    return target;
  }
  function revealHash() {
    let id;
    try { id = decodeURIComponent(location.hash.slice(1)); } catch { return; }
    revealTarget(id)?.scrollIntoView({ block: 'start' });
  }
  window.addEventListener('hashchange', revealHash);
  guide.addEventListener('click', event => {
    const link = event.target.closest('a[href^="#component-"], a[href^="#layout-"]');
    if (!link) return;
    revealTarget(link.getAttribute('href').slice(1));
  });

  const copyStatus = guide.querySelector('#kit-copy-status');
  guide.querySelectorAll('[data-copy]').forEach(button => {
    button.hidden = false;
    button.addEventListener('click', async () => {
      const code = document.getElementById(button.dataset.copy);
      const label = button.dataset.copyLabel || button.textContent;
      button.dataset.copyLabel = label;
      copyStatus.textContent = '';
      try {
        if (!navigator.clipboard?.writeText) throw new Error('Clipboard unavailable');
        await navigator.clipboard.writeText(code.textContent);
        button.textContent = 'Copied';
        copyStatus.textContent = 'Copied to clipboard.';
      } catch {
        const selection = window.getSelection();
        const range = document.createRange();
        range.selectNodeContents(code);
        selection.removeAllRanges(); selection.addRange(range);
        code.setAttribute('tabindex', '-1'); code.focus();
        button.textContent = 'Code selected — use Copy';
        copyStatus.textContent = 'Clipboard unavailable. Code selected; use your device’s Copy command.';
      }
      setTimeout(() => { button.textContent = label; }, 2500);
    });
  });
  guide.querySelector('[data-kit-controls]').hidden = false;
  filter(); preview(); revealHash();
})();

/* The design studio uses independent, statically rendered restaurant pages. */
(() => {
  'use strict';
  const studio = document.querySelector('[data-preset-studio]');
  if (!studio) return;
  const presets = JSON.parse(studio.dataset.presets);
  const current = presets.find(p => p.id === studio.dataset.currentPreset);
  if (!current) return;
  const byId = id => presets.find(p => p.id === id);
  const page = studio.querySelector('#design-page');
  const width = studio.querySelector('#design-width');
  const compare = studio.querySelector('#design-compare');
  const against = studio.querySelector('#design-against');
  const frames = [...studio.querySelectorAll('[data-design-frame]')];
  const params = new URLSearchParams(location.search);
  let comparing = Boolean(byId(params.get('compare')));
  against.value = byId(params.get('compare'))?.id || presets.find(p => p.id !== current.id).id;
  if (against.value === current.id) against.value = presets.find(p => p.id !== current.id).id;
  [...against.options].forEach(option => { option.disabled = option.value === current.id; });
  width.value = ['phone', 'desktop'].includes(params.get('width')) ? params.get('width') : (window.matchMedia('(max-width: 700px)').matches ? 'phone' : 'desktop');
  let selectedPage = params.get('page') || '';

  function fitFrames() {
    const screen = width.value === 'phone' ? { width: 390, height: 780 } : { width: 1280, height: 900 };
    frames.forEach(panel => {
      if (panel.hidden) return;
      const mat = panel.querySelector('.sg-frame-mat');
      const viewport = panel.querySelector('.sg-frame-viewport');
      const frame = panel.querySelector('iframe');
      const scale = Math.min(1, mat.clientWidth / screen.width);
      frame.style.width = `${screen.width}px`;
      frame.style.height = `${screen.height}px`;
      frame.style.transform = `scale(${scale})`;
      viewport.style.width = `${screen.width * scale}px`;
      viewport.style.height = `${screen.height * scale}px`;
    });
  }

  function remember() {
    const url = new URL(location.href);
    for (const [key, value] of [['compare', comparing ? against.value : ''], ['page', selectedPage], ['width', width.value]]) {
      if (value) url.searchParams.set(key, value); else url.searchParams.delete(key);
    }
    history.replaceState(null, '', url);
    studio.querySelectorAll('[data-design-link]').forEach(link => {
      const next = new URL(link.href);
      next.search = '';
      for (const key of ['compare', 'page', 'width']) if (url.searchParams.has(key)) next.searchParams.set(key, url.searchParams.get(key));
      if (next.searchParams.get('compare') === link.dataset.designLink) next.searchParams.set('compare', current.id);
      link.href = next.href;
    });
  }

  function showFrame(panel, preset) {
    const frame = panel.querySelector('iframe');
    const route = preset.routes.find(r => r.path === selectedPage);
    const url = new URL(preset.url + route.path, location.href);
    if (frame.dataset.requested !== url.href) panel.querySelector('[data-frame-label]').textContent = `${preset.label} · ${route.label}`;
    panel.querySelector('[data-frame-title]').textContent = preset.name;
    if (frame.dataset.requested !== url.href) panel.querySelector('[data-frame-open]').href = url.href;
    if (frame.dataset.requested !== url.href) frame.title = `${preset.label} restaurant — ${route.label} preview`;
    // Changing width alone preserves the page's current scroll position and inputs.
    if (frame.dataset.requested !== url.href) {
      frame.dataset.requested = url.href;
      frame.src = url.href;
    }
  }

  function render() {
    const other = byId(against.value);
    const routes = current.routes.filter(r => !comparing || other.routes.some(o => o.path === r.path));
    const previousPage = selectedPage;
    if (!routes.some(r => r.path === selectedPage)) selectedPage = '';
    page.replaceChildren(...routes.map(r => new Option(r.label, r.path)));
    page.value = selectedPage;
    compare.setAttribute('aria-pressed', String(comparing));
    compare.textContent = comparing ? 'Show one design' : 'Compare two designs';
    studio.querySelector('[data-compare-control]').hidden = !comparing;
    studio.querySelector('[data-design-frames]').dataset.comparing = String(comparing);
    frames[1].hidden = !comparing;
    showFrame(frames[0], current);
    if (comparing) showFrame(frames[1], other);
    else if (frames[1].querySelector('iframe').hasAttribute('src')) {
      frames[1].querySelector('iframe').removeAttribute('src');
      delete frames[1].querySelector('iframe').dataset.requested;
    }
    const label = routes.find(r => r.path === selectedPage).label;
    studio.querySelector('#design-status').textContent = `${comparing ? `${current.label} and ${other.label}` : current.label} · ${label} · ${width.value === 'phone' ? '390' : '1280'} px.${comparing ? ' Only pages available in both designs are listed.' : ''}${previousPage !== selectedPage ? ' Switched to Home because the previous page is unavailable.' : ''}`;
    fitFrames(); remember();
  }

  frames.forEach(panel => {
    const frame = panel.querySelector('iframe');
    frame.addEventListener('load', () => {
      if (!frame.hasAttribute('src')) return;
      try {
        const url = new URL(frame.contentWindow.location.href);
        if (url.origin !== location.origin || !frame.contentDocument.body.dataset.preset) return;
        if (frame.dataset.requested !== url.href) panel.querySelector('[data-frame-open]').href = url.href;
        const heading = frame.contentDocument.querySelector('main h1');
        const preset = byId(frame.contentDocument.body.dataset.preset);
        const relative = url.pathname.slice(new URL(preset.url, location.href).pathname.length);
        const route = preset.routes.find(r => r.path === relative);
        panel.querySelector('[data-frame-label]').textContent = `${preset.label} · ${route?.label || heading?.textContent.trim() || 'Page'}`;
        if (heading) frame.title = `${preset.label} restaurant — ${heading.textContent.trim()} preview`;
      } catch { /* The full-page link remains available if a provider opens cross-origin. */ }
    });
  });
  compare.addEventListener('click', () => { comparing = !comparing; render(); });
  against.addEventListener('change', render);
  page.addEventListener('change', () => { selectedPage = page.value; render(); });
  width.addEventListener('change', render);
  studio.querySelector('#design-reset-pages').addEventListener('click', () => {
    frames.forEach(panel => { delete panel.querySelector('iframe').dataset.requested; });
    render();
  });
  studio.querySelector('[data-studio-controls]').hidden = false;
  if (window.ResizeObserver) new ResizeObserver(fitFrames).observe(studio.querySelector('[data-design-frames]'));
  else window.addEventListener('resize', fitFrames);
  render();
})();
