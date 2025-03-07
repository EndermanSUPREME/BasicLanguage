import tokenizer

def test_parse_factor():
    print(f"{tokenizer.INFO} Testing Parse Factor. . .")
    for s in ["1","22","333","(4)","(55)","(666)"]:
        tokens = tokenizer.tokenize(s)
        ast, tokens = parse_term(tokens)

        # array slicing to remove the first and last element
        # s_n = s[1:-1]

        # crude filtering
        s_n = s.replace("(","").replace(")","")

        assert ast == {"tag": "number", "value": int(s_n)}, f"{tokenizer.ERR} Parse Factor Rule Test Failed!"
        assert tokens[0]["tag"] == None, f"{tokenizer.ERR} None-Tag should be present!"

    tokens = tokenizer.tokenize("1")
    ast, tokens = parse_factor(tokens)
    assert ast == {"tag":"number", "value":1}, f"{tokenizer.ERR} Parse Factor Rule Test Failed!"
    
    tokens = tokenizer.tokenize("x")
    ast, tokens = parse_factor(tokens)
    assert ast == {'tag': 'identifier', 'value': 'x'}, f"{tokenizer.ERR} Parse Factor Rule Test Failed!"
    
    tokens = tokenizer.tokenize("(x+3)")
    ast, tokens = parse_factor(tokens)
    assert ast == {'tag': 'plus', 'left': {'tag': 'identifier', 'value': 'x'}, 'right': {'tag': 'number', 'value': 3}}, f"{tokenizer.ERR} Parse Factor Rule Test Failed!"

    print(f"{tokenizer.OK} Parse Factor Rule Test Passed!")
# RULE: factor = number | indentifier | "(" expression ")"
def parse_factor(tokens):
    token = tokens[0]
    if token["tag"] == "number":
        return {
            "tag": "number",
            "value": token["value"]
        }, tokens[1:] # return what else is left
    elif token["tag"] == "l_paran":
        tokens = tokens[1:] # remove the '('
        ast, tokens = parse_expr(tokens)

        # see if potentially we now have a closing-paran at index 0 after performing parse_expr rule
        if tokens[0]["tag"] == "r_paran":
            tokens = tokens[1:] # remove the ')'
            return ast, tokens
        return ast, tokens
    elif token["tag"] == "identifier":
        return {
            "tag": "identifier",
            "value": token["value"]
        }, tokens[1:] # return what else is left
    
    raise Exception(f"{ tokenizer.ERR } Unexpected token: { token['tag'] } at position: { token['position'] }")

def test_parse_logical_factor():
    """
    logical_factor = relational_expression ;
    """
    print("testing parse_logical_factor()")
    for s in ["1", "2+2", "3<4"]:
        tokens = tokenizer.tokenize(s)
        ast1, tokens1 = parse_logical_factor(tokens)
        ast2, tokens2 = parse_relational_expr(tokens)
        assert ast1 == ast2
def parse_logical_factor(tokens):
    """
    logical_factor = relational_expression ;
    """
    return parse_relational_expr(tokens)


def test_parse_term():
    print(f"{tokenizer.INFO} Testing Parse Term. . .")
    tokens = tokenizer.tokenize("2*4")
    ast, tokens = parse_term(tokens)
    assert ast == {'tag': 'times', 'left': {'tag': 'number', 'value': 2}, 'right': {'tag': 'number', 'value': 4}}, f"{tokenizer.ERR} Invalid AST Generated!"

    tokens = tokenizer.tokenize("2*4/6")
    ast, tokens = parse_term(tokens)
    assert ast == {
        'tag': 'division',
        'left': {'tag': 'times', 'left': {'tag': 'number', 'value': 2},'right': {'tag': 'number', 'value': 4}},
        'right': {'tag': 'number', 'value': 6}
    }, f"{tokenizer.ERR} Invalid AST Generated!"

    print(f"{tokenizer.OK} Parse Term Rule Test Passed!")
