document.addEventListener("DOMContentLoaded", () => {
    const faders = document.querySelectorAll(".fade-up");

    const options = {
        threshold: 0.15,
    };

    const appearOnScroll = new IntersectionObserver((entries, observer) => {
        entries.forEach(entry => {
            if (!entry.isIntersecting) return;
            entry.target.classList.add("is-visible");
            observer.unobserve(entry.target);
        });
    }, options);

    faders.forEach(fader => {
        appearOnScroll.observe(fader);
    });
});

document.addEventListener("DOMContentLoaded", () => {

    /* ===== PROJECT DETAIL SECTIONS ===== */

    const sections = document.querySelectorAll(".project-section");

    const options = {
        threshold: 0.2
    };

    const revealOnScroll = new IntersectionObserver((entries, observer) => {
        entries.forEach(entry => {
            if (!entry.isIntersecting) return;
            entry.target.classList.add("is-visible");
            observer.unobserve(entry.target);
        });
    }, options);

    sections.forEach(section => {
        revealOnScroll.observe(section);
    });

});

document.addEventListener("DOMContentLoaded", () => {
    const form = document.querySelector(".contact-form");
    if (!form) return;

    form.addEventListener("reset", () => {
        document.querySelectorAll(
            ".form-error, .form-error-gen, .form-success"
        ).forEach(el => el.remove());
    });
});