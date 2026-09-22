import os
from app import app

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    print("=" * 65)
    print("   CODERESQ - Code Debugging Competition Platform")
    print("   Code. Debug. Conquer.")
    print("=" * 65)
    print(f" * Candidate Web Portal: http://127.0.0.1:{port}/")
    print(f" * Live Leaderboard:     http://127.0.0.1:{port}/leaderboard")
    print(f" * Admin Console:        http://127.0.0.1:{port}/admin/login")
    print(f" * Admin Credentials:    admin / CoderesQ@Admin2026")
    print("=" * 65)
    app.run(host='0.0.0.0', port=port, debug=False)
