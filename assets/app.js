'use strict';
const input = document.querySelector('#search');
const cards = [...document.querySelectorAll('.article-card')];
const buttons = [...document.querySelectorAll('[data-filter]')];
let selected = 'all';
function filterArticles() {
  const query = (input?.value || '').trim().toLocaleLowerCase();
  let count = 0;
  for (const card of cards) {
    const visible = (selected === 'all' || card.dataset.category === selected) && card.dataset.search.toLocaleLowerCase().includes(query);
    card.hidden = !visible;
    if (visible) count++;
  }
  const status = document.querySelector('.result-count');
  if (status) status.textContent = `共 ${count} 篇，按理解顺序排列`;
  const empty = document.querySelector('#empty');
  if (empty) empty.hidden = count !== 0;
}
for (const button of buttons) {
  button.addEventListener('click', () => {
    selected = button.dataset.filter;
    for (const item of buttons) {
      const active = item === button;
      item.classList.toggle('active', active);
      item.setAttribute('aria-pressed', String(active));
    }
    filterArticles();
  });
}
input?.addEventListener('input', filterArticles);
const termInput = document.querySelector('#term-search');
termInput?.addEventListener('input', () => {
  const query = termInput.value.trim().toLocaleLowerCase();
  let visible = 0;
  for (const term of document.querySelectorAll('[data-term]')) {
    term.hidden = !term.dataset.term.includes(query);
    if (!term.hidden) visible++;
  }
  document.querySelector('#term-empty').hidden = visible !== 0;
});
