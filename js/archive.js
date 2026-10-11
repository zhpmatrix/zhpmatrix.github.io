const form = document.querySelector('.archive-filters');
const query = document.querySelector('#archive-query');
const tag = document.querySelector('#archive-tag');
const year = document.querySelector('#archive-year');
const items = [...document.querySelectorAll('.archive-list .reading-item')];
form.hidden = false;
function filterArticles() {
  const keyword = query.value.trim().toLocaleLowerCase();
  let count = 0;
  items.forEach(item => {
    const matches = `${item.querySelector('h3').textContent} ${item.querySelector('.reading-summary').textContent}`.toLocaleLowerCase().includes(keyword)
      && (!year.value || item.dataset.year === year.value)
      && (!tag.value || JSON.parse(item.dataset.tags || '[]').includes(tag.value));
    item.hidden = !matches;
    if (matches) count += 1;
  });
  document.querySelector('#archive-status').textContent = `共 ${count} 篇文章`;
  document.querySelector('#archive-empty').hidden = count !== 0;
}
form.addEventListener('submit', event => event.preventDefault());
form.addEventListener('input', filterArticles);
form.addEventListener('reset', () => requestAnimationFrame(filterArticles));
