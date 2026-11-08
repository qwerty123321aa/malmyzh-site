const reducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)');
const journey = document.querySelector('.ore-experience');

if (journey) {
  const steps = [...journey.querySelectorAll('[data-ore-step]')];
  const links = [...journey.querySelectorAll('[data-ore-link]')];
  const image = journey.querySelector('#ore-image');
  const credit = journey.querySelector('#ore-credit');
  const current = journey.querySelector('#ore-current');
  const progress = journey.querySelector('#ore-progress');
  let active = -1;
  let scheduled = false;

  function activate(index) {
    if (active === index) return;
    active = index;
    const step = steps[index];
    steps.forEach((item, i) => item.classList.toggle('is-active', i === index));
    links.forEach((link, i) => {
      if (i === index) link.setAttribute('aria-current', 'step');
      else link.removeAttribute('aria-current');
    });
    image.src = step.dataset.image;
    image.alt = step.dataset.alt;
    credit.href = step.dataset.source;
    credit.textContent = step.dataset.credit;
    current.textContent = links[index].textContent;
    progress.value = index + 1;
    if (!reducedMotion.matches) image.animate([{ opacity: 0.55 }, { opacity: 1 }], { duration: 280 });
  }

  function updateFromScroll() {
    scheduled = false;
    const target = window.innerHeight * 0.64;
    let index = 0;
    steps.forEach((step, i) => {
      if (step.getBoundingClientRect().top <= target) index = i;
    });
    activate(index);
  }

  links.forEach((link, index) => link.addEventListener('click', event => {
    event.preventDefault();
    steps[index].scrollIntoView({ behavior: reducedMotion.matches ? 'instant' : 'smooth', block: 'start' });
    history.replaceState(null, '', link.getAttribute('href'));
  }));
  function scheduleUpdate() {
    if (scheduled) return;
    scheduled = true;
    requestAnimationFrame(updateFromScroll);
  }
  window.addEventListener('scroll', scheduleUpdate, { passive: true });
  window.addEventListener('resize', scheduleUpdate);
  journey.classList.add('is-interactive');
  updateFromScroll();
}

const geology = document.querySelector('.geology-explorer');
if (geology) {
  const buttons = [...geology.querySelectorAll('[data-geo-target]')];
  const panels = [...geology.querySelectorAll('.geo-panel')];
  function selectFeature(button) {
    buttons.forEach(item => item.setAttribute('aria-pressed', String(item === button)));
    panels.forEach(panel => { panel.hidden = panel.id !== 'geo-' + button.dataset.geoTarget; });
    geology.dataset.activeFeature = button.dataset.geoTarget;
  }
  buttons.forEach(button => button.addEventListener('click', () => selectFeature(button)));
  selectFeature(buttons[0]);
}

const calculator = document.querySelector('.copper-calculator');
if (calculator) {
  const input = calculator.querySelector('#ore-mass');
  const range = calculator.querySelector('#ore-mass-range');
  const copper = calculator.querySelector('#copper-mass');
  const other = calculator.querySelector('#other-mass');
  const help = calculator.querySelector('#ore-mass-help');
  const presets = [...calculator.querySelectorAll('[data-mass]')];
  const format = new Intl.NumberFormat('ru-RU', { maximumFractionDigits: 3 });

  function update() {
    const mass = input.valueAsNumber;
    const valid = Number.isFinite(mass) && mass >= 0 && mass <= 10000;
    input.setAttribute('aria-invalid', String(!valid));
    help.textContent = valid ? 'От 0 до 10 000 тонн' : 'Введите массу от 0 до 10 000 тонн';
    copper.value = valid ? format.format(mass * 3.5) : '—';
    other.value = valid ? format.format(mass * 996.5) : '—';
    presets.forEach(button => button.setAttribute('aria-pressed', String(valid && Number(button.dataset.mass) === mass)));
    if (valid) range.value = mass;
  }
  input.addEventListener('input', update);
  range.addEventListener('input', () => { input.value = range.value; update(); });
  presets.forEach(button => button.addEventListener('click', () => { input.value = button.dataset.mass; update(); }));
  update();
}
