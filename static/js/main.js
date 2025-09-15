const mobileMenu = document.getElementById('mobile-menu');
const navbar = document.getElementById('navbar');

mobileMenu.addEventListener('click', () => {
  navbar.classList.toggle('active');
});

// ---------------- Carousel & Animation ---------------- //
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

// Fade-in animation
const observer = new IntersectionObserver(entries => {
  entries.forEach(entry => {
    if (entry.isIntersecting) {
      entry.target.classList.add('active');
      observer.unobserve(entry.target);
    }
  });
}, { threshold: 0.2 });

cards.forEach(card => observer.observe(card));

// ---------------- Modal Functionality ---------------- //
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

// ---------------- Backend API Integration ---------------- //
const API_BASE = "https://educommerce-backend.onrender.com"; // ✅ Render backend

// Signup
// async function handleSignup(e) {
//   e.preventDefault();
//   const formData = new FormData(e.target);

//   try {
//     const res = await fetch(`${API_BASE}/signup`, {
//       method: "POST",
//       body: formData
//     });

//     const data = await res.text();
//     alert(data);
//   } catch (err) {
//     console.error(err);
//     alert("Signup failed. Please try again.");
//   }
// }

// Login
// async function handleLogin(e) {
//   e.preventDefault();
//   const formData = new FormData(e.target);

//   try {
//     const res = await fetch(`${API_BASE}/login`, {
//       method: "POST",
//       body: formData
//     });

//     const data = await res.text();
//     alert(data);
//   } catch (err) {
//     console.error(err);
//     alert("Login failed. Please try again.");
//   }
// }

// Load Courses
async function loadCourses() {
  try {
    let res = await fetch(`${API_BASE}/api/courses`);
    let courses = await res.json();

    let container = document.getElementById("courses");
    if (container) {
      container.innerHTML = courses.map(c => `<li>${c.title} - ${c.price}</li>`).join("");
    }
  } catch (err) {
    console.error(err);
  }
}

// Auto load courses if container exists
if (document.getElementById("courses")) {
  loadCourses();
}

// Attach event listeners if forms exist
const signupForm = document.getElementById("signup-form");
if (signupForm) signupForm.addEventListener("submit", handleSignup);

const loginForm = document.getElementById("login-form");
if (loginForm) loginForm.addEventListener("submit", handleLogin);
