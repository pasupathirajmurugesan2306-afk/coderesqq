/**
 * CoderesQ Round 2 (Java Debugging) IDE Controller
 */

let editor = null;
let currentQuestionIndex = 0;
const questions = window.QUESTIONS_DATA || [];

function initRound2IDE() {
    require.config({ paths: { 'vs': 'https://cdnjs.cloudflare.com/ajax/libs/monaco-editor/0.45.0/min/vs' }});

    require(['vs/editor/editor.main'], function() {
        editor = monaco.editor.create(document.getElementById('monaco-editor-container'), {
            value: questions[0]?.current_code || questions[0]?.buggy_code || '',
            language: 'java',
            theme: 'vs-dark',
            automaticLayout: true,
            fontSize: 14,
            fontFamily: "'JetBrains Mono', 'Fira Code', monospace",
            lineNumbers: 'on',
            minimap: { enabled: false },
            scrollBeyondLastLine: false,
            tabSize: 4,
            renderWhitespace: 'selection'
        });

        editor.onDidChangeModelContent(function() {
            if (questions[currentQuestionIndex]) {
                questions[currentQuestionIndex].current_code = editor.getValue();
            }
        });

        loadQuestion(0);
    });

    setupEventListeners();
}

function loadQuestion(index) {
    if (index < 0 || index >= questions.length) return;

    if (editor && questions[currentQuestionIndex]) {
        questions[currentQuestionIndex].current_code = editor.getValue();
    }

    currentQuestionIndex = index;
    const q = questions[index];

    document.getElementById('q-title').textContent = q.title;
    document.getElementById('q-indicator').textContent = `Question ${q.order_num} / ${questions.length}`;
    document.getElementById('q-difficulty').textContent = q.difficulty;
    document.getElementById('q-points').textContent = `${q.points} Marks (2 Marks / Error)`;
    document.getElementById('q-description').textContent = q.question_text;

    // Update 7 Errors Fixed Meter
    updateErrorMeter(q.errors_fixed_count || 0);

    updateNavigatorUI();

    if (editor) {
        editor.setValue(q.current_code || q.buggy_code);
    }

    document.getElementById('output-terminal').innerHTML = '<span class="text-slate-500">Run code or submit solution to evaluate resolved Java errors...</span>';
}

function updateErrorMeter(fixedCount, statusList = null) {
    const counterElem = document.getElementById('errors-fixed-counter');
    if (counterElem) {
        counterElem.textContent = `${fixedCount} / 7`;
    }

    const badgesContainer = document.getElementById('error-badges-container');
    if (!badgesContainer) return;

    let html = '';
    for (let i = 1; i <= 7; i++) {
        const isResolved = i <= fixedCount;
        const cls = isResolved ? 'error-badge resolved' : 'error-badge unresolved';
        const icon = isResolved ? '✓' : i;
        html += `<div class="${cls}" title="Error ${i}: ${isResolved ? 'Resolved' : 'Pending'}">${icon}</div>`;
    }
    badgesContainer.innerHTML = html;
}

function updateNavigatorUI() {
    questions.forEach((q, idx) => {
        const btn = document.getElementById(`nav-btn-${idx}`);
        if (!btn) return;

        btn.className = 'q-pill w-12 h-10 rounded-lg font-mono text-sm font-semibold flex items-center justify-center transition-all cursor-pointer ';
        
        if (idx === currentQuestionIndex) {
            btn.className += 'bg-indigo-600 text-white shadow-lg ring-2 ring-indigo-400 ring-offset-2 ring-offset-slate-900 ';
        } else if (q.errors_fixed_count === 7) {
            btn.className += 'bg-emerald-600 text-white shadow-sm ';
        } else if (q.errors_fixed_count > 0) {
            btn.className += 'bg-amber-600/80 text-white ';
        } else {
            btn.className += 'bg-slate-800 text-slate-400 hover:bg-slate-700 hover:text-white ';
        }
    });
}

