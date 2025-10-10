// Header functionality
document.addEventListener('DOMContentLoaded', function() {
    
    // Ensure navbar is visible on page load
    setTimeout(function() {
        const navbarContent = document.getElementById('navbarContent');
        if (navbarContent && window.innerWidth >= 992) {
            navbarContent.classList.remove('collapse');
            navbarContent.classList.add('show');
            navbarContent.style.display = 'flex';
        }
    }, 100);
    
    // Theme Toggle Functionality
    const themeToggle = document.getElementById('theme-toggle');
    const body = document.body;
    
    // Check for saved theme preference or default to light mode
    const currentTheme = localStorage.getItem('theme') || 'light';
    body.setAttribute('data-theme', currentTheme);
    
    // Update theme toggle icon based on current theme
    updateThemeIcon(currentTheme);
    
    themeToggle.addEventListener('click', function() {
        const currentTheme = body.getAttribute('data-theme');
        const newTheme = currentTheme === 'light' ? 'dark' : 'light';
        
        body.setAttribute('data-theme', newTheme);
        localStorage.setItem('theme', newTheme);
        updateThemeIcon(newTheme);
    });
    
    function updateThemeIcon(theme) {
        const svg = themeToggle.querySelector('svg path');
        if (theme === 'dark') {
            // Sun icon for light mode
            svg.setAttribute('d', 'M12 3v1m0 16v1m9-9h-1M4 12H3m15.364 6.364l-.707-.707M6.343 6.343l-.707-.707m12.728 0l-.707.707M6.343 17.657l-.707.707M16 12a4 4 0 11-8 0 4 4 0 018 0z');
        } else {
            // Moon icon for dark mode
            svg.setAttribute('d', 'M20.354 15.354A9 9 0 018.646 3.646 9.003 9.003 0 0012 21a9.003 9.003 0 008.354-5.646z');
        }
    }
    
    // Search functionality for both desktop and mobile
    const searchInputs = [document.getElementById('searchInput'), document.getElementById('mobileSearchInput')];
    
    searchInputs.forEach(searchInput => {
        if (searchInput) {
            // Add search suggestions or auto-complete functionality
            searchInput.addEventListener('keypress', function(e) {
                if (e.key === 'Enter') {
                    const searchValue = this.value.trim();
                    if (searchValue) {
                        // The form will automatically submit to the explore page
                        // You can add additional search logic here if needed
                    }
                }
            });
            
            // Add search suggestions (optional)
            searchInput.addEventListener('input', function() {
                const value = this.value.trim();
                if (value.length > 2) {
                    // You can implement search suggestions here
                    // For now, we'll just highlight the input
                    this.style.borderColor = 'rgba(109,40,217,0.5)';
                } else {
                    this.style.borderColor = 'rgba(109,40,217,0.2)';
                }
            });
        }
    });
    
    // Mobile menu improvements - Only for mobile screens
    const navbarToggler = document.querySelector('.navbar-toggler');
    const navbarContent = document.getElementById('navbarContent');
    
    if (navbarToggler && navbarContent) {
        // Only add mobile behavior on small screens
        function isMobileScreen() {
            return window.innerWidth < 992;
        }
        
        // Close mobile menu when clicking outside (only on mobile)
        document.addEventListener('click', function(e) {
            if (isMobileScreen() && !navbarToggler.contains(e.target) && !navbarContent.contains(e.target)) {
                const bsCollapse = new bootstrap.Collapse(navbarContent, {
                    toggle: false
                });
                bsCollapse.hide();
            }
        });
        
        // Close mobile menu when clicking on a link (only on mobile)
        const mobileLinks = navbarContent.querySelectorAll('a');
        mobileLinks.forEach(link => {
            link.addEventListener('click', function() {
                if (isMobileScreen()) {
                    const bsCollapse = new bootstrap.Collapse(navbarContent, {
                        toggle: false
                    });
                    bsCollapse.hide();
                }
            });
        });
        
        // Ensure navbar is visible on desktop
        if (!isMobileScreen()) {
            navbarContent.classList.remove('collapse');
            navbarContent.classList.add('show');
            navbarContent.style.display = 'flex';
        }
        
        // Handle window resize
        window.addEventListener('resize', function() {
            if (!isMobileScreen()) {
                // Desktop: ensure navbar is visible
                navbarContent.classList.remove('collapse');
                navbarContent.classList.add('show');
                navbarContent.style.display = 'flex';
            } else {
                // Mobile: restore collapse behavior
                if (!navbarContent.classList.contains('show')) {
                    navbarContent.classList.add('collapse');
                    navbarContent.classList.remove('show');
                    navbarContent.style.display = '';
                }
            }
        });
    }
    
    // Add smooth scrolling for anchor links
    const anchorLinks = document.querySelectorAll('a[href^="#"]');
    anchorLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            const targetId = this.getAttribute('href').substring(1);
            const targetElement = document.getElementById(targetId);
            if (targetElement) {
                targetElement.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });
    
    // Add navbar scroll effect
    const navbar = document.querySelector('.navbar');
    if (navbar) {
        window.addEventListener('scroll', function() {
            if (window.scrollY > 50) {
                navbar.style.background = 'rgba(255,255,255,0.98)';
                navbar.style.boxShadow = '0 2px 20px rgba(0,0,0,0.1)';
            } else {
                navbar.style.background = 'rgba(255,255,255,0.95)';
                navbar.style.boxShadow = 'none';
            }
        });
    }
});

