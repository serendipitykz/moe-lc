const slides = Array.from(document.querySelectorAll('.slide'));
const counter  = document.getElementById('counter');
const prevBtn  = document.getElementById('prev');
const nextBtn  = document.getElementById('next');
const progress = document.getElementById('prog');

let current = 0;

/* Set each slide rail's vfill to reflect its position in the deck */
slides.forEach((sl, i) => {
  const vf = sl.querySelector('.vfill');
  if (vf) vf.style.height = `${(i + 1) / slides.length * 100}%`;
});

function go(n) {
  slides[current].classList.remove('on');
  current = Math.max(0, Math.min(n, slides.length - 1));
  slides[current].classList.add('on');
  counter.textContent = `${current + 1} / ${slides.length}`;
  prevBtn.disabled = current === 0;
  nextBtn.disabled = current === slides.length - 1;
  progress.style.width = `${(current + 1) / slides.length * 100}%`;
}

document.addEventListener('keydown', e => {
  if (['ArrowRight', 'ArrowDown', ' '].includes(e.key)) { e.preventDefault(); go(current + 1); }
  else if (['ArrowLeft', 'ArrowUp'].includes(e.key))    { e.preventDefault(); go(current - 1); }
});

prevBtn.addEventListener('click', () => go(current - 1));
nextBtn.addEventListener('click', () => go(current + 1));

go(0);
