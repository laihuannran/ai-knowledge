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

// Book directory filtering preserves the relationship between parts, chapters and sections.
const bookSearch = document.querySelector('#book-search');
const bookParts = [...document.querySelectorAll('.book-part')];
function openHashPart() {
  if (!location.hash) return;
  const target = document.getElementById(decodeURIComponent(location.hash.slice(1)));
  if (target?.matches('.book-part')) target.open = true;
  const parent = target?.closest('.book-part');
  if (parent) parent.open = true;
}
openHashPart();
window.addEventListener('hashchange', openHashPart);
bookSearch?.addEventListener('input', () => {
  const query = bookSearch.value.trim().toLocaleLowerCase();
  let count = 0;
  for (const part of bookParts) {
    let partCount = 0;
    for (const chapter of part.querySelectorAll('.book-chapter')) {
      let chapterCount = 0;
      for (const item of chapter.querySelectorAll('[data-book-search]')) {
        item.hidden = !item.dataset.bookSearch.toLocaleLowerCase().includes(query);
        if (!item.hidden) chapterCount++;
      }
      chapter.hidden = chapterCount === 0;
      partCount += chapterCount;
    }
    part.hidden = partCount === 0;
    if (query && partCount) part.open = true;
    count += partCount;
  }
  document.querySelector('#book-results').textContent = query ? `找到 ${count} 节相关内容` : '所有章节按理解顺序排列';
  document.querySelector('#book-empty').hidden = count !== 0;
});
document.querySelector('#expand-toc')?.addEventListener('click', () => bookParts.forEach(part => { part.open = true; }));
document.querySelector('#collapse-toc')?.addEventListener('click', () => bookParts.forEach(part => { part.open = false; }));
const menuButton = document.querySelector('.mobile-menu');
menuButton?.addEventListener('click', () => {
  const open = document.body.classList.toggle('nav-open');
  menuButton.setAttribute('aria-expanded', String(open));
});

// Project search is independent of article topic filters.
const projectInput = document.querySelector('#project-search');
const projectCards = [...document.querySelectorAll('.project-card')];
const projectButtons = [...document.querySelectorAll('[data-project-filter]')];
let projectRole = 'all';
function filterProjects() {
  const query = (projectInput?.value || '').trim().toLocaleLowerCase();
  let count = 0;
  for (const card of projectCards) {
    const visible = (projectRole === 'all' || projectRole.split(',').includes(card.dataset.role)) && card.dataset.projectSearch.toLocaleLowerCase().includes(query);
    card.hidden = !visible;
    if (visible) count++;
  }
  for (const button of projectButtons) {
    const active = button.dataset.projectFilter === projectRole;
    button.classList.toggle('active', active);
    button.setAttribute('aria-pressed', String(active));
  }
  const result = document.querySelector('#project-results');
  if (result) result.textContent = `共 ${count} 个项目，按技术职责组织`;
  const empty = document.querySelector('#project-empty');
  if (empty) empty.hidden = count !== 0;
}
projectInput?.addEventListener('input', filterProjects);
for (const button of projectButtons) button.addEventListener('click', () => { projectRole = button.dataset.projectFilter; filterProjects(); });
for (const link of document.querySelectorAll('[data-role-shortcut]')) {
  link.addEventListener('click', () => { projectRole = link.dataset.roleShortcut; filterProjects(); });
}

// API atlas search filters reference rows and detail cards together.
const apiInput = document.querySelector('#api-search');
apiInput?.addEventListener('input', () => {
  const query = apiInput.value.trim().toLocaleLowerCase();
  for (const item of document.querySelectorAll('[data-api-search]')) {
    item.hidden = !item.dataset.apiSearch.includes(query);
  }
  const count = [...document.querySelectorAll('.api-profile')].filter(item => !item.hidden).length;
  document.querySelector('#api-results').textContent = `共 ${count} 种接入形态，按职责对照`;
  document.querySelector('#api-empty').hidden = count !== 0;
});
