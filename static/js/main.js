const container = document.getElementById('container');
const registerBtn = document.getElementById('register');
const loginBtn = document.getElementById('login');

registerBtn.addEventListener('click', () => {
  container.classList.add("active");
});

loginBtn.addEventListener('click', () => {
  container.classList.remove("active");
});

document.addEventListener('DOMContentLoaded', () => {
  // Small toast auto-hide
  document.querySelectorAll('.toast-item').forEach(t => setTimeout(()=> t.remove(), 3800));

  // Voice button placeholder with premium microcopy
  const vb = document.getElementById('voiceBtn');
  if (vb) {
    vb.addEventListener('click', () => {
      // Gentle modal-style prompt (native)
      alert('Voice navigation demo — integrate Speech-to-Text to enable voice search. Try: "Find a plumber in Lucknow"');
    });
  }

  // Language button placeholder
  const lb = document.getElementById('langBtn');
  if (lb) {
    lb.addEventListener('click', () => {
      alert('Language selector demo — integrate Flask-Babel / translations for full multilingual support.');
    });
  }

  // small chip click micro-interaction
  document.querySelectorAll('.chip').forEach(el => {
    el.addEventListener('click', () => {
      el.animate([{ transform: 'scale(1.02)' }, { transform: 'scale(1)' }], { duration: 260 });
    });
  });
});

