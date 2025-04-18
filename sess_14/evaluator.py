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

def test_evaluate_kentid():
    print(f"{tokenizer.INFO} Testing evaluate KentID. . .")
    prgm = "nallahab;"
    assert eval(prgm) == None
    print(f"{tokenizer.OK} Evaluate KentID Passed!")

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

def test_if_stmt():
    print(f"{tokenizer.INFO} Testing evaluate If Statements. . .")

    env = {"x":4,"y":5}
    assert eval("if(1){x=8}",env) == None
    assert env["x"] == 8, f"Expected x=8, got x={env['x']}"

    assert eval("if(0){x=5}else{y=9}",env) == None
    assert env["x"] == 8, f"Expected x=8, got x={env['x']}"
    assert env["y"] == 9, f"Expected y=9, got y={env['y']}"

    print(f"{tokenizer.OK} Evaluate If Statements Passed!")

def test_while_stmt():
    print(f"{tokenizer.INFO} Testing evaluate While Statements. . .")

    env = {"x":4,"y":5}
    assert eval("while(x<6){y=y+1;x=x+1}",env) == None
    assert env["x"] == 6
    assert env["y"] == 7

    print(f"{tokenizer.OK} Evaluate While Statements Passed!")

def test_evaluate_macro():
    print(f"{tokenizer.INFO} Testing evaluate macro. . .")
    assert evaluate("__PI__ = 3.14\nprint __PI__") == 4
    print(f"{tokenizer.OK} Evaluate macro Passed!")

# ============================================================================
# ============================================================================

def evaluate(ast, environ={}):
    global print_buffer
    try:
        if ast["tag"] == "if":
            condition_value = evaluate(ast["condition"], environ)
            if condition_value:
                evaluate(ast["then"], environ)
            else:
                if ast["else"]:
                    evaluate(ast["else"], environ)
            return None
        if ast["tag"] == "while":
            print(ast)
            while evaluate(ast["condition"], environ):
                evaluate(ast["do"], environ)
            return None
        if ast["tag"] == "assign":
            target = ast["target"]
            assert target["tag"] == "identifier"
            identifier = target["value"]
            assert type(identifier) is str

            # print(f"{tokenizer.INFO} Evaluating {identifier}'s value {ast['value']}")

            value = evaluate(ast["value"],environ)
            environ[identifier] = value
        if ast["tag"] == "&&":
            left_value = evaluate(ast["left"], environ)
            right_value = evaluate(ast["right"], environ)
            return left_value and right_value
        if ast["tag"] == "||":
            left_value = evaluate(ast["left"], environ)
            right_value = evaluate(ast["right"], environ)
            return left_value or right_value
        if ast["tag"] == "!":
            value = evaluate(ast["value"], environ)
            return not value
        if ast["tag"] == "<":
            left_value = evaluate(ast["left"], environ)
            right_value = evaluate(ast["right"], environ)
            return left_value < right_value
        if ast["tag"] == ">":
            left_value = evaluate(ast["left"], environ)
            right_value = evaluate(ast["right"], environ)
            return left_value > right_value
        if ast["tag"] == "<=":
            left_value = evaluate(ast["left"], environ)
            right_value = evaluate(ast["right"], environ)
            return left_value <= right_value
        if ast["tag"] == ">=":
            left_value = evaluate(ast["left"], environ)
            right_value = evaluate(ast["right"], environ)
            return left_value >= right_value
        if ast["tag"] == "==":
            left_value = evaluate(ast["left"], environ)
            right_value = evaluate(ast["right"], environ)
            return left_value == right_value
        if ast["tag"] == "!=":
            left_value = evaluate(ast["left"], environ)
            right_value = evaluate(ast["right"], environ)
            return left_value != right_value
        
        if ast["tag"] == "number":
            return ast["value"]
        if ast["tag"] == "macro":
            print(ast)
            return ast["value"]
        if ast["tag"] == "identifier":
            if ast["value"][0] == "-": # check for negated identifier
                identifier = ast["value"][1:] # removing the negation symbol
                if identifier in environ:
                    if type(environ[identifier]) in [int,float]: # negation can only occur on number-based types
                        return -(environ[identifier])
                    raise Exception(f"Environment Identifier {identifier} with value {type(environ[identifier])} cannot be Negated!")
                raise Exception(f"Unknown Environment Identifier {identifier}")
            if ast["value"] in environ:
                return environ[ast["value"]]
            
            # handle parent environ
            parent_env = environ
            while "$parent" in parent_env:
                parent_env = environ["$parent"]
                if ast["value"] in parent_env:
                    return parent_env[ast["value"]]
                raise Exception(f"Value {ast['value']} not found in parent environ {parent_env}.")
            
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
        if ast["tag"] == "block":
            for statement in ast["statements"]:
                _ = evaluate(statement, environ)
        if ast["tag"] == "print":
            # print(f"{tokenizer.INFO} PRINT DEBUG: {ast}")

            # evaluating what we are attempting to print
            ast_value = evaluate(ast["value"],environ)
            # cast ast_value as string as print_buffer is a string variable
            # and gets compared in tests as a string
            print(ast_value) # this print is for displaying output, dont remove!
            print_buffer = str(ast_value)
            return None
        if ast["tag"] == "kentID":
            # update the envion
            environ['_kentid_'] = ast["value"]
            assert environ['_kentid_'] == "nallahab@kent.edu", f"{tokenizer.ERR} Unexpected environ value: {environ['_kentid_']}"
            print(f"KENT-ID AST: {ast}")
    except Exception as e:
        import traceback
        print(f"{tokenizer.ERR} Evaluation Err: {e}")
        traceback.print_exc()

# Used in test-cases
def eval(s, environ={}):
    tokens = tokenizer.tokenize(s)
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
    test_evaluate_kentid()

    test_evaluate_identifier()

    test_if_stmt()
    test_while_stmt()

    # needs work
    # test_evaluate_macro()

    print(f"{tokenizer.OK} Evaluator is Functional!")