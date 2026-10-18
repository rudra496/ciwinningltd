/* ============================================================
   CI WINNING LTD — site interactions
   ============================================================ */
(function () {
  "use strict";

  document.documentElement.classList.add("js");

  var prefersReduced = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  /* ---------- Scroll progress ---------- */
  var progress = document.getElementById("scroll-progress");
  function onScrollProgress() {
    if (!progress) return;
    var h = document.documentElement;
    var max = h.scrollHeight - h.clientHeight;
    progress.style.width = (max > 0 ? (h.scrollTop / max) * 100 : 0) + "%";
  }

  /* ---------- Sticky header ---------- */
  var header = document.querySelector(".site-header");
  function onHeaderScroll() {
    if (!header) return;
    header.classList.toggle("is-scrolled", window.scrollY > 8);
  }

  /* ---------- Back to top ---------- */
  var fabTop = document.querySelector(".fab--top");
  function onFabTop() {
    if (!fabTop) return;
    fabTop.classList.toggle("is-visible", window.scrollY > 650);
  }

  var ticking = false;
  window.addEventListener("scroll", function () {
    if (ticking) return;
    ticking = true;
    window.requestAnimationFrame(function () {
      onScrollProgress();
      onHeaderScroll();
      onFabTop();
      ticking = false;
    });
  }, { passive: true });
  onScrollProgress(); onHeaderScroll(); onFabTop();

  if (fabTop) {
    fabTop.addEventListener("click", function () {
      window.scrollTo({ top: 0, behavior: prefersReduced ? "auto" : "smooth" });
    });
  }

  /* ---------- Mobile menu ---------- */
  var mobileMenu = document.getElementById("mobile-menu");
  var navToggle = document.querySelector(".nav__toggle");
  if (mobileMenu && navToggle) {
    var closeBtn = mobileMenu.querySelector(".mobile-menu__close");
    var backdrop = mobileMenu.querySelector(".mobile-menu__backdrop");
    function openMenu() {
      mobileMenu.classList.add("is-open");
      navToggle.setAttribute("aria-expanded", "true");
      document.body.style.overflow = "hidden";
      var first = mobileMenu.querySelector("a, button");
      if (first) first.focus();
    }
    function closeMenu() {
      mobileMenu.classList.remove("is-open");
      navToggle.setAttribute("aria-expanded", "false");
      document.body.style.overflow = "";
      navToggle.focus();
    }
    navToggle.addEventListener("click", openMenu);
    if (closeBtn) closeBtn.addEventListener("click", closeMenu);
    if (backdrop) backdrop.addEventListener("click", closeMenu);
    document.addEventListener("keydown", function (e) {
      if (e.key === "Escape" && mobileMenu.classList.contains("is-open")) closeMenu();
    });
    mobileMenu.querySelectorAll("a").forEach(function (a) {
      a.addEventListener("click", function () { closeMenu(); });
    });
  }

  /* ---------- Reveal on scroll ---------- */
  var revealEls = document.querySelectorAll(".reveal");
  function revealAll() {
    revealEls.forEach(function (el) { el.classList.add("is-visible"); });
  }
  if ("IntersectionObserver" in window && revealEls.length && !prefersReduced) {
    var revealIO = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) {
          entry.target.classList.add("is-visible");
          revealIO.unobserve(entry.target);
        }
      });
    }, { threshold: 0.08, rootMargin: "0px 0px 180px 0px" });
    var vh = window.innerHeight;
    revealEls.forEach(function (el) {
      var r = el.getBoundingClientRect();
      /* anything already on screen (or in print) shows instantly — never blank */
      if (r.top < vh && r.bottom > 0) {
        el.classList.add("is-visible");
      } else {
        revealIO.observe(el);
      }
    });
    window.addEventListener("beforeprint", revealAll);
  } else {
    revealAll();
  }

  /* ---------- Animated counters ---------- */
  var counters = document.querySelectorAll("[data-count]");
  function animateCounter(el) {
    var target = parseFloat(el.getAttribute("data-count"));
    var suffix = el.getAttribute("data-suffix") || "";
    if (prefersReduced || isNaN(target)) { el.textContent = target + suffix; return; }
    var dur = 1600, start = null;
    function step(ts) {
      if (!start) start = ts;
      var p = Math.min((ts - start) / dur, 1);
      var eased = 1 - Math.pow(1 - p, 3);
      el.textContent = Math.round(target * eased) + suffix;
      if (p < 1) window.requestAnimationFrame(step);
    }
    window.requestAnimationFrame(step);
  }
  if ("IntersectionObserver" in window && counters.length) {
    var countIO = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) {
          animateCounter(entry.target);
          countIO.unobserve(entry.target);
        }
      });
    }, { threshold: 0.5 });
    counters.forEach(function (el) { countIO.observe(el); });
  } else {
    counters.forEach(animateCounter);
  }

  /* ---------- Testimonial slider ---------- */
  var track = document.querySelector(".testi-track");
  if (track) {
    var slides = track.children;
    var dotsWrap = document.querySelector(".testi-dots");
    var current = 0, timer = null, DURATION = 6500;

    var dots = [];
    if (dotsWrap) {
      Array.prototype.forEach.call(slides, function (_, i) {
        var b = document.createElement("button");
        b.className = "testi-dot" + (i === 0 ? " is-active" : "");
        b.setAttribute("aria-label", "Go to testimonial " + (i + 1));
        b.addEventListener("click", function () { go(i, true); });
        dotsWrap.appendChild(b);
        dots.push(b);
      });
    }
    function go(i, user) {
      current = (i + slides.length) % slides.length;
      track.style.transform = "translateX(-" + current * 100 + "%)";
      dots.forEach(function (d, di) { d.classList.toggle("is-active", di === current); });
      if (user) restart();
    }
    function restart() {
      if (timer) clearInterval(timer);
      if (!prefersReduced) timer = setInterval(function () { go(current + 1); }, DURATION);
    }
    var prev = document.querySelector(".testi-btn--prev");
    var next = document.querySelector(".testi-btn--next");
    if (prev) prev.addEventListener("click", function () { go(current - 1, true); });
    if (next) next.addEventListener("click", function () { go(current + 1, true); });

    var wrap = document.querySelector(".testi-wrap");
    if (wrap) {
      wrap.addEventListener("mouseenter", function () { if (timer) clearInterval(timer); });
      wrap.addEventListener("mouseleave", restart);
      /* touch swipe */
      var startX = null;
      wrap.addEventListener("touchstart", function (e) { startX = e.touches[0].clientX; }, { passive: true });
      wrap.addEventListener("touchend", function (e) {
        if (startX === null) return;
        var dx = e.changedTouches[0].clientX - startX;
        if (Math.abs(dx) > 45) go(current + (dx < 0 ? 1 : -1), true);
        startX = null;
      }, { passive: true });
    }
    restart();
  }

  /* ---------- FAQ: keep one open at a time ---------- */
  var faqs = document.querySelectorAll(".faq-item");
  faqs.forEach(function (d) {
    d.addEventListener("toggle", function () {
      if (!d.open) return;
      faqs.forEach(function (other) { if (other !== d) other.open = false; });
    });
  });


  /* ---------- Footer year ---------- */
  var yr = document.getElementById("year");
  if (yr) yr.textContent = String(new Date().getFullYear());
})();
