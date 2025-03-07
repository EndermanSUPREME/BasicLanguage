def eval(s: str):
    # check if the string s is not empty
    assert len(s) > 0, "Passed Number String has no Length!"
    # check if the string s is valid (is a proper number)
    assert s != "-" and s != ".", "Invalid Number String Passed!"

    # if there are too many occurances of . or - it is an invalid number
    assert s.count(".") <= 1, "Invalid Number String! (Too Many .)"
    assert s.count("-") <= 1, "Invalid Number String! (Too Many -)"

    if s.count("-") == 1:
        assert s[0] == '-', "Invalid Number String (Misplaced Negation-Sign)"

    # check if the characters in s are within the
    # const literal below
    for c in s:
        assert c in ".-0123456789"

    # General Reused Locals
    multi = 1.0
    fractional = False
    sign = 1
    i = 0
    n = 0

    # Iterate the characters of the string and perform condition logic
    for c in s:
        if s[0] == '-' and i == 0: # Manage the potential signed numbers
            sign = -1
        elif c == '.': # Handle decimal with no leading zero
            fractional = True
        else:
            # Build integer n, based on number type (fractional)
            if not fractional:
                    n = n * 10 + ord(c) - ord("0")
            else:
                multi = multi / 10
                n = n + (ord(c) - ord("0")) * multi
        # track index of string we are at
        i = i + 1

    # basic debug line
    # print(f's:{s} | sign:{sign} | n:{n}')

    return n * sign

# DRY Template for checking bad cases
def check_bad_cases(c: str):
    RED = "\033[31m"
    YLW = "\033[33m"
    BLU = "\033[34m"
    REG = "\033[0m"

    try:
        assert eval(c) == 0
        print(f'Case "{c}"' + REG + ': ' + RED + 'executed successfully!' + REG)
    except Exception as e:
        print(YLW + f'Error Caught from "{c}"' + REG + ': ' + BLU + f'{e}' + REG)

# DRY Template for checking normal cases
def check_cases(c: str, n: int, msg: str):
    # ANSI Color Escape Code Strings
    RED = "\033[31m"
    GRN = "\033[32m"
    BLU = "\033[34m"
    REG = "\033[0m"

    assert eval(c) == n, RED + msg + REG
    print(GRN + 'Passed' + REG + ': ' + BLU + f'{c}' + REG)

def test_eval():
    # mult-line comment
    """ test eval """
    print(f"[*] Running: test_eval. . .")
    
    check_cases("0", 0, "Expected \"0\" to be 0")
    check_cases("1", 1, "Expected \"1\" to be 1")
    check_cases("99", 99, "Expected \"99\" to be 99")

    check_cases("1099", 1099, "Expected \"1099\" to be 1099")
    check_cases("0001", 1, "Expected \"0001\" to be 1")
    check_cases("-90", -90, "Expected \"-90\" to be -90")

    check_cases("1.", 1, "Expected \"1.\" to be 1")
    check_cases("1.23", 1.23, "Expected \"1.23\" to be 1.23")
    check_cases("-1.23", -1.23, "Expected \"-1.23\" to be -1.23")

    # My own Funky
    check_cases("-.", 0, "Expected \"-.\" to be 0")


    # Test for cases we do not like
    check_bad_cases("--1")
    check_bad_cases("-1.2.3")
    check_bad_cases("3..14")

def main():
    test_eval()
    print(f'Done Executing {__file__.split("/")[-1]}')

if __name__ == "__main__":
    main()