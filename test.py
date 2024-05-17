import subprocess

def run_test(filename, method, expected_output):
    result = subprocess.run(['python', 'iengine.py', filename, method], capture_output=True, text=True)
    output = result.stdout.strip()
    print(f"Output for test {filename} with method {method}: {output}")
    assert expected_output in output, f"Test {filename} failed: expected '{expected_output}', got '{output}'"


# List of test cases
test_cases_TT = [
    ('test1.txt', 'YES'),
    ('test2.txt', 'YES'),
    ('test3.txt', 'YES'),
    ('test4.txt', 'NO'),
    ('test5.txt', 'YES'),
    ('test6.txt', 'NO'),
    ('test7.txt', 'YES'),
    ('test8.txt', 'YES'),
    ('test9.txt', 'YES'),
    ('test10.txt', 'NO'),
    ('test11.txt', 'YES'),
    ('test12.txt', 'NO'),
    ('test13.txt', 'YES'),
    ('test14.txt', 'YES'),
    ('test15.txt', 'YES'),
    ('test16.txt', 'YES'),
]
test_cases_CHAIN = [
    ('test1.txt', 'YES'),
    ('test2.txt', 'YES'),
    ('test3.txt', 'YES'),
    ('test4.txt', 'NO'),
    ('test5.txt', 'YES'),
    ('test6.txt', 'NO'),
    ('test7.txt', 'YES'),
    ('test8.txt', 'YES'),
    ('test9.txt', 'YES'),
    ('test10.txt', 'NO'),
    ('test11.txt', 'YES'),
    ('test12.txt', 'NO'),
    ('test13.txt', 'YES'),
    ('test14.txt', 'YES'),
    ('test15.txt', 'YES'),
    ('test16.txt', 'YES'),
]

for filename, expected_output in test_cases_TT:
    print(f"Running test: {filename} with method: Truth Table")
    run_test(filename, "TT", expected_output)

for filename, expected_output in test_cases_CHAIN:
    print(f"Running test: {filename} with method: Backwards Chaining")
    run_test(filename, "BC", expected_output)

for filename, expected_output in test_cases_CHAIN:
    print(f"Running test: {filename} with method: Forward Chaining")
    run_test(filename, "FC", expected_output)

print("All tests passed!")
