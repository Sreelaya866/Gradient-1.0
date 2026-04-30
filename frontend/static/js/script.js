/* ========================================
   AUTOWEALTH - INTERACTIVE JAVASCRIPT
   ======================================== */

// ========================================
// MODAL FUNCTIONS
// ========================================

function openModal(modalName) {
    const modal = document.getElementById(modalName + 'Modal');
    if (modal) {
        modal.classList.add('active');
        document.body.style.overflow = 'hidden';
    }
}

function closeModal(modalName) {
    const modal = document.getElementById(modalName + 'Modal');
    if (modal) {
        modal.classList.remove('active');
        document.body.style.overflow = 'auto';
    }
}

// Close modal when clicking outside
document.addEventListener('click', function(event) {
    if (event.target.classList.contains('modal')) {
        const modal = event.target;
        modal.classList.remove('active');
        document.body.style.overflow = 'auto';
    }
});

// ========================================
// NOTIFICATION SYSTEM
// ========================================

function showNotification(message, type = 'info') {
    const notification = document.getElementById('notification');
    if (!notification) return;

    notification.textContent = message;
    notification.className = `notification active ${type}`;
    
    // Add icon based on type
    const icons = {
        'success': '✓',
        'error': '✗',
        'info': 'ℹ'
    };
    
    notification.innerHTML = `<span>${icons[type] || ''}</span> ${message}`;
    notification.className = `notification active ${type}`;

    setTimeout(() => {
        notification.classList.remove('active');
    }, 3000);
}

// ========================================
// PASSWORD MANAGEMENT
// ========================================

function togglePasswordVisibility(fieldId) {
    const field = document.getElementById(fieldId);
    if (field.type === 'password') {
        field.type = 'text';
    } else {
        field.type = 'password';
    }
}

// ========================================
// MOBILE MENU
// ========================================

const hamburger = document.getElementById('hamburger');
const navMenu = document.getElementById('navMenu');

if (hamburger) {
    hamburger.addEventListener('click', function() {
        navMenu.classList.toggle('active');
        hamburger.classList.toggle('active');
    });

    // Close menu when link is clicked
    document.querySelectorAll('.nav-link').forEach(link => {
        link.addEventListener('click', () => {
            navMenu.classList.remove('active');
            hamburger.classList.remove('active');
        });
    });
}

// ========================================
// SMOOTH SCROLLING
// ========================================

document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function(e) {
        const href = this.getAttribute('href');
        if (href !== '#') {
            e.preventDefault();
            const target = document.querySelector(href);
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        }
    });
});

// ========================================
// COUNTER ANIMATION
// ========================================

function animateCounter(element, target) {
    const duration = 2000;
    const start = 0;
    const increment = target / (duration / 16);
    let current = start;

    const counter = setInterval(() => {
        current += increment;
        if (current >= target) {
            element.textContent = target.toLocaleString();
            clearInterval(counter);
        } else {
            element.textContent = Math.floor(current).toLocaleString();
        }
    }, 16);
}

// Animate stat counters when page loads
document.addEventListener('DOMContentLoaded', function() {
    document.querySelectorAll('[data-target]').forEach(element => {
        const target = parseInt(element.getAttribute('data-target'));
        animateCounter(element, target);
    });
});

// ========================================
// GREETING MESSAGE
// ========================================

function updateGreeting() {
    const greetingElement = document.getElementById('greeting');
    if (!greetingElement) return;

    const hour = new Date().getHours();
    let greeting = '';

    if (hour < 12) {
        greeting = '☀️ Good morning! Here\'s your financial snapshot for today.';
    } else if (hour < 18) {
        greeting = '🌤️ Good afternoon! Keep tracking your progress.';
    } else {
        greeting = '🌙 Good evening! Review your daily spending and goals.';
    }

    greetingElement.textContent = greeting;
}

// ========================================
// LOCAL STORAGE USER MANAGEMENT
// ========================================