# RULE: term = factor { "*" | "/" factor }
def parse_term(tokens):
    # nodes are part of the syntax tree
    node, tokens = parse_factor(tokens)
    # term = factor { "times" | "division" factor }
    while tokens[0]["tag"] in ["times","division"]:
        tag = tokens[0]["tag"]
        # slice out the contant terminal (operation token) when encountered
        right_node, tokens = parse_factor(tokens[1:])
        node = {"tag":tag, "left": node, "right": right_node}
    return node, tokens


def test_parse_expr():
    print(f"{tokenizer.INFO} Testing Parse Expression. . .")
    tokens = tokenizer.tokenize("1+2*3")
    ast,tokens = parse_expr(tokens)

    assert ast == {
        'tag': 'plus',
        'left': {'tag': 'number', 'value': 1},
        'right': {
                'tag': 'times',
                'left': {'tag': 'number', 'value': 2},
                'right': {'tag': 'number', 'value': 3}
            }
        }, f"{tokenizer.ERR} Invalid AST Generated!"

    # Test for various paranthesis grouping
    tokens = tokenizer.tokenize("2*(1+3)")
    ast,tokens = parse_expr(tokens)
    assert ast == {
        'tag': 'times',
        'left': {'tag': 'number', 'value': 2},
        'right': {'tag': 'plus', 'left': {'tag': 'number', 'value': 1}, 'right': {'tag': 'number', 'value': 3}}
        }, f"{tokenizer.ERR} Invalid AST Generated!"

    tokens = tokenizer.tokenize("(2*1)+3)")
    ast,tokens = parse_expr(tokens)
    assert ast == {
        'tag': 'plus',
        'left': {'tag': 'times', 'left': {'tag': 'number', 'value': 2}, 'right': {'tag': 'number', 'value': 1}},
        'right': {'tag': 'number', 'value': 3}
        }, f"{tokenizer.ERR} Invalid AST Generated!"
    
    tokens = tokenizer.tokenize("(2*(4+5))+3)")
    ast,tokens = parse_expr(tokens)
    assert ast == {
        'tag': 'plus',
        'left': {
            'tag': 'times',
            'left': {'tag': 'number', 'value': 2},
            'right': {'tag': 'plus', 'left': {'tag': 'number', 'value': 4}, 'right': {'tag': 'number', 'value': 5}}
        },
        'right': {'tag': 'number', 'value': 3}
        }, f"{tokenizer.ERR} Invalid AST Generated!"
    
    print(f"{tokenizer.OK} Parse Expression Rule Test Passed!")
# RULE: arithmetic_expression = term { "+" | "-" term }
def parse_expr(tokens):
    # Follows the same rule logic as parse_term
    # only now we focus on the tags being: "plus" || "minus"
    node, tokens = parse_term(tokens)
    while tokens[0]["tag"] in ["plus","minus"]:
        tag = tokens[0]["tag"]
        right_node, tokens = parse_term(tokens[1:])
        node = {"tag":tag, "left": node, "right": right_node}
    return node, tokens

