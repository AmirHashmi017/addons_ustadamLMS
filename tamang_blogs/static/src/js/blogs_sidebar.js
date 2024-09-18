if (window.location.pathname.includes('/blog')) {
    const openBtn = document.getElementById('open-sidebar');
    const closeBtn = document.getElementById('close-sidebar');
    const sidebar = document.getElementById('blog-sidebar');

    // Open sidebar when hamburger icon is clicked
    if (openBtn) {
        openBtn.addEventListener('click', function() {
            sidebar.style.display = 'block';
            closeBtn.style.display = 'block';
        });
    }

    // Close sidebar when close button is clicked
    if (closeBtn) {
        closeBtn.addEventListener('click', function() {
            sidebar.style.display = 'none';
        });
    }
}