function initializeUser() {
    let user = localStorage.getItem('user');
    
    if (!user) {
        // For demo purposes, create a demo user
        const demoUser = {
            id: 1,
            name: 'Aisha Yadav',
            email: 'aisha.yadav1@gmail.com'
        };
        localStorage.setItem('user', JSON.stringify(demoUser));
        user = demoUser;
    } else {
        user = JSON.parse(user);
    }

    // Update user initials everywhere
    const initials = user.name.charAt(0).toUpperCase();
    document.querySelectorAll('#userInitial, #profileInitial').forEach(el => {
        el.textContent = initials;
    });

    // Update user name
    const userNameElements = document.querySelectorAll('#userName, #profileName');
    userNameElements.forEach(el => {
        el.textContent = user.name.split(' ')[0];
    });

    // Update email
    const userEmailElement = document.getElementById('profileEmail');
    if (userEmailElement) {
        userEmailElement.textContent = user.email;
    }

    return user;
}

// ========================================
// FORM VALIDATION
// ========================================

function validateForm(formId) {
    const form = document.getElementById(formId);
    if (!form) return false;

    let isValid = true;
    const inputs = form.querySelectorAll('input[required], select[required]');

    inputs.forEach(input => {
        if (!input.value.trim()) {
            input.style.borderColor = '#FF6B6B';
            isValid = false;
        } else {
            input.style.borderColor = '#ddd';
        }
    });

    return isValid;
}

// ========================================
// PAGE INITIALIZATION
// ========================================

document.addEventListener('DOMContentLoaded', function() {
    // Initialize user
    initializeUser();

    // Update greeting if on dashboard
    updateGreeting();

    // Add some interactive enhancements
    addFormEnhancements();

    // Setup event listeners
    setupEventListeners();
});

function addFormEnhancements() {
    // Add visual feedback to form inputs
    document.querySelectorAll('input, select, textarea').forEach(input => {
        input.addEventListener('focus', function() {
            this.style.boxShadow = '0 0 0 3px rgba(102, 126, 234, 0.1)';
        });

        input.addEventListener('blur', function() {
            this.style.boxShadow = 'none';
        });
    });
}

function setupEventListeners() {
    // Handle logout buttons
    document.querySelectorAll('.logout-btn').forEach(btn => {
        btn.addEventListener('click', function(e) {
            e.preventDefault();
            localStorage.removeItem('user');
            window.location.href = 'login.html';
        });
    });

    // Handle wishlist/bookmark icons
    document.querySelectorAll('.btn-wishlist').forEach(btn => {
        btn.addEventListener('click', function(e) {
            e.preventDefault();
            this.classList.toggle('active');
            const isActive = this.classList.contains('active');
            showNotification(
                isActive ? '❤️ Added to favorites' : '💔 Removed from favorites',
                'info'
            );
        });
    });
}

// ========================================
// SCROLL ANIMATIONS
// ========================================

const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.style.opacity = '1';
            entry.target.style.transform = 'translateY(0)';
        }
    });
}, { threshold: 0.1 });

document.querySelectorAll('.card, .feature-card, .goal-card, .hustle-card').forEach(el => {
    el.style.opacity = '0';
    el.style.transform = 'translateY(20px)';
    el.style.transition = 'all 0.6s ease';
    observer.observe(el);
});

// ========================================
// KEYBOARD SHORTCUTS
// ========================================

document.addEventListener('keydown', function(e) {
    // Press 'Esc' to close any open modal
    if (e.key === 'Escape') {
        document.querySelectorAll('.modal.active').forEach(modal => {
            modal.classList.remove('active');
        });
        document.body.style.overflow = 'auto';
    }

    // Press 'D' to go to dashboard
    if (e.ctrlKey && e.key === 'd') {
        e.preventDefault();
        window.location.href = 'dashboard.html';
    }

    // Press 'G' to go to goals
    if (e.ctrlKey && e.key === 'g') {
        e.preventDefault();
        window.location.href = 'goals.html';
    }

    // Press 'H' for help (you can customize this)
    if (e.ctrlKey && e.key === 'h') {
        e.preventDefault();
        alert('Keyboard Shortcuts:\n\nCtrl+D - Dashboard\nCtrl+G - Goals\nEsc - Close modal');
    }
});

// ========================================
// DYNAMIC CONTENT LOADER
// ========================================

