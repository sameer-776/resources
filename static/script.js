document.addEventListener('DOMContentLoaded', () => {
    const API_BASE_URL = 'http://127.0.0.1:5000/api';

    // --- DOM Helpers ---
    const $ = (sel) => document.querySelector(sel);
    const $$ = (sel) => Array.from(document.querySelectorAll(sel));

    // --- Dynamic Content Loading ---
    const fetchLinks = async () => {
      const grid = $('#resourcesGrid');
      if (!grid) return;
      try {
        const response = await fetch(`${API_BASE_URL}/links`);
        const links = await response.json();
        grid.innerHTML = links.map(link => `
          <a href="${link.url}" class="resource-card" target="_blank" rel="noopener noreferrer">
            <img src="/static/uploads/${link.image}" alt="">
            <div class="title">${link.title}</div>
          </a>`).join('');
      } catch (error) {
        console.error("Failed to fetch links:", error);
        grid.innerHTML = '<p>Could not load resources.</p>';
      }
    };

    const fetchNotices = async () => {
      const track = $('#tickerTrack');
      if (!track) return;
      try {
        const response = await fetch(`${API_BASE_URL}/notices`);
        const notices = await response.json();
        const allNotices = notices.length > 0 ? [...notices, ...notices] : [{ text: "No new notices at the moment." }];
        track.innerHTML = allNotices.map(notice => `<div class="ticker-item">${notice.text}</div>`).join('');
      } catch (error) {
        console.error("Failed to fetch notices:", error);
        track.innerHTML = '<div class="ticker-item">Could not load notices.</div>';
      }
    };

    // --- UI Interactivity ---
    const yearEl = $('#year');
    if (yearEl) yearEl.textContent = new Date().getFullYear();

    const progress = $('#progress-bar');
    window.addEventListener('scroll', () => {
      if (document.body.scrollHeight <= window.innerHeight) return;
      const pct = (window.scrollY / (document.body.scrollHeight - window.innerHeight)) * 100;
      progress.style.width = `${Math.max(0, Math.min(100, pct))}%`;
    });

    let lastScroll = 0;
    const header = $('#site-header');
    window.addEventListener('scroll', () => {
      const s = window.scrollY;
      if (header) header.style.transform = (s > lastScroll && s > 80) ? 'translateY(-100%)' : 'translateY(0)';
      lastScroll = s;
    });

    const mobileMenu = $('#mobileMenu');
    const openMobile = () => mobileMenu.style.transform = 'translateX(0)';
    const closeMobile = () => mobileMenu.style.transform = 'translateX(100%)';
    $('#mobileBtn')?.addEventListener('click', openMobile);
    $('#mobileClose')?.addEventListener('click', closeMobile);
    $$('.mobile-link').forEach(link => link.addEventListener('click', closeMobile));

    $('#darkToggle')?.addEventListener('click', () => {
      document.documentElement.classList.toggle('dark');
      const icon = $('#darkToggle i');
      icon?.classList.toggle('fa-sun'); icon?.classList.toggle('fa-moon');
    });

    const observer = new IntersectionObserver((entries) => {
      entries.forEach(e => {
        if (e.isIntersecting) { e.target.classList.add('visible'); observer.unobserve(e.target); }
      });
    }, { threshold: 0.1 });
    $$('.reveal').forEach(el => observer.observe(el));

    const counterObserver = new IntersectionObserver((entries) => {
      entries.forEach(ent => {
        if (ent.isIntersecting) {
          const el = ent.target;
          const target = +el.dataset.target || 0;
          let cur = 0;
          const step = Math.max(1, Math.round(target / 100));
          const timer = setInterval(() => {
            cur += step;
            if (cur >= target) { el.textContent = target.toLocaleString(); clearInterval(timer); } 
            else { el.textContent = cur.toLocaleString(); }
          }, 12);
          counterObserver.unobserve(el);
        }
      });
    }, { threshold: 0.5 });
    $$('.stat-num').forEach(c => counterObserver.observe(c));

    $('#tickerTrack')?.addEventListener('mouseenter', (e) => e.target.style.animationPlayState = 'paused');
    $('#tickerTrack')?.addEventListener('mouseleave', (e) => e.target.style.animationPlayState = 'running');
    
    // --- Photo Gallery ---
    const setupGallery = async () => {
        const gTrack = $('#galleryTrack');
        if (!gTrack) return;

        try {
            const response = await fetch(`${API_BASE_URL}/gallery`);
            const images = await response.json();
            
            if (images.length === 0) {
                const galleryViewport = $('.gallery-viewport');
                if(galleryViewport) galleryViewport.innerHTML = '<p style="text-align: center; padding: 2rem;">No gallery images have been uploaded yet.</p>';
                return;
            }

            gTrack.innerHTML = images.map(img => 
                `<div class="gallery-slide"><img src="/static/uploads/${img.filename}" alt="Gallery image"></div>`
            ).join('');

            let gIndex = 0;
            let gTimer = null;
            const slides = gTrack.children;

            const updateTrack = () => gTrack.style.transform = `translateX(-${gIndex * 100}%)`;
            const nextSlide = () => { gIndex = (gIndex + 1) % slides.length; updateTrack(); };
            const prevSlide = () => { gIndex = (gIndex - 1 + slides.length) % slides.length; updateTrack(); };
            const startAuto = () => { clearInterval(gTimer); gTimer = setInterval(nextSlide, 3500); };
            
            $('.gallery-nav.next')?.addEventListener('click', () => { nextSlide(); startAuto(); });
            $('.gallery-nav.prev')?.addEventListener('click', () => { prevSlide(); startAuto(); });
            gTrack.addEventListener('mouseenter', () => clearInterval(gTimer));
            gTrack.addEventListener('mouseleave', startAuto);
            
            startAuto();
            
        } catch (error) {
            console.error('Failed to load gallery images:', error);
            const galleryViewport = $('.gallery-viewport');
            if(galleryViewport) galleryViewport.innerHTML = '<p style="text-align: center; padding: 2rem;">Could not load the gallery at this time.</p>';
        }
    };
    
    // --- Initializations ---
    fetchLinks();
    fetchNotices();
    setupGallery();
});