def test_parse_arithmetic_expr():
    print(f"{tokenizer.INFO} Testing Parse Arithmetic Expression. . .")
    tokens = tokenizer.tokenize("1+2*3")
    ast,tokens = parse_arithmetic_expr(tokens)

    assert ast == {
        'tag': 'plus',
        'left': {'tag': 'number', 'value': 1},
        'right': {
                'tag': 'times',
                'left': {'tag': 'number', 'value': 2},
                'right': {'tag': 'number', 'value': 3}
            }
        }, f"{tokenizer.ERR} Invalid AST Generated!"

    # Test for various paranthesis grouping
    tokens = tokenizer.tokenize("2*(1+3)")
    ast,tokens = parse_arithmetic_expr(tokens)
    assert ast == {
        'tag': 'times',
        'left': {'tag': 'number', 'value': 2},
        'right': {'tag': 'plus', 'left': {'tag': 'number', 'value': 1}, 'right': {'tag': 'number', 'value': 3}}
        }, f"{tokenizer.ERR} Invalid AST Generated!"

    tokens = tokenizer.tokenize("(2*1)+3)")
    ast,tokens = parse_arithmetic_expr(tokens)
    assert ast == {
        'tag': 'plus',
        'left': {'tag': 'times', 'left': {'tag': 'number', 'value': 2}, 'right': {'tag': 'number', 'value': 1}},
        'right': {'tag': 'number', 'value': 3}
        }, f"{tokenizer.ERR} Invalid AST Generated!"
    
    tokens = tokenizer.tokenize("(2*(4+5))+3)")
    ast,tokens = parse_arithmetic_expr(tokens)
    assert ast == {
        'tag': 'plus',
        'left': {
            'tag': 'times',
            'left': {'tag': 'number', 'value': 2},
            'right': {'tag': 'plus', 'left': {'tag': 'number', 'value': 4}, 'right': {'tag': 'number', 'value': 5}}
        },
        'right': {'tag': 'number', 'value': 3}
        }, f"{tokenizer.ERR} Invalid AST Generated!"
    
    print(f"{tokenizer.OK} Parse Arithmetic Expression Rule Test Passed!")
def parse_arithmetic_expr(tokens):
    # arithmetic_expression = term { "+"|"-" term }
    node, tokens = parse_term(tokens)
    while tokens[0]["tag"] in ["plus","minus"]:
        tag = tokens[0]["tag"]
        right_node, tokens = parse_term(tokens[1:])
        node = {"tag":tag, "left": node, "right": right_node}
    return node, tokens


def test_parse_relational_expr():
    print(f"{tokenizer.INFO} Testing Parse Relational Expression. . .")
    for operator in ["<" , ">" , "<=" , ">=" , "==" , "!="]:
        tokens = tokenizer.tokenize(f"2{operator}4")
        ast, tokens = parse_relational_expr(tokens)
        assert ast == {
            "tag": operator,
            "left": {"tag": "number", "value": 2},
            "right": {"tag": "number", "value": 4},
        }, f"AST = [{ast}]"
    tokens = tokenizer.tokenize("2>4==3")
    ast, tokens = parse_relational_expr(tokens)  
    assert ast=={'tag': '==', 'left': {'tag': '>', 'left': {'tag': 'number', 'value': 2}, 'right': {'tag': 'number', 'value': 4}}, 'right': {'tag': 'number', 'value': 3}}

    print(f"{tokenizer.OK} Parse Relational Expression Rule Test Passed!")
def parse_relational_expr(tokens):
    # relational_expression = arithmetic_expression { ("<" | ">" | "<=" | ">=" | "==" | "!=") arithmetic_expression } ;
    node, tokens = parse_arithmetic_expr(tokens)
    while tokens[0]["tag"] in ["<",">",">=","<=","!=","=="]:
        tag = tokens[0]["tag"]
        right_node, tokens = parse_arithmetic_expr(tokens[1:])
        node = {"tag":tag, "left": node, "right": right_node}
    return node, tokens


def parse_assignment_stmt(tokens):
    """
        assignment_stmt = expr [ "=" expr ]
    """
    target, tokens = parse_expr(tokens)
    if tokens[0]["tag"] == "equals":
        tokens = tokens[1:]
        value, tokens = parse_expr(tokens)
        return {
                "tag": "assign",
                "target": target,
                "value": value
            }, tokens
def test_assignment_stmt():
    print()

