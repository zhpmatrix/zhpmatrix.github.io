const articleHeadings = [...document.querySelectorAll('#article-body h2, #article-body h3, #article-body h4, #article-body h5')];
if (articleHeadings.length >= 3) {
  const toc = document.querySelector('.article-toc');
  const list = document.querySelector('#toc-links');
  const baseLevel = Math.min(...articleHeadings.map(heading => Number(heading.tagName[1])));
  articleHeadings.forEach((heading, index) => {
    if (!heading.id) heading.id = `article-section-${index}`;
    const item = document.createElement('li');
    item.style.paddingLeft = `${Math.min(Number(heading.tagName[1]) - baseLevel, 2) * 12}px`;
    const link = document.createElement('a');
    link.href = `#${encodeURIComponent(heading.id)}`;
    link.textContent = heading.textContent;
    item.appendChild(link);
    list.appendChild(item);
  });
  toc.hidden = false;
  if (window.matchMedia('(max-width: 1200px)').matches) toc.querySelector('details').open = false;
}
