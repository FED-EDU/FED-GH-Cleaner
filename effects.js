(() => {
  const root = document.documentElement;
  const reduced = matchMedia('(prefers-reduced-motion: reduce)').matches;
  const progress = document.querySelector('.scroll-progress');
  const updateProgress = () => {
    if (!progress) return;
    const max = Math.max(1, document.documentElement.scrollHeight - innerHeight);
    progress.style.transform = `scaleX(${Math.min(1, scrollY / max)})`;
  };
  addEventListener('scroll', updateProgress, { passive: true });
  updateProgress();

  const saved = localStorage.getItem('gh-cleaner-theme');
  if (saved) root.dataset.theme = saved;
  document.querySelector('[data-theme-toggle]')?.addEventListener('click', () => {
    const next = root.dataset.theme === 'light' ? 'dark' : 'light';
    root.dataset.theme = next;
    localStorage.setItem('gh-cleaner-theme', next);
  });

  if (!reduced && 'IntersectionObserver' in window) {
    const observer = new IntersectionObserver((entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          entry.target.classList.add('is-visible');
          observer.unobserve(entry.target);
        }
      });
    }, { threshold: 0.12 });
    document.querySelectorAll('[data-reveal]').forEach((element) => observer.observe(element));
  } else {
    document.querySelectorAll('[data-reveal]').forEach((element) => element.classList.add('is-visible'));
  }

  document.querySelectorAll('a[href^="#"]').forEach((link) => link.addEventListener('click', (event) => {
    const target = document.querySelector(link.getAttribute('href'));
    if (!target) return;
    event.preventDefault();
    target.scrollIntoView({ behavior: reduced ? 'auto' : 'smooth' });
  }));
})();
