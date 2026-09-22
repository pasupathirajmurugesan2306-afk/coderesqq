# CoderesQ — Code Debugging Competition Platform
> **Code. Debug. Conquer.**  
> *“Find the bug. Fix the code. Prove your skills.”*

CoderesQ is a modern, responsive full-stack web application designed for conducting multi-round programming code debugging competitions. It features a dark developer/IDE-inspired theme, Monaco code editor integration, real-time code evaluation, anti-cheating tracking, live countdown timers, automatic grading, interactive leaderboard, and an administrator control center.

---

## Key Competition Structure

### Round 1 — Python Debugging
* **Language:** Python
* **Total Questions:** 20 Medium to Hard questions
* **Error Constraint:** Each question contains **strictly ONE intentional error**
* **Concepts Tested:**
  1. Dictionary Mutation During Iteration (`RuntimeError`)
  2. String Manipulation / Word Reversal
  3. Binary Search Boundary Increment (Infinite Loop)
  4. Mutable Default Arguments in Graph Accumulators
  5. Closure Scope (`nonlocal` keyword)
  6. Sieve of Eratosthenes Range Boundary
  7. Nested List Flattening Base Case
  8. 2D Matrix Shallow Copy Pitfall
  9. Leap Year Conditional Precedence
  10. Run-Length Encoding End Boundary Flush
  11. Merge Sort Slice Concatenation
  12. Memoized Fibonacci State Cache
  13. FIFO Queue Using Two LIFO Stacks
  14. Exception Handling `finally` Return Trap
  15. Palindrome Phrase Alphanumeric Cleaner
  16. Binary Search Tree Global Range Bounds
  17. OOP Subclass `super().__init__()` Initialization
  18. Sliding Window Non-Repeating Substring
  19. Max-Heap Sift Down Child Comparison
  20. Syntax Error in Lambda Sorter Key Tuple
* **Evaluation:** Evaluated safely in isolated subprocesses against public & hidden test cases.

### Round 2 — Java Debugging
* **Language:** Java
* **Total Questions:** 5 Hard system programs
* **Error Constraint:** Each question contains **strictly 7 intentional errors**
* **System Challenges:**
  1. `LRUCache.java` — Doubly Linked List & HashMap caching engine
  2. `TransactionProcessor.java` — Thread-safe financial concurrency & BigDecimal arithmetic
  3. `DijkstraRouter.java` — PriorityQueue graph shortest path routing
  4. `ExpressionEvaluator.java` — Arithmetic parser with operator precedence stacks
  5. `HospitalRegistry.java` — Patient triage Binary Search Tree priority manager
* **7 Error Distribution:**
  - Variable declaration / Type error
  - Method signature / Access modifier error
  - Loop boundary / Condition error
  - Array / Collection indexing error
  - Conditional logic / String equality error
  - Object-Oriented Programming (OOP / Constructor) error
  - Java API / Exception handling error
* **Visual Progress Meter:** Live counter dynamically indicates `Errors Fixed: 0 / 7` through `7 / 7` with visual badges.

---

## Technical Architecture

* **Backend:** Python Flask 3.x, SQLAlchemy ORM
* **Database:** SQLite with foreign keys and cascade deletions
* **Frontend:** HTML5, CSS3, Tailwind CSS, FontAwesome 6, JetBrains Mono font
* **Code Editor:** Microsoft Monaco Editor (VS Code core) via CDN
* **Security & Anti-Cheat:**
  - Tab switch & window blur detection
  - Right-click context menu prevention
  - Developer tools shortcut warnings
  - Server-side timer validation with latency grace periods
  - PBKDF2/SHA256 hashed administrator credentials

---

## Quick Start Guide

### 1. Requirements
Ensure Python 3.10+ is installed:
```bash
python --version
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Launch CoderesQ
```bash
python run.py
```
Open your web browser and navigate to:
* **Candidate Portal:** [http://127.0.0.1:5000/](http://127.0.0.1:5000/)
* **Leaderboard:** [http://127.0.0.1:5000/leaderboard](http://127.0.0.1:5000/leaderboard)
* **Admin Console:** [http://127.0.0.1:5000/admin/login](http://127.0.0.1:5000/admin/login)

### Default Administrator Credentials:
* **Username:** `admin`
* **Password:** `CoderesQ@Admin2026`

---

## Project Organization

```
coderesq/
├── app.py                      # Flask factory & context setup
├── run.py                      # Production launcher
├── config.py                   # Environment & timer configurations
├── models.py                   # SQLAlchemy schema (7 database models)
├── seed_data.py                # Database seed data (20 Py + 5 Java Qs)
├── requirements.txt            # Python dependencies
├── test_app.py                 # Automated unit and integration test suite
│
├── services/
│   ├── code_evaluator.py       # Isolated Python subprocess runner & Java 7-error checkpoint engine
│   ├── anti_cheat.py           # Suspicious activity logging & timer validation
│   └── stats_service.py        # Leaderboard ranking & admin dashboard analytics
│
├── routes/
│   ├── auth.py                 # Admin authentication guards
│   ├── participant.py          # Candidate registration, rules, scorecard, leaderboard
│   ├── competition.py          # Round 1 & Round 2 Monaco IDEs, test runner, submission APIs
│   ├── admin.py                # Question CRUD, participant manager, CSV export, settings
│   └── api.py                  # Anti-cheat beacon & timer sync APIs
│
├── templates/
│   ├── base.html               # Dark theme layout
│   ├── index.html              # Landing page
│   ├── register.html           # Candidate registration form
│   ├── rules.html              # Rules agreement & round guidelines
│   ├── round1.html             # Round 1 Python Monaco IDE
│   ├── round2.html             # Round 2 Java Monaco IDE (0/7 to 7/7 meter)
│   ├── result.html             # Candidate performance scorecard & printable view
│   ├── leaderboard.html        # Live filtered leaderboard
│   └── admin/                  # Admin dashboard, question manager, submissions, logs
│
└── static/
    ├── css/style.css           # Custom dark IDE styling & animations
    └── js/
        ├── anti_cheat.js       # Tab switch, blur, shortcut integrity monitor
        ├── ide_round1.js       # Python Monaco Editor controller & test runner
        ├── ide_round2.js       # Java Monaco Editor controller & 7-error checker
        └── timer.js            # Live countdown timer & auto-submission handler
```
