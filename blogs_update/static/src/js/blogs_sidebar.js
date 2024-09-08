console.log("Heavy")
    const openBtn = document.getElementById('open-sidebar');
    const closeBtn = document.getElementById('close-sidebar');
    const sidebar = document.getElementById('blog-sidebar');

    // Open sidebar when hamburger icon is clicked
    openBtn.addEventListener('click', function() {
        sidebar.style.display = 'block';
        closeBtn.style.display = 'block';
    });

    // Close sidebar when close button is clicked
    closeBtn.addEventListener('click', function() {
        sidebar.style.display = 'none';
    });
