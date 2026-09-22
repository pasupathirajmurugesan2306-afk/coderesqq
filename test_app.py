import unittest
import json
from app import create_app
from models import db, Admin, Competition, Question, JavaError, Participant, Submission, SuspiciousActivity
from services.code_evaluator import run_python_code, evaluate_java_code

class CoderesQTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.app.config['TESTING'] = True
        self.app.config['WTF_CSRF_ENABLED'] = False
        self.client = self.app.test_client()
        self.ctx = self.app.app_context()
        self.ctx.push()

    def tearDown(self):
        self.ctx.pop()

    def test_01_seed_verification(self):
        """Verifies database seeding of Admin, Settings, and Questions."""
        admin = Admin.query.filter_by(username='admin').first()
        self.assertIsNotNone(admin, "Default admin must exist")
        self.assertTrue(admin.check_password('CoderesQ@Admin2026'), "Admin password must match")

        comp = Competition.query.first()
        self.assertIsNotNone(comp, "Competition settings must exist")
        self.assertEqual(comp.r1_duration_minutes, 30)

        # 20 Python Questions
        py_qs = Question.query.filter_by(round=1).all()
        self.assertEqual(len(py_qs), 20, f"Expected 20 Python questions, found {len(py_qs)}")

        # 5 Java Questions
        java_qs = Question.query.filter_by(round=2).all()
        self.assertEqual(len(java_qs), 5, f"Expected 5 Java questions, found {len(java_qs)}")

        # 35 Java Errors (7 per question)
        for q in java_qs:
            self.assertEqual(len(q.java_errors), 7, f"Java question {q.id} must have exactly 7 errors")

    def test_02_python_evaluator(self):
        """Tests Python evaluation against intentional bug and fix."""
        q1 = Question.query.filter_by(round=1, order_num=1).first()
        self.assertIsNotNone(q1)

        # Buggy code should fail
        res_buggy = run_python_code(q1.buggy_code, q1.test_cases)
        self.assertFalse(res_buggy['success'], "Buggy code must not pass tests")

        # Correct code should pass
        res_correct = run_python_code(q1.correct_code, q1.test_cases)
        self.assertTrue(res_correct['success'], "Corrected code must pass all tests")

    def test_03_java_evaluator(self):
        """Tests Java evaluation of 7 errors."""
        q_java = Question.query.filter_by(round=2, order_num=1).first()
        self.assertIsNotNone(q_java)

        # Buggy code should have 0 fixed
        res_buggy = evaluate_java_code(q_java.buggy_code, q_java.java_errors)
        self.assertLessEqual(res_buggy['errors_fixed_count'], 1)

        # Correct code should have all 7 fixed
        res_correct = evaluate_java_code(q_java.correct_code, q_java.java_errors)
        self.assertEqual(res_correct['errors_fixed_count'], 7, "All 7 errors must be detected as fixed")
        self.assertTrue(res_correct['success'])

    def test_04_participant_flow(self):
        """Simulates candidate registration -> round 1 -> round 2 -> result."""
        # 1. Registration
        reg_data = {
            'name': 'Test Participant',
            'participant_id': 'TEST2026',
            'email': 'test@university.edu',
            'college': 'Test Institute of Tech',
            'department': 'Computer Science',
            'year': '3rd Year',
            'team_name': 'BugHunters'
        }
        resp = self.client.post('/register', data=reg_data, follow_redirects=True)
        self.assertEqual(resp.status_code, 200)
        self.assertIn(b'Competition Rules', resp.data)

        # 2. Enter Round 1
        resp_r1 = self.client.get('/round1')
        self.assertEqual(resp_r1.status_code, 200)
        self.assertIn(b'ROUND 1', resp_r1.data)

        # 3. Submit Python Code for Q1
        q1 = Question.query.filter_by(round=1, order_num=1).first()
        submit_data = {
            'question_id': q1.id,
            'code': q1.correct_code
        }
        resp_sub = self.client.post('/api/submit_code', 
                                    data=json.dumps(submit_data),
                                    content_type='application/json')
        self.assertEqual(resp_sub.status_code, 200)
        sub_json = json.loads(resp_sub.data)
        self.assertEqual(sub_json['status'], 'passed')
        self.assertEqual(sub_json['score'], 5.0)

        # 4. Anti-Cheat Activity Logging
        cheat_data = {'event': 'Tab Switch / Window Hidden', 'details': 'Test blur event'}
        resp_cheat = self.client.post('/api/anti_cheat/log',
                                      data=json.dumps(cheat_data),
                                      content_type='application/json')
        self.assertEqual(resp_cheat.status_code, 200)
        p = Participant.query.filter_by(participant_id='TEST2026').first()
        self.assertGreater(p.activities.count(), 0)

        # 5. Finish Round 1 -> Round 2
        resp_finish_r1 = self.client.post('/round1/finish', follow_redirects=True)
        self.assertEqual(resp_finish_r1.status_code, 200)
        self.assertIn(b'ROUND 2', resp_finish_r1.data)

        # 6. Submit Java Code for Q1
        q_java = Question.query.filter_by(round=2, order_num=1).first()
        submit_java_data = {
            'question_id': q_java.id,
            'code': q_java.correct_code
        }
        resp_java_sub = self.client.post('/api/submit_code',
                                         data=json.dumps(submit_java_data),
                                         content_type='application/json')
        self.assertEqual(resp_java_sub.status_code, 200)
        java_sub_json = json.loads(resp_java_sub.data)
        self.assertEqual(java_sub_json['errors_fixed_count'], 7)
        self.assertEqual(java_sub_json['status'], 'passed')

        # 7. Finish Challenge
        resp_finish_r2 = self.client.post('/round2/finish', follow_redirects=True)
        self.assertEqual(resp_finish_r2.status_code, 200)
        self.assertIn(b'CODERESQ RESULT', resp_finish_r2.data)

        # 8. Check Leaderboard
        resp_lead = self.client.get('/leaderboard')
        self.assertEqual(resp_lead.status_code, 200)
        self.assertIn(b'Test Participant', resp_lead.data)

    def test_05_admin_operations(self):
        """Tests admin login, dashboard, question management, settings."""
        # 1. Login
        login_resp = self.client.post('/admin/login', data={
            'username': 'admin',
            'password': 'CoderesQ@Admin2026'
        }, follow_redirects=True)
        self.assertEqual(login_resp.status_code, 200)
        self.assertIn(b'Command Center', login_resp.data)

        # 2. Add question
        add_q_data = {
            'round': '1',
            'title': 'Test Extra Question',
            'difficulty': 'Medium',
            'points': '5.0',
            'error_type': 'Syntax Error',
            'question_text': 'A test question description.',
            'buggy_code': 'def foo(): pass',
            'correct_code': 'def foo(): return True',
            'explanation': 'Explanation here',
            'test_cases': '[{"call": "foo()", "expected": true, "description": "Test"}]'
        }
        resp_add = self.client.post('/admin/questions/add', data=add_q_data, follow_redirects=True)
        self.assertEqual(resp_add.status_code, 200)
        new_q = Question.query.filter_by(title='Test Extra Question').first()
        self.assertIsNotNone(new_q)

        # 3. Export CSV
        resp_export = self.client.get('/admin/participants/export')
        self.assertEqual(resp_export.status_code, 200)
        self.assertEqual(resp_export.content_type, 'text/csv; charset=utf-8')

if __name__ == '__main__':
    unittest.main()
