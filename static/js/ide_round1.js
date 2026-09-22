/**
 * CoderesQ Round 1 (Python Debugging) IDE Controller
 */

let editor = null;
let currentQuestionIndex = 0;
const questions = window.QUESTIONS_DATA || [];

function initRound1IDE() {
    require.config({ paths: { 'vs': 'https://cdnjs.cloudflare.com/ajax/libs/monaco-editor/0.45.0/min/vs' }});

    require(['vs/editor/editor.main'], function() {
        editor = monaco.editor.create(document.getElementById('monaco-editor-container'), {
            value: questions[0]?.current_code || questions[0]?.buggy_code || '',
            language: 'python',
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

        // Track changes locally
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

    // Save current editor state
    if (editor && questions[currentQuestionIndex]) {
        questions[currentQuestionIndex].current_code = editor.getValue();
    }

    currentQuestionIndex = index;
    const q = questions[index];

    // Update UI Elements
    document.getElementById('q-title').textContent = q.title;
    document.getElementById('q-indicator').textContent = `Question ${q.order_num} / ${questions.length}`;
    document.getElementById('q-error-type').textContent = q.error_type || 'Python Bug';
    document.getElementById('q-difficulty').textContent = q.difficulty;
    document.getElementById('q-points').textContent = `${q.points} Marks`;
    document.getElementById('q-description').textContent = q.question_text;

    // Update Question Navigator Pills
    updateNavigatorUI();

    // Load code into Monaco editor
    if (editor) {
        editor.setValue(q.current_code || q.buggy_code);
    }

    // Render sample test cases
    renderSampleTestCases(q.test_cases || []);

    // Clear previous output
    document.getElementById('output-terminal').innerHTML = '<span class="text-slate-500">Run or submit code to view execution output...</span>';
}

function updateNavigatorUI() {
    questions.forEach((q, idx) => {
        const btn = document.getElementById(`nav-btn-${idx}`);
        if (!btn) return;

        btn.className = 'q-pill w-9 h-9 rounded-lg font-mono text-sm font-semibold flex items-center justify-center transition-all cursor-pointer ';
        
        if (idx === currentQuestionIndex) {
            btn.className += 'bg-indigo-600 text-white shadow-lg ring-2 ring-indigo-400 ring-offset-2 ring-offset-slate-900 ';
        } else if (q.is_solved) {
            btn.className += 'bg-emerald-600 text-white shadow-sm ';
        } else if (q.current_code && q.current_code !== q.buggy_code) {
            btn.className += 'bg-amber-600/80 text-white ';
        } else {
            btn.className += 'bg-slate-800 text-slate-400 hover:bg-slate-700 hover:text-white ';
        }
    });
}

function renderSampleTestCases(tests) {
    const container = document.getElementById('test-cases-container');
    if (!container) return;

    if (!tests || tests.length === 0) {
        container.innerHTML = '<p class="text-xs text-slate-500 italic">No visible sample test cases for this question.</p>';
        return;
    }

    let html = '';
    tests.forEach((tc, idx) => {
        html += `
            <div class="bg-slate-900/90 border border-slate-800 rounded p-2 mb-2">
                <div class="flex items-center justify-between text-xs text-slate-400 mb-1">
                    <span class="font-semibold">${tc.description || 'Sample ' + (idx + 1)}</span>
                </div>
                <div class="text-xs font-mono text-slate-300">
                    <span class="text-slate-500">Input:</span> ${escapeHtml(tc.call || tc.stdin || '')}
                </div>
                <div class="text-xs font-mono text-indigo-300">
                    <span class="text-slate-500">Expected:</span> ${escapeHtml(JSON.stringify(tc.expected))}
                </div>
            </div>
        `;
    });
    container.innerHTML = html;
}

function setupEventListeners() {
    // Next / Prev buttons
    document.getElementById('btn-prev').addEventListener('click', () => {
        if (currentQuestionIndex > 0) loadQuestion(currentQuestionIndex - 1);
    });

    document.getElementById('btn-next').addEventListener('click', () => {
        if (currentQuestionIndex < questions.length - 1) loadQuestion(currentQuestionIndex + 1);
    });

    // Reset Code Button
    document.getElementById('btn-reset').addEventListener('click', () => {
        if (confirm('Reset editor to original buggy code?')) {
            const q = questions[currentQuestionIndex];
            q.current_code = q.buggy_code;
            if (editor) editor.setValue(q.buggy_code);
        }
    });

    // Run Code Button
    document.getElementById('btn-run').addEventListener('click', () => {
        const q = questions[currentQuestionIndex];
        const code = editor ? editor.getValue() : q.current_code;
        const outElem = document.getElementById('output-terminal');
        outElem.innerHTML = '<span class="text-indigo-400 animate-pulse">Running test cases against Python evaluator...</span>';

        fetch('/api/run_code', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ question_id: q.id, code: code })
        })
        .then(res => res.json())
        .then(data => {
            let outputHtml = '';
            if (data.results && data.results.length > 0) {
                data.results.forEach(r => {
                    const badge = r.passed 
                        ? '<span class="px-1.5 py-0.5 rounded text-xs font-bold bg-emerald-950 text-emerald-400 border border-emerald-500/40">PASSED</span>'
                        : '<span class="px-1.5 py-0.5 rounded text-xs font-bold bg-rose-950 text-rose-400 border border-rose-500/40">FAILED</span>';
                    
                    outputHtml += `
                        <div class="mb-2 p-2 rounded bg-slate-900/60 border border-slate-800">
                            <div class="flex items-center justify-between mb-1">
                                <span class="font-semibold text-slate-300 text-xs">${r.description}</span>
                                ${badge}
                            </div>
                            <div class="text-xs text-slate-400 font-mono">Expected: ${escapeHtml(JSON.stringify(r.expected))}</div>
                            <div class="text-xs ${r.passed ? 'text-emerald-400' : 'text-rose-400'} font-mono">Actual: ${escapeHtml(JSON.stringify(r.actual))}</div>
                            ${r.error ? `<div class="text-xs text-rose-400 mt-1">Error: ${escapeHtml(r.error)}</div>` : ''}
                        </div>
                    `;
                });
            } else if (data.fatal_error || data.stderr) {
                outputHtml = `<div class="text-rose-400 font-mono text-xs whitespace-pre-wrap">${escapeHtml(data.fatal_error || data.stderr)}</div>`;
            } else {
                outputHtml = `<div class="text-slate-400 text-xs">${escapeHtml(data.stdout || 'Code executed with no output.')}</div>`;
            }
            outElem.innerHTML = outputHtml;
        })
        .catch(err => {
            outElem.innerHTML = `<span class="text-rose-400">Request Error: ${err.message}</span>`;
        });
    });

    // Submit Answer Button
    document.getElementById('btn-submit').addEventListener('click', () => {
        const q = questions[currentQuestionIndex];
        const code = editor ? editor.getValue() : q.current_code;
        const outElem = document.getElementById('output-terminal');
        outElem.innerHTML = '<span class="text-indigo-400 animate-pulse">Evaluating submission against full test suite...</span>';

        fetch('/api/submit_code', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ question_id: q.id, code: code })
        })
        .then(res => res.json())
        .then(data => {
            if (data.status === 'passed') {
                q.is_solved = true;
                q.score = data.score;
                outElem.innerHTML = `
                    <div class="p-3 bg-emerald-950/60 border border-emerald-500/50 rounded-lg text-emerald-300">
                        <div class="flex items-center gap-2 font-bold text-sm mb-1">
                            <svg class="w-5 h-5 text-emerald-400" fill="currentColor" viewBox="0 0 20 20"><path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd"></path></svg>
                            CORRECT! Bug Fixed Successfully (+${data.score} Marks)
                        </div>
                        <p class="text-xs text-emerald-400/80">All test cases passed cleanly. Answer saved!</p>
                    </div>
                `;
            } else {
                q.is_solved = false;
                outElem.innerHTML = `
                    <div class="p-3 bg-rose-950/60 border border-rose-500/50 rounded-lg text-rose-300">
                        <div class="flex items-center gap-2 font-bold text-sm mb-1">
                            <svg class="w-5 h-5 text-rose-400" fill="currentColor" viewBox="0 0 20 20"><path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clip-rule="evenodd"></path></svg>
                            Bug Still Present (0 / ${q.points} Marks)
                        </div>
                        <p class="text-xs text-rose-400/80">One or more test cases failed or caused runtime errors. Debug and try again.</p>
                    </div>
                `;
            }

            // Update score display in header
            document.getElementById('r1-score-display').textContent = data.r1_score;
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

document.addEventListener('DOMContentLoaded', initRound1IDE);
