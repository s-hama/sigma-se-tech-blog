/* Keep the author on a separate row when the two dates wrap. */
(() => {
    const rows = document.querySelectorAll('.article-detail .post-meta-dates-separated');
    if (!rows.length) return;

    const update = (row) => {
        const dates = row.querySelectorAll('.post-date');
        if (dates.length !== 2) return;
        const wrapped = Math.abs(
            dates[0].getBoundingClientRect().top - dates[1].getBoundingClientRect().top
        ) > 1;
        row.classList.toggle('post-meta-dates-wrapped', wrapped);
        const author = row.querySelector('.post-author');
        if (author) {
            row.classList.toggle('post-meta-author-wrapped',
                author.getBoundingClientRect().top - dates[1].getBoundingClientRect().top > 1);
        }
    };

    const observer = new ResizeObserver((entries) => {
        entries.forEach(({ target }) => update(target));
    });
    rows.forEach((row) => {
        update(row);
        observer.observe(row);
    });
})();