// CSS for theme toggle and header improvements
const themeStyles = `
    /* Override conflicting navbar styles */
    .navbar {
        position: fixed !important;
        top: 0 !important;
        left: 0 !important;
        right: 0 !important;
        z-index: 1050 !important;
        background: rgba(255,255,255,0.95) !important;
        backdrop-filter: blur(10px) !important;
        border-bottom: 1px solid rgba(109, 40, 217, 0.1) !important;
        height: auto !important;
        padding: 0.75rem 1rem !important;
    }
    
    .navbar .container-fluid {
        max-width: none !important;
        margin: 0 !important;
        display: flex !important;
        justify-content: space-between !important;
        align-items: center !important;
        height: auto !important;
        gap: 0 !important;
    }
    
    .navbar-brand {
        font-weight: 700 !important;
        font-size: 1.5rem !important;
        background: linear-gradient(135deg, #6D28D9 0%, #1E40AF 100%) !important;
        -webkit-background-clip: text !important;
        -webkit-text-fill-color: transparent !important;
        white-space: nowrap !important;
        flex-shrink: 0 !important;
        margin-right: 2rem !important;
    }
    
    .navbar-nav {
        display: flex !important;
        align-items: center !important;
        gap: 1rem !important;
        margin: 0 !important;
        padding: 0 !important;
    }
    
    .navbar-nav .nav-link {
        color: #4B5563 !important;
        transition: color 0.3s ease !important;
        position: relative !important;
        padding: 0.5rem 1rem !important;
        text-decoration: none !important;
    }
    
    .navbar-nav .nav-link:hover {
        color: #6D28D9 !important;
    }
    
    .navbar-nav .nav-link::after {
        content: '';
        position: absolute;
        width: 0;
        height: 2px;
        bottom: -5px;
        left: 50%;
        background: linear-gradient(135deg, #6D28D9 0%, #1E40AF 100%);
        transition: all 0.3s ease;
        transform: translateX(-50%);
    }
    
    .navbar-nav .nav-link:hover::after {
        width: 100%;
    }
    
    .navbar-toggler {
        border: none !important;
        padding: 0.25rem 0.5rem !important;
        background: transparent !important;
    }
    
    .navbar-toggler:focus {
        box-shadow: none !important;
    }
    
    .navbar-collapse {
        flex-basis: 100% !important;
        flex-grow: 1 !important;
        align-items: center !important;
    }
    
    /* Ensure navbar collapse is always visible on desktop */
    @media (min-width: 992px) {
        .navbar-collapse {
            display: flex !important;
        }
        
        .navbar-collapse.show {
            display: flex !important;
        }
        
        .navbar-collapse.collapse {
            display: flex !important;
        }
    }
    
    /* Force visibility of navbar content */
    .navbar-collapse.show {
        display: flex !important;
    }
    
    /* Ensure navbar buttons are always visible */
    .navbar .btn {
        display: inline-block !important;
        visibility: visible !important;
        opacity: 1 !important;
        position: relative !important;
        z-index: 10 !important;
    }
    
    .navbar .navbar-nav {
        display: flex !important;
        align-items: center !important;
        margin: 0 !important;
        padding: 0 !important;
    }
    
    .navbar .nav-item {
        display: flex !important;
        align-items: center !important;
    }
    
    .dropdown-menu {
        background: white !important;
        border: 1px solid rgba(0,0,0,0.15) !important;
        border-radius: 0.375rem !important;
        box-shadow: 0 0.5rem 1rem rgba(0,0,0,0.175) !important;
        padding: 0.5rem 0 !important;
        margin: 0 !important;
        min-width: 10rem !important;
    }
    
    .dropdown-item {
        display: block !important;
        width: 100% !important;
        padding: 0.5rem 1rem !important;
        clear: both !important;
        font-weight: 400 !important;
        color: #212529 !important;
        text-align: inherit !important;
        text-decoration: none !important;
        white-space: nowrap !important;
        background-color: transparent !important;
        border: 0 !important;
        transition: all 0.15s ease-in-out !important;
    }
    
    .dropdown-item:hover {
        color: #1e2125 !important;
        background-color: #f8f9fa !important;
    }
    
    .dropdown-divider {
        height: 0 !important;
        margin: 0.5rem 0 !important;
        overflow: hidden !important;
        border-top: 1px solid rgba(0,0,0,0.15) !important;
    }
    
    /* Theme Toggle Button Styles */
    .theme-toggle {
        transition: all 0.3s ease;
        border: 1px solid rgba(109,40,217,0.2) !important;
        background: transparent !important;
    }
    
    .theme-toggle:hover {
        background: rgba(109,40,217,0.1) !important;
        border-color: rgba(109,40,217,0.4) !important;
        transform: scale(1.05);
    }
    
    /* Navigation Link Styles */
    .navbar-nav .nav-link {
        color: #4B5563 !important;
        transition: color 0.3s ease;
        position: relative;
    }
    
    .navbar-nav .nav-link:hover {
        color: #6D28D9 !important;
    }
    
    .navbar-nav .nav-link::after {
        content: '';
        position: absolute;
        width: 0;
        height: 2px;
        bottom: -5px;
        left: 50%;
        background: linear-gradient(135deg, #6D28D9 0%, #1E40AF 100%);
        transition: all 0.3s ease;
        transform: translateX(-50%);
    }
    
    .navbar-nav .nav-link:hover::after {
        width: 100%;
    }
    
    /* Dark Theme Styles */
    [data-theme="dark"] {
        --bg-color: #1a1a1a;
        --text-color: #ffffff;
        --border-color: #333333;
    }
    
    [data-theme="dark"] .navbar {
        background: rgba(26, 26, 26, 0.95) !important;
        border-bottom: 1px solid rgba(255, 255, 255, 0.1) !important;
    }
    
    [data-theme="dark"] .navbar-brand {
        color: #ffffff !important;
    }
    
    [data-theme="dark"] .navbar-nav .nav-link {
        color: #e5e7eb !important;
    }
    
    [data-theme="dark"] .navbar-nav .nav-link:hover {
        color: #a78bfa !important;
    }
    
    [data-theme="dark"] .form-control {
        background: rgba(255, 255, 255, 0.1) !important;
        border-color: rgba(255, 255, 255, 0.2) !important;
        color: #ffffff !important;
    }
    
    [data-theme="dark"] .form-control::placeholder {
        color: rgba(255, 255, 255, 0.6) !important;
    }
    
    [data-theme="dark"] .dropdown-menu {
        background: #2a2a2a !important;
        border-color: #333333 !important;
    }
    
    [data-theme="dark"] .dropdown-item {
        color: #ffffff !important;
    }
    
    [data-theme="dark"] .dropdown-item:hover {
        background: #333333 !important;
    }
    
    [data-theme="dark"] .theme-toggle {
        border-color: rgba(255, 255, 255, 0.2) !important;
        color: #ffffff !important;
    }
    
    [data-theme="dark"] .theme-toggle:hover {
        background: rgba(255, 255, 255, 0.1) !important;
        border-color: rgba(255, 255, 255, 0.4) !important;
    }
    
    /* Mobile Responsive Improvements */
    @media (max-width: 991.98px) {
        .navbar-collapse {
            background: rgba(255,255,255,0.98) !important;
            backdrop-filter: blur(10px) !important;
            border-radius: 0.5rem !important;
            margin-top: 1rem !important;
            padding: 1rem !important;
            box-shadow: 0 0.5rem 1rem rgba(0,0,0,0.15) !important;
        }
        
        .navbar-nav {
            flex-direction: column !important;
            width: 100% !important;
            gap: 0 !important;
        }
        
        .navbar-nav .nav-link {
            padding: 0.75rem 1rem !important;
            border-bottom: 1px solid rgba(109,40,217,0.1) !important;
            width: 100% !important;
            text-align: left !important;
        }
        
        .navbar-nav .nav-link:last-child {
            border-bottom: none !important;
        }
        
        .navbar-nav .nav-item {
            width: 100% !important;
        }
        
        .dropdown {
            width: 100% !important;
        }
        
        .dropdown .btn {
            width: 100% !important;
            text-align: left !important;
        }
        
        .dropdown-menu {
            position: static !important;
            float: none !important;
            width: 100% !important;
            margin-top: 0 !important;
            background-color: transparent !important;
            border: none !important;
            box-shadow: none !important;
        }
        
        .dropdown-item {
            padding: 0.5rem 0 !important;
            border-bottom: 1px solid rgba(109,40,217,0.1) !important;
        }
        
        .dropdown-item:last-child {
            border-bottom: none !important;
        }
    }
`;

// Inject theme styles
const styleSheet = document.createElement('style');
styleSheet.textContent = themeStyles;
document.head.appendChild(styleSheet);
