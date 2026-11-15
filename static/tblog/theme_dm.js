(() => {
  const storageKey = 'sigma-se-theme';
  const root = document.documentElement;
  const imageStates = new WeakMap();
  let toggleButton;

  const readTheme = () => {
    try {
      return localStorage.getItem(storageKey) === 'dark' ? 'dark' : 'light';
    } catch (error) {
      return 'light';
    }
  };

  // This script runs synchronously in <head>, before styles or page content.
  // Only an explicit saved choice enables dark mode; OS preferences are ignored.
  root.dataset.bsTheme = readTheme();

  const updateButton = () => {
    if (!toggleButton) return;
    const label = root.dataset.bsTheme === 'dark'
      ? 'ライトモードに切り替える' : 'ダークモードに切り替える';
    toggleButton.setAttribute('aria-label', label);
    toggleButton.title = label;
  };

  const updateImage = (image) => {
    const source = image.getAttribute('src');
    if (!source) return;
    let state = imageStates.get(image);
    if (!state || (source !== state.light && source !== state.dark)) {
      // Match article assets only; leave photos, external SVGs and icons alone.
      let url;
      try {
        url = new URL(source, document.baseURI);
      } catch (error) {
        return;
      }
      if (url.origin !== location.origin || !/\/static\/tblog\/img\/pid\d+_\d+\.svg$/.test(url.pathname)) {
        imageStates.delete(image);
        delete image.dataset.themeSvg;
        image.classList.remove('theme-svg-pending-dm', 'theme-svg-fallback-dm');
        return;
      }
      state = {
        light: source,
        dark: source.replace(/\.svg(?=[?#]|$)/, '_dm.svg'),
        missing: false,
      };
      imageStates.set(image, state);
      image.dataset.themeSvg = '';
    }
    const dark = root.dataset.bsTheme === 'dark';
    const target = dark && !state.missing ? state.dark : state.light;
    image.classList.toggle('theme-svg-fallback-dm', dark && state.missing);
    if (!dark || state.missing) image.classList.remove('theme-svg-pending-dm');
    if (source === target) return;
    if (dark && !state.missing) image.classList.add('theme-svg-pending-dm');
    image.setAttribute('src', target);
  };

  // Process parser-inserted images before paint, including a saved dark theme.
  // Also supports article images inserted or replaced later without polling.
  const observer = new MutationObserver((records) => {
    const images = new Set();
    records.forEach((record) => {
      if (record.type === 'attributes' && record.target.tagName === 'IMG') {
        images.add(record.target);
      }
      record.addedNodes.forEach((node) => {
        if (node.nodeType !== Node.ELEMENT_NODE) return;
        if (node.tagName === 'IMG') images.add(node);
        node.querySelectorAll('img').forEach((image) => images.add(image));
      });
    });
    images.forEach(updateImage);
  });
  observer.observe(root, { childList: true, subtree: true, attributes: true, attributeFilter: ['src'] });

  document.addEventListener('load', (event) => {
    const image = event.target;
    if (image.tagName === 'IMG') image.classList.remove('theme-svg-pending-dm');
  }, true);
  document.addEventListener('error', (event) => {
    const image = event.target;
    const state = imageStates.get(image);
    if (state && image.getAttribute('src') === state.dark) {
      state.missing = true;
      // A missing future variant must not leave a broken or invisible figure.
      updateImage(image);
    }
  }, true);

  const applyTheme = (theme) => {
    root.dataset.bsTheme = theme;
    updateButton();
    document.querySelectorAll('img').forEach(updateImage);
  };

  document.addEventListener('DOMContentLoaded', () => {
    toggleButton = document.getElementById('theme-toggle-dm');
    if (toggleButton) {
      updateButton();
      toggleButton.hidden = false;
      toggleButton.addEventListener('click', () => {
        const theme = root.dataset.bsTheme === 'dark' ? 'light' : 'dark';
        applyTheme(theme);
        try {
          localStorage.setItem(storageKey, theme);
        } catch (error) {
          // Storage may be blocked; switching within this page still works.
        }
      });
    }
    document.querySelectorAll('img').forEach(updateImage);
  });

  window.addEventListener('storage', (event) => {
    if (event.key === storageKey || event.key === null) applyTheme(readTheme());
  });
  window.addEventListener('pageshow', (event) => {
    if (event.persisted) applyTheme(readTheme());
  });
})();
