document.addEventListener('DOMContentLoaded', () => {
    const userBtn = document.getElementById('userMenuBtn');
    const dropdown = document.getElementById('userDropdownMenu');

    if (!userBtn || !dropdown) return;

    // Toggle desktop dropdown
    userBtn.addEventListener('click', (e) => {
        e.stopPropagation();
        dropdown.classList.toggle('show');
    });

    document.addEventListener('click', (e) => {
        if (!dropdown.contains(e.target) && !userBtn.contains(e.target)) {
            dropdown.classList.remove('show');
        }
    });

    document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape') {
            dropdown.classList.remove('show');
        }
    });
});
