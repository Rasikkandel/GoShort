// Utility function to copy text to clipboard
function copyToClipboard(elementId) {
    const element = document.getElementById(elementId);
    if (!element) return;

    // Create a temporary input to copy from
    const tempInput = document.createElement('input');
    tempInput.type = 'text';
    tempInput.value = element.value;
    document.body.appendChild(tempInput);

    // Select and copy the text
    tempInput.select();
    document.execCommand('copy');

    // Remove the temporary input
    document.body.removeChild(tempInput);

    // Visual feedback
    const button = event.target.closest('button');
    const originalText = button.innerHTML;
    button.innerHTML = '<i class="fas fa-check me-1"></i>Copied!';
    button.classList.add('btn-success');
    button.classList.remove('btn-primary', 'btn-outline-secondary', 'btn-outline-primary');

    setTimeout(() => {
        button.innerHTML = originalText;
        button.classList.remove('btn-success');
        if (originalText.includes('Copy')) {
            button.classList.add('btn-primary');
        } else {
            button.classList.add('btn-outline-secondary');
        }
    }, 2000);
}

// Form validation
document.addEventListener('DOMContentLoaded', function() {
    const forms = document.querySelectorAll('.needs-validation');
    
    forms.forEach(form => {
        form.addEventListener('submit', function(event) {
            if (!form.checkValidity()) {
                event.preventDefault();
                event.stopPropagation();
            }
            form.classList.add('was-validated');
        });
    });

    // Add smooth scroll behavior
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth'
                });
            }
        });
    });

    // Auto-dismiss alerts after 5 seconds
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(alert => {
        setTimeout(() => {
            const bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        }, 5000);
    });
});

// Responsive table handling for mobile
function makeTablesResponsive() {
    const tables = document.querySelectorAll('.table');
    tables.forEach(table => {
        if (window.innerWidth < 768) {
            table.classList.add('table-responsive');
        }
    });
}

window.addEventListener('resize', makeTablesResponsive);
makeTablesResponsive();
