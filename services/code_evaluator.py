import os
import sys
import subprocess
import tempfile
import json
import re

def normalize_code_snippet(snippet):
    """Normalize code snippet for comparison: remove comments, normalize whitespace."""
    # Remove single line comments
    lines = snippet.split('\n')
    cleaned_lines = []
    for line in lines:
        cleaned = re.sub(r'//.*$', '', line) # Java comments
        cleaned = re.sub(r'#.*$', '', cleaned) # Python comments
        cleaned = cleaned.strip()
        if cleaned:
            cleaned_lines.append(cleaned)
    return ' '.join(cleaned_lines)

def run_python_code(user_code, test_cases, timeout=5):
    """
    Safely executes user Python code against test cases in an isolated subprocess.
    test_cases format: list of dicts: [{"call": "func(1, 2)", "expected": 3, "description": "Test 1"}]
    or [{"stdin": "5\n", "expected": "120", "description": "Factorial"}]
    """
    # Create test harness script
    test_runner_script = f"""
import sys
import json
import traceback

# --- PARTICIPANT CODE ---
{user_code}

# --- TEST RUNNER HARNESS ---
def _run_tests():
    raw_tests = {json.dumps(test_cases)}
    results = []
    all_passed = True
    
    for i, tc in enumerate(raw_tests):
        desc = tc.get('description', f'Test Case {{i + 1}}')
        is_hidden = tc.get('is_hidden', False)
        call_code = tc.get('call', '')
        expected = tc.get('expected', None)
        
        test_res = {{
            'index': i + 1,
            'description': desc,
            'is_hidden': is_hidden,
            'passed': False,
            'expected': expected if not is_hidden else 'HIDDEN',
            'actual': None,
            'error': None
        }}
        
        try:
            if call_code:
                # Evaluate expression
                actual = eval(call_code)
                test_res['actual'] = actual if not is_hidden else ('MATCH' if actual == expected else 'MISMATCH')
                if actual == expected:
                    test_res['passed'] = True
                else:
                    all_passed = False
            elif 'stdin' in tc:
                # Script output test case
                pass
            else:
                test_res['passed'] = True
        except Exception as e:
            all_passed = False
            tb_lines = traceback.format_exc().splitlines()
            test_res['error'] = tb_lines[-1] if tb_lines else str(e)
            test_res['actual'] = f"Exception: {{test_res['error']}}"
            
        results.append(test_res)
        
    print("__RESULTS_START__")
    print(json.dumps({{'all_passed': all_passed, 'results': results}}))
    print("__RESULTS_END__")

if __name__ == '__main__':
    try:
        _run_tests()
    except Exception as e:
        print("__RESULTS_START__")
        print(json.dumps({{'all_passed': False, 'results': [], 'fatal_error': traceback.format_exc()}}))
        print("__RESULTS_END__")
"""

    with tempfile.NamedTemporaryFile('w', suffix='.py', delete=False, encoding='utf-8') as f:
        f.write(test_runner_script)
        temp_path = f.name

    try:
        proc = subprocess.run(
            [sys.executable, temp_path],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            timeout=timeout,
            encoding='utf-8',
            errors='replace'
        )
        stdout = proc.stdout
        stderr = proc.stderr
        
        # Parse test results from stdout
        if "__RESULTS_START__" in stdout and "__RESULTS_END__" in stdout:
            parts = stdout.split("__RESULTS_START__")[1].split("__RESULTS_END__")[0].strip()
            parsed = json.loads(parts)
            user_stdout = stdout.split("__RESULTS_START__")[0].strip()
            return {
                'success': parsed.get('all_passed', False),
                'results': parsed.get('results', []),
                'stdout': user_stdout,
                'stderr': stderr,
                'fatal_error': parsed.get('fatal_error')
            }
        else:
            return {
                'success': False,
                'results': [],
                'stdout': stdout,
                'stderr': stderr or 'Runtime or Syntax Error occurred while executing code.',
                'fatal_error': stderr or stdout
            }
    except subprocess.TimeoutExpired:
        return {
            'success': False,
            'results': [],
            'stdout': '',
            'stderr': f'Execution timed out after {timeout} seconds. Check for infinite loops or recursion.',
            'fatal_error': 'TimeoutExpired'
        }
    except Exception as e:
        return {
            'success': False,
            'results': [],
            'stdout': '',
            'stderr': str(e),
            'fatal_error': str(e)
        }
    finally:
        if os.path.exists(temp_path):
            try:
                os.remove(temp_path)
            except Exception:
                pass


