import subprocess

def run_test(filename, method, expected_output):
    result = subprocess.run(['python', 'iengine.py', filename, method], capture_output=True, text=True)
    output = result.stdout.strip()
    assert expected_output in output, f"Test {filename} failed: expected '{expected_output}', got '{output}'"

# List of test cases
test_cases = [
    ('test1.txt', 'YES'),
    ('test2.txt', 'YES'),
    ('test3.txt',  'YES'),
    ('test4.txt',  'NO'),
    ('test5.txt',  'YES'),
    ('test6.txt',  'NO'),
    ('test7.txt',  'YES'),
    ('test8.txt',  'YES'),
    ('test9.txt',  'YES'),
    ('test10.txt',  'YES'),
    ('test11.txt',  'YES'),
    ('test12.txt',  'NO'),
    ('test13.txt',  'YES'),
    ('test14.txt',  'YES'),
    ('test15.txt',  'YES'),
]

# Run all test cases for each method
for filename, expected_output in test_cases:
    for method in ["FC", "BC", "TT"]:
        print(f"Running test: {filename} with method: {method}")
        run_test(filename, method, expected_output)

print("All tests passed!")