function loadDashboardData() {
    // Simulate loading data from backend
    // In production, this would fetch from API
    
    const mockData = {
        expenses: [
            { name: 'Cafe', amount: 345, date: 'Today' },
            { name: 'Auto Ride', amount: 145, date: 'Today' },
            { name: 'Grocery', amount: 2250, date: 'Yesterday' },
            { name: 'Movie', amount: 650, date: '2 days ago' }
        ],
        goals: [
            { name: 'Emergency Fund', saved: 5200, target: 20000 },
            { name: 'Laptop', saved: 13825, target: 50000 },
            { name: 'Vacation', saved: 28500, target: 75000 }
        ]
    };

    return mockData;
}

// ========================================
// THEME TOGGLE
// ========================================

function toggleTheme() {
    const html = document.documentElement;
    const isDark = html.getAttribute('data-theme') === 'dark';
    
    if (isDark) {
        html.removeAttribute('data-theme');
        localStorage.setItem('theme', 'light');
    } else {
        html.setAttribute('data-theme', 'dark');
        localStorage.setItem('theme', 'dark');
    }
}

// Apply saved theme on load
document.addEventListener('DOMContentLoaded', function() {
    const savedTheme = localStorage.getItem('theme');
    if (savedTheme === 'dark') {
        document.documentElement.setAttribute('data-theme', 'dark');
    }
});

// ========================================
// ANALYTICS & TRACKING
// ========================================

function trackEvent(eventName, eventData) {
    // In production, send to analytics service
    console.log('Event:', eventName, eventData);
    
    // Store locally for demo
    let events = JSON.parse(localStorage.getItem('events') || '[]');
    events.push({
        name: eventName,
        data: eventData,
        timestamp: new Date().toISOString()
    });
    localStorage.setItem('events', JSON.stringify(events.slice(-50))); // Keep last 50 events
}

// Track page views
document.addEventListener('DOMContentLoaded', function() {
    const pageName = document.title.split(' - ')[0];
    trackEvent('page_view', { page: pageName });
});

// Track button clicks
document.querySelectorAll('.btn, a').forEach(element => {
    element.addEventListener('click', function() {
        trackEvent('click', {
            element: this.textContent,
            href: this.href
        });
    });
});

// ========================================
// EXPORT TO CSV FUNCTION
// ========================================

function exportToCSV(filename = 'expenses.csv') {
    trackEvent('export_csv', { filename });
    showNotification('✓ Downloaded to CSV successfully!', 'success');
}

// ========================================
// SEARCH FUNCTIONALITY
// ========================================

function setupSearch(inputSelector, itemSelector, textSelector) {
    const input = document.querySelector(inputSelector);
    if (!input) return;

    input.addEventListener('input', function(e) {
        const query = e.target.value.toLowerCase();
        const items = document.querySelectorAll(itemSelector);

        items.forEach(item => {
            const text = item.querySelector(textSelector).textContent.toLowerCase();
            item.style.display = text.includes(query) ? '' : 'none';
        });

        trackEvent('search', { query });
    });
}

// ========================================
// DATE FORMATTING UTILITY
// ========================================

function formatDate(date) {
    return new Date(date).toLocaleDateString('en-IN', {
        year: 'numeric',
        month: 'short',
        day: 'numeric'
    });
}

// ========================================
// CURRENCY FORMATTER
// ========================================

function formatCurrency(amount, currency = '₹') {
    return currency + ' ' + parseFloat(amount).toLocaleString('en-IN', {
        minimumFractionDigits: 0,
        maximumFractionDigits: 2
    });
}

// ========================================
// LOCAL LANGUAGE SUPPORT
// ========================================

const translations = {
    'hi': {
        'Total Spent': 'कुल खर्च',
        'Round-Up Saved': 'राउंड-अप बचाया गया',
        'Goals': 'लक्ष्य',
        'Dashboard': 'डैशबोर्ड'
    },
    'es': {
        'Total Spent': 'Gasto Total',
        'Round-Up Saved': 'Ahorro de Redondeo',
        'Goals': 'Objetivos',
        'Dashboard': 'Panel de Control'
    }
};

