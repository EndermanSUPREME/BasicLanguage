import tokenizer
import parser

def test_evaluate_number():
    print(f"{tokenizer.INFO} Testing evaluate number. . .")
    assert evaluate({"tag":"number","value":4}) == 4
    print(f"{tokenizer.OK} Evaluate Number Passed!")

def test_evaluate_addition():
    print(f"{tokenizer.INFO} Testing evaluate addition. . .")
    ast = {
        "tag":"plus",
        "left":{"tag":"number","value":1},
        "right":{"tag":"number","value":3}
        }
    assert evaluate(ast) == 4
    print(f"{tokenizer.OK} Evaluate Addition Passed!")

def test_evaluate_subtraction():
    print(f"{tokenizer.INFO} Testing evaluate subtraction. . .")
    ast = {
        "tag":"minus",
        "left":{"tag":"number","value":3},
        "right":{"tag":"number","value":2}
        }
    assert evaluate(ast) == 1
    print(f"{tokenizer.OK} Evaluate Subtraction Passed!")

def test_evaluate_multiplication():
    print(f"{tokenizer.INFO} Testing evaluate multiplication. . .")
    ast = {
        "tag":"times",
        "left":{"tag":"number","value":3},
        "right":{"tag":"number","value":2}
        }
    assert evaluate(ast) == 6
    print(f"{tokenizer.OK} Evaluate Multiplication Passed!")

def test_evaluate_division():
    print(f"{tokenizer.INFO} Testing evaluate division. . .")
    ast = {
        "tag":"division",
        "left":{"tag":"number","value":4},
        "right":{"tag":"number","value":2}
        }
    assert evaluate(ast) == 2
    print(f"{tokenizer.OK} Evaluate Division Passed!")

def test_evaluate_expression():
    print(f"{tokenizer.INFO} Testing evaluate expression. . .")
    assert eval("1+2+3") == 6
    assert eval("1+2*3") == 7
    assert eval("(1+2)*3") == 9
    assert eval("(1.0+2.1)*3") == 9.3
    print(f"{tokenizer.OK} Evaluate Expression Passed!")

print_buffer = ""
def test_evaluate_print():
    print(f"{tokenizer.INFO} Testing evaluate print. . .")
    assert eval("print 3") == None
    assert print_buffer == "3"
    assert eval("print 3.14") == None
    assert print_buffer == "3.14"
    print(f"{tokenizer.OK} Evaluate Print Passed!")

# ============================================================================
# ============================================================================

def evaluate(ast):
    if ast["tag"] == "number":
        return ast["value"]
    if ast["tag"] in ["plus","minus","times","division"]:
        # Recursively evaluate both sides of the tree to a literal value
        left_value = evaluate(ast["left"])
        right_value = evaluate(ast["right"])

        # after evaluating the left and right sides of the tree we can
        # perform the operation against both sides and eval a final solution
        if ast["tag"] == "plus":
            return left_value + right_value
        if ast["tag"] == "minus":
            return left_value - right_value
        if ast["tag"] == "times":
            return left_value * right_value
        if ast["tag"] == "division":
            return left_value / right_value
    if ast["tag"] == "print":
        global print_buffer
        # evaluating what we are attempting to print
        ast_value = evaluate(ast["value"])
        print(ast_value)
        # cast ast_value as string as print_buffer is a string variable
        # and gets compared in tests as a string
        print_buffer = str(ast_value)
        return None

def eval(s):
    tokens = tokenizer.tokenize(s)
    ast = parser.parse(tokens)
    result = evaluate(ast)
    return result

if __name__ == "__main__":
    test_evaluate_number()
    test_evaluate_addition()
    test_evaluate_subtraction()
    test_evaluate_multiplication()
    test_evaluate_division()
    test_evaluate_expression()
    test_evaluate_print()
    print(f"{tokenizer.OK} All Tests Passed!")