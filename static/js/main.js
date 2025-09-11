
const mobileMenu = document.getElementById('mobile-menu');
const navbar = document.getElementById('navbar');

mobileMenu.addEventListener('click', () => {
  navbar.classList.toggle('active');
});


// Carousel & Animation
const slider = document.querySelector('.testimonial-slider');
const cards = document.querySelectorAll('.testimonial-card');
let currentIndex = 0;

// Show slide function
function showSlide(index) {
  cards.forEach((card, i) => {
    card.classList.remove('active');
    if (i === index) card.classList.add('active');
  });
}

// Initial display
showSlide(currentIndex);

// Auto slide every 5 seconds
setInterval(() => {
  currentIndex = (currentIndex + 1) % cards.length;
  showSlide(currentIndex);
}, 5000);

// Optional: Fade-in when scrolling into view
const observer = new IntersectionObserver(entries => {
  entries.forEach(entry => {
    if (entry.isIntersecting) {
      entry.target.classList.add('active');
      observer.unobserve(entry.target); // animate once
    }
  });
}, { threshold: 0.2 });

cards.forEach(card => observer.observe(card));



// Modal Functionality
document.querySelectorAll('.instructor-card').forEach(card => {
  card.addEventListener('click', () => {
    const modalId = card.getAttribute('data-modal');
    document.getElementById(modalId).style.display = 'block';
  });
});

document.querySelectorAll('.close').forEach(closeBtn => {
  closeBtn.addEventListener('click', () => {
    closeBtn.closest('.modal').style.display = 'none';
  });
});

window.addEventListener('click', (e) => {
  if (e.target.classList.contains('modal')) {
    e.target.style.display = 'none';
  }
});



