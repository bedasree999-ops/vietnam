const viewer = document.querySelector('#viewer');
const fullPhoto = document.querySelector('#full-photo');
const caption = document.querySelector('#photo-caption');
let collection = [], current = 0;
function showPhoto(index) {
  current = (index + collection.length) % collection.length;
  const photo = collection[current];
  fullPhoto.src = photo.dataset.full;
  fullPhoto.alt = photo.querySelector('img').alt;
  caption.textContent = `${photo.dataset.place} / ${current + 1} of ${collection.length}`;
}
document.querySelectorAll('.photo').forEach(button => {
  button.addEventListener('click', () => {
    collection = [...button.closest('.gallery').querySelectorAll('.photo')];
    showPhoto(collection.indexOf(button));
    viewer.showModal();
    document.body.classList.add('viewer-open');
  });
});
document.querySelector('#close').addEventListener('click', () => viewer.close());
viewer.addEventListener('close', () => { document.body.classList.remove('viewer-open'); fullPhoto.removeAttribute('src'); });
document.querySelector('#previous').addEventListener('click', () => showPhoto(current - 1));
document.querySelector('#next').addEventListener('click', () => showPhoto(current + 1));
viewer.addEventListener('keydown', event => {
  if (event.key === 'ArrowLeft' || event.key === 'ArrowRight') {
    event.preventDefault(); showPhoto(current + (event.key === 'ArrowLeft' ? -1 : 1));
  }
});
let touchStart = null;
fullPhoto.addEventListener('touchstart', e => {touchStart = e.changedTouches[0].clientX;}, {passive:true});
fullPhoto.addEventListener('touchend', e => {
  if(touchStart === null) return;
  const distance = e.changedTouches[0].clientX - touchStart;
  if(Math.abs(distance)>50) showPhoto(current + (distance>0 ? -1 : 1));
  touchStart=null;
}, {passive:true});
document.querySelectorAll('.expand').forEach(button => {
  button.addEventListener('click', () => {
    const expanded = button.getAttribute('aria-expanded') === 'true';
    const section = button.closest('.chapter');
    const photos = [...section.querySelectorAll('.photo')];
    photos.forEach((photo,index) => {photo.hidden = !expanded ? false : index >= 6;});
    button.setAttribute('aria-expanded', String(!expanded));
    button.innerHTML = expanded ? `Explore all ${photos.length} photographs <span>＋</span>` : 'Show fewer photographs <span>−</span>';
    if(expanded) section.scrollIntoView({behavior:matchMedia('(prefers-reduced-motion: reduce)').matches?'instant':'smooth'});
  });
});
const observer = new IntersectionObserver(entries => {
  entries.forEach(entry => {
    if(entry.isIntersecting) {
      document.querySelectorAll('.places a').forEach(link => {
        const active = link.hash === `#${entry.target.id}`;
        link.classList.toggle('active', active);
        if(active) link.setAttribute('aria-current','location'); else link.removeAttribute('aria-current');
      });
    }
  });
},{rootMargin:'-10% 0px -60% 0px'});
document.querySelectorAll('.chapter').forEach(section => observer.observe(section));
