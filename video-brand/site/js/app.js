// Abschnitte beim Scrollen mit animate.css einblenden
const io = new IntersectionObserver(es => es.forEach(e => {
  if (e.isIntersecting) { e.target.classList.add('animate__animated', 'animate__fadeInUp'); io.unobserve(e.target); }
}), { threshold: .2 });
document.querySelectorAll('.reveal').forEach(el => io.observe(el));