function setupEventListeners() {
    document.getElementById('btn-prev').addEventListener('click', () => {
        if (currentQuestionIndex > 0) loadQuestion(currentQuestionIndex - 1);
    });

    document.getElementById('btn-next').addEventListener('click', () => {
        if (currentQuestionIndex < questions.length - 1) loadQuestion(currentQuestionIndex + 1);
    });

    document.getElementById('btn-reset').addEventListener('click', () => {
        if (confirm('Reset editor to original buggy Java code?')) {
            const q = questions[currentQuestionIndex];
            q.current_code = q.buggy_code;
            if (editor) editor.setValue(q.buggy_code);
        }
    });

    // Run Code Button (Check resolved count)
    document.getElementById('btn-run').addEventListener('click', () => {
        const q = questions[currentQuestionIndex];
        const code = editor ? editor.getValue() : q.current_code;
        const outElem = document.getElementById('output-terminal');
        outElem.innerHTML = '<span class="text-indigo-400 animate-pulse">Analyzing Java source for 7 error checkpoints...</span>';

        fetch('/api/run_code', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ question_id: q.id, code: code })
        })
        .then(res => res.json())
        .then(data => {
            const fixedCount = data.errors_fixed_count || 0;
            q.errors_fixed_count = fixedCount;
            updateErrorMeter(fixedCount, data.fixed_status_list);

            let statusHtml = `
                <div class="mb-3 p-3 rounded bg-slate-900/80 border border-slate-700">
                    <div class="flex items-center justify-between mb-2">
                        <span class="text-sm font-semibold text-slate-200">Java Analysis Report</span>
                        <span class="px-2 py-0.5 rounded text-xs font-bold ${fixedCount === 7 ? 'bg-emerald-950 text-emerald-400 border border-emerald-500/40' : 'bg-indigo-950 text-indigo-400 border border-indigo-500/40'}">
                            ${fixedCount} of 7 Errors Corrected
                        </span>
                    </div>
                    <div class="text-xs text-slate-300 font-mono whitespace-pre-wrap">${escapeHtml(data.stdout || '')}</div>
                </div>
            `;
            outElem.innerHTML = statusHtml;
            updateNavigatorUI();
        })
        .catch(err => {
            outElem.innerHTML = `<span class="text-rose-400">Analysis Request Failed: ${err.message}</span>`;
        });
    });

    // Submit Answer Button
    document.getElementById('btn-submit').addEventListener('click', () => {
        const q = questions[currentQuestionIndex];
        const code = editor ? editor.getValue() : q.current_code;
        const outElem = document.getElementById('output-terminal');
        outElem.innerHTML = '<span class="text-indigo-400 animate-pulse">Submitting Java solution & calculating score...</span>';

        fetch('/api/submit_code', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ question_id: q.id, code: code })
        })
        .then(res => res.json())
        .then(data => {
            const fixedCount = data.errors_fixed_count || 0;
            q.errors_fixed_count = fixedCount;
            q.score = data.score;
            updateErrorMeter(fixedCount);

            if (fixedCount === 7) {
                outElem.innerHTML = `
                    <div class="p-3 bg-emerald-950/60 border border-emerald-500/50 rounded-lg text-emerald-300">
                        <div class="flex items-center gap-2 font-bold text-sm mb-1">
                            <svg class="w-5 h-5 text-emerald-400" fill="currentColor" viewBox="0 0 20 20"><path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd"></path></svg>
                            OUTSTANDING! All 7 Java Errors Fixed (+${data.score} Marks)
                        </div>
                        <p class="text-xs text-emerald-400/80">Maximum score awarded for this question.</p>
                    </div>
                `;
            } else {
                outElem.innerHTML = `
                    <div class="p-3 bg-amber-950/60 border border-amber-500/50 rounded-lg text-amber-300">
                        <div class="flex items-center gap-2 font-bold text-sm mb-1">
                            <svg class="w-5 h-5 text-amber-400" fill="currentColor" viewBox="0 0 20 20"><path fill-rule="evenodd" d="M8.257 3.099c.765-1.36 2.722-1.36 3.486 0l5.58 9.92c.75 1.334-.213 2.98-1.742 2.98H4.42c-1.53 0-2.493-1.646-1.743-2.98l5.58-9.92zM11 13a1 1 0 11-2 0 1 1 0 012 0zm-1-8a1 1 0 00-1 1v3a1 1 0 002 0V6a1 1 0 00-1-1z" clip-rule="evenodd"></path></svg>
                            Partial Solution: ${fixedCount}/7 Errors Fixed (+${data.score} Marks)
                        </div>
                        <p class="text-xs text-amber-400/80">You have earned partial credit. Keep debugging to resolve the remaining errors!</p>
                    </div>
                `;
            }

            document.getElementById('r2-score-display').textContent = data.r2_score;
            updateNavigatorUI();
        })
        .catch(err => {
            outElem.innerHTML = `<span class="text-rose-400">Submission Error: ${err.message}</span>`;
        });
    });
}

function escapeHtml(str) {
    if (typeof str !== 'string') str = String(str);
    return str.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;").replace(/"/g, "&quot;").replace(/'/g, "&#039;");
}

document.addEventListener('DOMContentLoaded', initRound2IDE);