def evaluate_java_code(user_code, java_errors, test_cases=None, question=None):
    """
    Evaluates Java submission by checking resolution of the 7 intentional errors.
    Returns:
      errors_fixed_count (0 to 7)
      fixed_status_list: list of dicts for each of the 7 errors (resolved: bool)
      success: bool (True if all 7 errors fixed)
      stdout / stderr details
    """
    fixed_status_list = []
    fixed_count = 0
    
    # Normalize user code for flexible matching (spaces, tabs, newlines)
    norm_user = ' '.join(user_code.split())
    # Remove single line comments
    code_no_comments = re.sub(r'//.*', '', user_code)
    norm_no_comm = ' '.join(code_no_comments.split())

    for err in java_errors:
        err_num = err.error_number
        buggy_norm = ' '.join(err.buggy_snippet.split())
        fixed_norm = ' '.join(err.fixed_snippet.split())
        
        is_fixed = False
        
        # Rule 1: Check if custom detection regex/rule is provided
        if err.detection_rule:
            try:
                rule = json.loads(err.detection_rule) if isinstance(err.detection_rule, str) and err.detection_rule.startswith('{') else None
                if rule and 'regex' in rule:
                    if re.search(rule['regex'], code_no_comments, re.IGNORECASE | re.MULTILINE):
                        is_fixed = True
                elif rule and 'anti_regex' in rule:
                    if not re.search(rule['anti_regex'], code_no_comments, re.IGNORECASE | re.MULTILINE):
                        is_fixed = True
            except Exception:
                pass
                
        # Rule 2: Check if fixed snippet is present or buggy snippet is removed
        if not is_fixed:
            # Buggy pattern should not be present
            buggy_still_present = (buggy_norm in norm_user) or (buggy_norm in norm_no_comm)
            fixed_is_present = (fixed_norm in norm_user) or (fixed_norm in norm_no_comm)
            
            # If fixed snippet was found, or buggy snippet was changed to a valid alternative
            if fixed_is_present:
                is_fixed = True
            elif not buggy_still_present:
                # Check fuzzy or key token match
                tokens = [t for t in fixed_norm.split() if len(t) > 2 and t not in ['public', 'private', 'static', 'int', 'void', 'for', 'if', 'else', '{', '}', ';']]
                if tokens and all(t in norm_no_comm for t in tokens):
                    is_fixed = True

        if is_fixed:
            fixed_count += 1
            
        fixed_status_list.append({
            'error_number': err_num,
            'category': err.error_category,
            'resolved': is_fixed,
            'description': err.description if is_fixed else "Error not yet resolved"
        })

    all_fixed = (fixed_count == len(java_errors))

    # Optional: If javac is installed, attempt actual compilation
    compile_output = ""
    compile_success = False
    try:
        javac_check = subprocess.run(['javac', '-version'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, timeout=2)
        if javac_check.returncode == 0:
            # javac is available!
            with tempfile.TemporaryDirectory() as temp_dir:
                # find class name
                match = re.search(r'class\s+([A-Za-z0-9_]+)', user_code)
                class_name = match.group(1) if match else "Solution"
                java_file = os.path.join(temp_dir, f"{class_name}.java")
                with open(java_file, 'w', encoding='utf-8') as jf:
                    jf.write(user_code)
                comp = subprocess.run(['javac', java_file], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, timeout=5)
                compile_success = (comp.returncode == 0)
                compile_output = comp.stderr if comp.stderr else ("Compilation Successful!" if compile_success else "")
    except Exception:
        # javac not available or error, relies on error verification
        pass

    return {
        'success': all_fixed,
        'errors_fixed_count': fixed_count,
        'total_errors': len(java_errors),
        'fixed_status_list': fixed_status_list,
        'compile_success': compile_success,
        'compile_output': compile_output,
        'stdout': f"Analysis complete. {fixed_count}/{len(java_errors)} errors corrected." + (f"\n{compile_output}" if compile_output else "")
    }
