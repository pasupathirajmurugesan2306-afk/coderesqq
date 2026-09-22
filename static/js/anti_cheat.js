/**
 * CoderesQ Anti-Cheating & Integrity Guard
 */
(function() {
    let warningCount = 0;
    let isSubmitting = false;

    // Toast alert helper
    function showWarning(message) {
        let alertContainer = document.getElementById('anti-cheat-container');
        if (!alertContainer) {
            alertContainer = document.createElement('div');
            alertContainer.id = 'anti-cheat-container';
            alertContainer.className = 'anti-cheat-alert';
            document.body.appendChild(alertContainer);
        }

        const toast = document.createElement('div');
        toast.className = 'bg-rose-950/90 border border-rose-500/50 text-rose-200 px-4 py-3 rounded-lg shadow-2xl flex items-center gap-3 backdrop-blur-md mb-2';
        toast.innerHTML = `
            <svg class="w-5 h-5 text-rose-400 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"></path>
            </svg>
            <div>
                <p class="text-xs font-semibold uppercase tracking-wider text-rose-400">Security Warning</p>
                <p class="text-sm">${message}</p>
            </div>
        `;
        alertContainer.appendChild(toast);

        setTimeout(() => {
            toast.style.opacity = '0';
            toast.style.transition = 'opacity 0.5s ease';
            setTimeout(() => toast.remove(), 500);
        }, 5000);
    }

    // Server-side reporting
    function reportActivity(event, details = '') {
        fetch('/api/anti_cheat/log', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ event: event, details: details })
        }).catch(err => console.error('Reporting failed:', err));
    }

    // 1. Tab Switching Detection
    document.addEventListener('visibilitychange', function() {
        if (document.hidden && !isSubmitting) {
            warningCount++;
            showWarning('Leaving the challenge window has been detected and logged.');
            reportActivity('Tab Switch / Window Hidden', `Count: ${warningCount}`);
        }
    });

    // 2. Window Blur Detection
    window.addEventListener('blur', function() {
        if (!isSubmitting) {
            warningCount++;
            reportActivity('Window Blur (Focus Lost)', `Count: ${warningCount}`);
        }
    });

    // 3. Disable Context Menu (Right Click)
    document.addEventListener('contextmenu', function(e) {
        e.preventDefault();
        showWarning('Right-click context menu is disabled during the challenge.');
        reportActivity('Context Menu Blocked');
        return false;
    });

    // 4. Prevent accidental refresh / back navigation
    window.addEventListener('beforeunload', function(e) {
        if (!isSubmitting) {
            e.preventDefault();
            e.returnValue = 'Are you sure you want to leave? Your timer will continue running.';
            return e.returnValue;
        }
    });

    // Disable keyboard shortcuts for inspect element / print
    document.addEventListener('keydown', function(e) {
        // F12 or Ctrl+Shift+I or Ctrl+Shift+J or Ctrl+U
        if (e.key === 'F12' || 
            (e.ctrlKey && e.shiftKey && (e.key === 'I' || e.key === 'i' || e.key === 'J' || e.key === 'j')) ||
            (e.ctrlKey && (e.key === 'u' || e.key === 'U'))) {
            e.preventDefault();
            showWarning('Developer tools and source inspection are prohibited.');
            reportActivity('Inspect Shortcut Prevented', `Key: ${e.key}`);
            return false;
        }
    });

    // Expose markSubmitting to allow form submissions without triggering beforeunload
    window.markChallengeSubmitting = function() {
        isSubmitting = true;
    };
})();
