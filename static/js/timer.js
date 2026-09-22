/**
 * CoderesQ Countdown Timer
 */
function initCompetitionTimer(initialSeconds, finishFormId, timerDisplayId = 'competition-timer') {
    let secondsLeft = initialSeconds;
    const timerElem = document.getElementById(timerDisplayId);
    const finishForm = document.getElementById(finishFormId);

    function updateDisplay() {
        if (!timerElem) return;
        const mins = Math.floor(secondsLeft / 60);
        const secs = secondsLeft % 60;
        timerElem.textContent = `${String(mins).padStart(2, '0')}:${String(secs).padStart(2, '0')}`;

        if (secondsLeft <= 60) {
            timerElem.classList.add('timer-urgent');
            timerElem.classList.remove('text-amber-400', 'text-emerald-400');
        } else if (secondsLeft <= 300) {
            timerElem.classList.add('text-amber-400');
            timerElem.classList.remove('timer-urgent', 'text-emerald-400');
        } else {
            timerElem.classList.add('text-emerald-400');
            timerElem.classList.remove('timer-urgent', 'text-amber-400');
        }
    }

    updateDisplay();

    const interval = setInterval(() => {
        secondsLeft--;
        if (secondsLeft <= 0) {
            clearInterval(interval);
            secondsLeft = 0;
            updateDisplay();
            if (window.markChallengeSubmitting) {
                window.markChallengeSubmitting();
            }
            alert('Time limit reached! Submitting your round automatically.');
            if (finishForm) {
                finishForm.submit();
            }
        } else {
            updateDisplay();
        }
    }, 1000);

    // Periodically re-sync with server every 60 seconds
    setInterval(() => {
        const roundNum = window.CURRENT_ROUND || 1;
        fetch(`/api/timer/sync?round=${roundNum}`)
            .then(res => res.json())
            .then(data => {
                if (data.remaining_seconds !== undefined) {
                    secondsLeft = data.remaining_seconds;
                }
            })
            .catch(err => console.error('Timer sync error:', err));
    }, 60000);
}
