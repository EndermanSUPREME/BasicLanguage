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

def test_evaluate_identifier():
    print(f"{tokenizer.INFO} Testing evaluate Identifier. . .")
    result = eval("x+3",{"x":3}) # x = 3 in the env
    assert result == 6

    result = eval("-x+3",{"x":3}) # x = 3 in the env
    assert result == 0

    # test printing identifiers
    assert eval("print x+3",{"x":3}) == None # x = 3 in the env
    assert print_buffer == "6"

    assert eval("print -x+3",{"x":3}) == None # x = 3 in the env
    assert print_buffer == "0"
    
    # non-number variables cannot be negated
    result = eval("-x+3",{"x":"homeAddress"}) # x = some-string in the env
    assert result != 0

    result = eval("x+y",{"$parent":{"x":4},"y":5})
    assert result == 9, f"Unexpected return value: {result}"

    result = eval("x+(-y)",{"$parent":{"x":4},"y":5})
    assert result == -1, f"Unexpected return value: {result}"

    print(f"{tokenizer.OK} Evaluate Identifier Passed!")

# ============================================================================
# ============================================================================

def evaluate(ast, environ={}):
    try:
        if ast["tag"] == "number":
            return ast["value"]
        if ast["tag"] == "identifier":
            if ast["value"][0] == "-": # check for negated identifier
                identifier = ast["value"][1:] # removing the negation symbol
                if identifier in environ:
                    if type(environ[identifier]) in [int,float]: # negation can only occur on number-based types
                        return -(environ[identifier])
                    raise Exception(f"Environment Identifier {identifier} cannot be Negated!")
                raise Exception(f"Unknown Environment Identifier {identifier}")
            if ast["value"] in environ:
                return environ[ast["value"]]
            
            # handle parent environment
            parent_env = environ
            while "$parent" in parent_env:
                parent_env = environ["$parent"]
                if ast["value"] in parent_env:
                    return parent_env[ast["value"]]
                raise Exception(f"Value {ast['value']} not found in parent environment {parent_env}.")
            
            raise Exception(f"Unknown Environment Identifier {identifier}")
        if ast["tag"] in ["plus","minus","times","division"]:
            # Recursively evaluate both sides of the tree to a literal value
            left_value = evaluate(ast["left"],environ)
            right_value = evaluate(ast["right"],environ)

            assert left_value != None, "left_value should have a value!"
            assert right_value != None, "right_value should have a value!"

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
            ast_value = evaluate(ast["value"],environ)
            # cast ast_value as string as print_buffer is a string variable
            # and gets compared in tests as a string
            print(ast_value) # this print if for displaying output, dont remove!
            print_buffer = str(ast_value)
            return None
    except Exception as e:
        print(f"{tokenizer.ERR} Evaluation Err: {e}")

def eval(s, environ={}):
    tokens = tokenizer.tokenize(s)
    # print(tokens) # here for debugging
    ast = parser.parse(tokens)
    result = evaluate(ast, environ)
    return result

if __name__ == "__main__":
    test_evaluate_number()
    test_evaluate_addition()
    test_evaluate_subtraction()
    test_evaluate_multiplication()
    test_evaluate_division()
    test_evaluate_expression()
    test_evaluate_print()
    test_evaluate_identifier()
    print(f"{tokenizer.OK} Evaluator is Functional!")