function setLanguage(lang = 'en') {
    localStorage.setItem('language', lang);
    
    if (lang === 'en') {
        // Reset to English
        document.querySelectorAll('[data-i18n]').forEach(el => {
            el.textContent = el.getAttribute('data-i18n-en');
        });
    } else if (translations[lang]) {
        document.querySelectorAll('[data-i18n]').forEach(el => {
            const key = el.getAttribute('data-i18n');
            if (translations[lang][key]) {
                el.textContent = translations[lang][key];
            }
        });
    }

    trackEvent('language_change', { language: lang });
}

// ========================================
// PERFORMANCE MONITORING
// ========================================

window.addEventListener('load', function() {
    const perfData = window.performance.timing;
    const pageLoadTime = perfData.loadEventEnd - perfData.navigationStart;
    
    console.log('Page Load Time:', pageLoadTime + 'ms');
    trackEvent('page_load', { loadTime: pageLoadTime });
});

// ========================================
// ERROR HANDLING
// ========================================

window.addEventListener('error', function(event) {
    console.error('Error:', event.error);
    trackEvent('error', { message: event.error.message });
});

// Unhandled promise rejection
window.addEventListener('unhandledrejection', function(event) {
    console.error('Unhandled promise rejection:', event.reason);
    trackEvent('unhandled_rejection', { reason: event.reason });
});

// ========================================
// SERVICE WORKER REGISTRATION (Optional)
// ========================================

if ('serviceWorker' in navigator) {
    // Uncomment to enable PWA features
    // navigator.serviceWorker.register('sw.js').then(reg => {
    //     console.log('Service Worker registered');
    // });
}

// ========================================
// ADVANCED FEATURES
// ========================================

// Auto-save form data
function enableAutoSave(formId, storageKey) {
    const form = document.getElementById(formId);
    if (!form) return;

    // Load saved data
    const savedData = localStorage.getItem(storageKey);
    if (savedData) {
        const data = JSON.parse(savedData);
        Object.keys(data).forEach(key => {
            const field = form.querySelector(`[name="${key}"]`);
            if (field) field.value = data[key];
        });
    }

    // Save on change
    form.addEventListener('change', function() {
        const formData = new FormData(form);
        const data = Object.fromEntries(formData);
        localStorage.setItem(storageKey, JSON.stringify(data));
    });
}

// ========================================
// DEMO DATA HELPERS
// ========================================

function generateMockExpense() {
    const categories = ['Food', 'Travel', 'Shopping', 'Bills', 'Entertainment'];
    const merchants = ['Cafe', 'Uber', 'Amazon', 'Netflix', 'Restaurant'];
    
    return {
        category: categories[Math.floor(Math.random() * categories.length)],
        merchant: merchants[Math.floor(Math.random() * merchants.length)],
        amount: Math.floor(Math.random() * 5000) + 100,
        date: new Date().toISOString().split('T')[0]
    };
}

// ========================================
// RESPONSIVE BEHAVIOR
// ========================================

// Handle responsive images
const images = document.querySelectorAll('img');
images.forEach(img => {
    img.addEventListener('load', function() {
        this.style.animation = 'fadeIn 0.4s ease';
    });
});

// Handle viewport changes
let resizeTimer;
window.addEventListener('resize', function() {
    clearTimeout(resizeTimer);
    resizeTimer = setTimeout(function() {
        trackEvent('viewport_resize', {
            width: window.innerWidth,
            height: window.innerHeight
        });
    }, 250);
});

// ========================================
// ACCESSIBILITY ENHANCEMENTS
// ========================================

// Add keyboard support for buttons
document.addEventListener('keydown', function(e) {
    if (e.key === 'Enter' && document.activeElement.classList.contains('btn')) {
        document.activeElement.click();
    }
});

// Add ARIA labels dynamically
document.querySelectorAll('.btn').forEach(btn => {
    if (!btn.getAttribute('aria-label')) {
        btn.setAttribute('aria-label', btn.textContent);
    }
});

// ========================================
// INITIALIZATION
// ========================================

// Final initialization on DOM ready
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initializeApp);
} else {
    initializeApp();
}

function initializeApp() {
    console.log('AutoWealth App Initialized');
    
    // Setup user
    initializeUser();
    
    // Update greeting
    updateGreeting();
    
    // Add form enhancements
    addFormEnhancements();
    
    // Setup event listeners
    setupEventListeners();
    
    // Track app load
    trackEvent('app_initialized', { timestamp: new Date().toISOString() });
}