# statement = <print> expression | expression
def test_parse_stmt():
    print(f"{tokenizer.INFO} Testing Parse Statement. . .")
    
    tokens = tokenizer.tokenize("1+(2+3)*4")
    ast, tokens = parse_stmt(tokens)
    assert ast == {'tag': 'plus', 'left': {'tag': 'number', 'value': 1}, 'right': {'tag': 'times', 'left': {'tag': 'plus', 'left': {'tag': 'number', 'value': 2}, 'right': {'tag': 'number', 'value': 3}}, 'right': {'tag': 'number', 'value': 4}}}
    
    tokens = tokenizer.tokenize("print 2*4")
    ast, tokens = parse_stmt(tokens)
    assert ast == {'tag': 'print', 'value': {'tag': 'times', 'left': {'tag': 'number', 'value': 2}, 'right': {'tag': 'number', 'value': 4}}}

    print(f"{tokenizer.OK} Parse Statement Rule Test Passed!")
# statement = <print> expression | expression
def parse_stmt(tokens):
    # if we are dealing with a print statement
    # we need to create a specific AST for it
    # to be later evaluated and executed by
    # the runner
    if tokens[0]["tag"] == "print":
        # parse the expression to get the value the print stmt will have
        value_ast, tokens = parse_expr(tokens[1:])
        ast = {
            'tag':'print',
            'value': value_ast
        }
    else:
        # parse the expression and return its AST
        # for the runner to handle
        ast, tokens = parse_expr(tokens)
    return ast, tokens

def test_parse_assignment_stmt():
    print(f"{tokenizer.INFO} Testing Parse Assignment Statement. . .")
    ast, tokens = parse_assignment_stmt(tokenizer.tokenize("i=2"))
    assert ast == {
        "tag": "assign",
        "target": {"tag": "identifier", "value": "i"},
        "value": {"tag": "number", "value": 2},
    }
    ast, tokens = parse_assignment_stmt(tokenizer.tokenize("2"))
    assert ast == {"tag": "number", "value": 2}
    print(f"{tokenizer.OK} Parse Assignment Statement Rule Test Passed!")
def parse_assignment_stmt(tokens):
    # assignment_statement = expression [ "=" expression ] ;
    target, tokens = parse_expr(tokens)
    if tokens[0]["tag"] == "equals":
        # parse the expression after the "=" token
        value, tokens = parse_expr(tokens[1:])
        return { # assign the value to the target
            'tag':'assign',
            'target': target,
            'value': value
        }, tokens
    return target, tokens


def parse_prgm(tokens):
    # program = [ statement { ";" statement } ] ;
    statements = []
    if tokens[0]["tag"]:
        # collect statements from the tokens
        statement, tokens = parse_stmt(tokens)
        statements.append(statement)
        # after parsing a statement we might have other
        # statements after the ";" we need to parse those too
        while tokens[0]["tag"] == ";":
            # remove the ";" token and parse the statement
            statement, tokens = parse_stmt(tokens[1:])
            statements.append(statement)
    assert tokens[0]["tag"] == None, f"Expected end of input, end token is {tokens[0]['value']}"
    # return the program with its statements and left over tokens
    return {
        "tag":"program",
        "statements": statements
    }, tokens
def test_parse_prgm():
    print(f"{tokenizer.INFO} Testing Parse Program. . .")
    
    tokens = tokenizer.tokenize("print 1; print 2")
    ast, tokens = parse_prgm(tokens)

    assert ast == {
        "tag": "program",
        "statements": [
            {"tag": "print", "value": {"tag": "number", "value": 1}},
            {"tag": "print", "value": {"tag": "number", "value": 2}},
        ],
    }

    print(f"{tokenizer.OK} Parse Program Rule Test Passed!")

# Used to parse statements
def parse(tokens):
    ast, tokens = parse_stmt(tokens)
    return ast

def main():
    test_parse_factor()
    test_parse_term()
    test_parse_expr()
    test_parse_stmt()
    test_parse_prgm()

    test_parse_arithmetic_expr()
    test_parse_relational_expr()
    test_parse_logical_factor()
    test_parse_assignment_stmt()

    print(f"{tokenizer.OK} Parser is Functional!")

if __name__ == "__main__":
    main()