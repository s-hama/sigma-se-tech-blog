/* Navigate between the page top and the shared mobile category/tag section. */
(() => {
    const menu = document.getElementById('exCollapsingNavbar2');
    const link = document.getElementById('category-tags-link');
    const destination = document.getElementById('category-tags');
    const topLink = document.getElementById('category-tags-top');
    const menuButton = document.querySelector('[data-bs-target="#exCollapsingNavbar2"]');
    if (!menu || !link || !destination || !topLink || !menuButton) return;

    const mobile = window.matchMedia('(max-width: 991.98px)');
    let pendingJump = false;

    const jump = () => {
        pendingJump = false;
        if (!mobile.matches) return;
        destination.focus({ preventScroll: true });
        const top = window.scrollY + destination.getBoundingClientRect().top - 70;
        window.scrollTo({ top, behavior: 'instant' });
    };

    menu.addEventListener('hidden.bs.collapse', (event) => {
        if (event.target === menu && pendingJump) jump();
    });

    link.addEventListener('click', (event) => {
        if (!mobile.matches || !window.bootstrap?.Collapse) return;
        event.preventDefault();
        pendingJump = true;
        if (menu.classList.contains('show')) {
            bootstrap.Collapse.getOrCreateInstance(menu, { toggle: false }).hide();
        } else if (!menu.classList.contains('collapsing')) {
            jump();
        }
    });

    topLink.addEventListener('click', (event) => {
        event.preventDefault();
        menuButton.focus({ preventScroll: true });
        window.scrollTo({ top: 0, behavior: 'instant' });
    });

    mobile.addEventListener('change', () => {
        if (!mobile.matches) {
            pendingJump = false;
        }
    });
})();
