const slides  = Array.from(document.querySelectorAll('.slide'));
const counter  = document.getElementById('counter');
const prevBtn  = document.getElementById('prev');
const nextBtn  = document.getElementById('next');
const progress = document.getElementById('progress');

let current = 0;

function go(n) {
  slides[current].classList.remove('active');
  current = Math.max(0, Math.min(n, slides.length - 1));
  slides[current].classList.add('active');
  counter.textContent = `${current + 1} / ${slides.length}`;
  prevBtn.disabled = current === 0;
  nextBtn.disabled = current === slides.length - 1;
  progress.style.width = `${((current + 1) / slides.length) * 100}%`;
}

document.addEventListener('keydown', e => {
  if (['ArrowRight', 'ArrowDown', ' '].includes(e.key)) { e.preventDefault(); go(current + 1); }
  else if (['ArrowLeft', 'ArrowUp'].includes(e.key))    { e.preventDefault(); go(current - 1); }
});

prevBtn.addEventListener('click', () => go(current - 1));
nextBtn.addEventListener('click', () => go(current + 1));

go(0);
