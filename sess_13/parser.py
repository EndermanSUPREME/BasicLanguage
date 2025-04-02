import tokenizer

def test_parse_factor():
    # factor = <number> | <identifier> | "(" expression ")" | "!" expression | negated expression
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
    
    tokens = tokenizer.tokenize("-x")
    ast, tokens = parse_factor(tokens)
    assert ast == {'tag': 'identifier', 'value': '-x'}, f"{tokenizer.ERR} Parse Factor Rule Test Failed!"

    tokens = tokenizer.tokenize("!x")
    ast, tokens = parse_factor(tokens)
    assert ast == {'tag': 'not', 'value': {'tag': 'identifier', 'value': 'x'}}, f"{tokenizer.ERR} Parse Factor Rule Test Failed!"
    
    tokens = tokenizer.tokenize("(x+3)")
    ast, tokens = parse_factor(tokens)
    assert ast == {'tag': 'plus', 'left': {'tag': 'identifier', 'value': 'x'}, 'right': {'tag': 'number', 'value': 3}}, f"{tokenizer.ERR} Parse Factor Rule Test Failed!"
    
    tokens = tokenizer.tokenize("!(x+5)")
    ast, tokens = parse_factor(tokens)
    assert ast == {'tag': 'not', 'value': {'tag': 'plus', 'left': {'tag': 'identifier', 'value': 'x'}, 'right': {'tag': 'number', 'value': 5}}}, f"{tokenizer.ERR} Parse Factor Rule Test Failed!"

    tokens = tokenizer.tokenize("-(y+3)")
    ast, tokens = parse_factor(tokens)
    assert ast == {'tag': 'negate', 'value': {'tag': 'plus', 'left': {'tag': 'identifier', 'value': 'y'}, 'right': {'tag': 'number', 'value': 3}}}, f"{tokenizer.ERR} Parse Factor Rule Test Failed!"

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
    elif token["tag"] == "not":
        ast, tokens = parse_expr(tokens[1:])
        return {"tag": "not", "value": ast}, tokens
    elif token["tag"] == "minus":
        ast, tokens = parse_expr(tokens[1:])
        return {"tag": "negate", "value": ast}, tokens
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
    print(f"{tokenizer.INFO} Testing Parse Logical Factor. . .")
    for s in ["1", "2+2", "3<4"]:
        tokens = tokenizer.tokenize(s)
        ast1, tokens1 = parse_logical_factor(tokens)
        ast2, tokens2 = parse_relational_expr(tokens)
        assert ast1 == ast2
    print(f"{tokenizer.OK} Testing Parse Logical Factor Passed!")
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
    
    tokens = tokenizer.tokenize("x*2")
    ast, tokens = parse_term(tokens)
    assert ast == {'tag': 'times', 'left': {'tag': 'identifier', 'value': 'x'}, 'right': {'tag': 'number', 'value': 2}}, f"{tokenizer.ERR} Invalid AST Generated!"
    
    tokens = tokenizer.tokenize("-x*2")
    ast, tokens = parse_term(tokens)
    assert ast == {'tag': 'times', 'left': {'tag': 'identifier', 'value': '-x'}, 'right': {'tag': 'number', 'value': 2}}, f"{tokenizer.ERR} Invalid AST Generated!"
    
    tokens = tokenizer.tokenize("-(x*2)")
    ast, tokens = parse_term(tokens)
    assert ast == {'tag':'negate', 'value':{'tag': 'times', 'left': {'tag': 'identifier', 'value': 'x'}, 'right': {'tag': 'number', 'value': 2}}}, f"{tokenizer.ERR} Invalid AST Generated!"
    
    tokens = tokenizer.tokenize("!(x*2)")
    ast, tokens = parse_term(tokens)
    assert ast == {'tag':'not', 'value':{'tag': 'times', 'left': {'tag': 'identifier', 'value': 'x'}, 'right': {'tag': 'number', 'value': 2}}}, f"{tokenizer.ERR} Invalid AST Generated!"

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


    tokens = tokenizer.tokenize("2<3")
    ast, tokens = parse_relational_expr(tokens)  
    assert ast=={'tag': '<', 'left': {'tag': 'number', 'value': 2}, 'right': {'tag': 'number', 'value': 3}}

    tokens = tokenizer.tokenize("x != 5")
    ast, tokens = parse_relational_expr(tokens)
    assert ast=={'tag': '!=', 'left': {'tag': 'identifier', 'value': 'x'}, 'right': {'tag': 'number', 'value': 5}}

    print(f"{tokenizer.OK} Parse Relational Expression Rule Test Passed!")
def parse_relational_expr(tokens):
    # relational_expression = arithmetic_expression { ("<" | ">" | "<=" | ">=" | "==" | "!=") arithmetic_expression } ;
    node, tokens = parse_arithmetic_expr(tokens)
    while tokens[0]["tag"] in ["<",">",">=","<=","!=","=="]:
        tag = tokens[0]["tag"]
        right_node, tokens = parse_arithmetic_expr(tokens[1:])
        node = {"tag":tag, "left": node, "right": right_node}
    return node, tokens

def test_parse_logical_term():
    """
    logical_term = logical_factor { "&&" logical_factor }
    """
    print(f"{tokenizer.INFO} Testing Parse Logical Term. . .")

    tokens = tokenizer.tokenize("x")
    ast, tokens = parse_logical_term(tokens)
    assert ast == {"tag": "identifier", "value": "x"}

    tokens = tokenizer.tokenize("x&&y")
    ast, tokens = parse_logical_term(tokens)
    assert ast == {
        "tag": "&&",
        "left": {"tag": "identifier", "value": "x"},
        "right": {"tag": "identifier", "value": "y"},
    }

    tokens = tokenizer.tokenize("x&&y&&z")
    ast, tokens = parse_logical_term(tokens)
    assert ast == {
        "tag": "&&",
        "left": {
            "tag": "&&",
            "left": {"tag": "identifier", "value": "x"},
            "right": {"tag": "identifier", "value": "y"},
        },
        "right": {"tag": "identifier", "value": "z"},
    }

    print(f"{tokenizer.OK} Parse Logical Term Rule Test Passed!")
def parse_logical_term(tokens):
    """
    logical_term = logical_factor { "&&" logical_factor }
    """
    node, tokens = parse_logical_factor(tokens)
    while tokens[0]["tag"] == "&&":
        tag = tokens[0]["tag"]
        next_node, tokens = parse_logical_factor(tokens[1:])
        node = {"tag": tag, "left": node, "right": next_node}
    return node, tokens


def test_parse_logical_expr():
    """
    logical_expression = logical_term { "||" logical_term }
    """
    print(f"{tokenizer.INFO} Testing Parse Logical Expression. . .")

    tokens = tokenizer.tokenize("x")
    ast, tokens = parse_logical_expr(tokens)
    assert ast == {"tag": "identifier", "value": "x"}
    tokens = tokenizer.tokenize("x||y")
    ast, tokens = parse_logical_expr(tokens)
    assert ast == {
        "tag": "||",
        "left": {"tag": "identifier", "value": "x"},
        "right": {"tag": "identifier", "value": "y"},
    }
    tokens = tokenizer.tokenize("x||y&&z")
    ast, tokens = parse_logical_expr(tokens)
    assert ast == {
        "tag": "||",
        "left": {"tag": "identifier", "value": "x"},
        "right": {
            "tag": "&&",
            "left": {"tag": "identifier", "value": "y"},
            "right": {"tag": "identifier", "value": "z"},
        },
    }

    print(f"{tokenizer.OK} Parse Logical Expression Rule Test Passed!")
def parse_logical_expr(tokens):
    """
    logical_expression = logical_term { "||" logical_term }
    """
    node, tokens = parse_logical_term(tokens)
    while tokens[0]["tag"] == "||":
        tag = tokens[0]["tag"]
        next_node, tokens = parse_logical_term(tokens[1:])
        node = {"tag": tag, "left": node, "right": next_node}
    return node, tokens


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

    """
    statement = statement_block | if_stmt | while_stmt | function_stmt | return_stmt | print_stmt | assignment_stmt ;
    """
    tag = tokens[0]["tag"]
    if tag == "l_curly":
        return parse_stmt_block(tokens)
    if tag == "if":
        return parse_if_stmt(tokens)
    if tag == "while":
        return parse_while_stmt(tokens)
    if tag == "function":
        print(f"{tokenizer.INFO} Coming Soon!")
        #return parse_function_stmt(tokens)
    if tag == "return":
        print(f"{tokenizer.INFO} Coming Soon!")
        #return parse_return_stmt(tokens)
    if tag == "print":
        return parse_print_stmt(tokens)

    return parse_assignment_stmt(tokens)

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


def test_parse_stmt_block():
    print(f"{tokenizer.INFO} Testing Parse Statement Block. . .")
    ast = parse_stmt_block(tokenizer.tokenize("{}"))[0]
    assert ast == {'tag': 'block', 'statements': []}

    ast = parse_stmt_block(tokenizer.tokenize("{i=2}"))[0]
    assert ast == {'tag': 'block', 'statements': [{'tag': 'assign', 'target': {'tag': 'identifier', 'value': 'i'}, 'value': {'tag': 'number', 'value': 2}}]}
    
    ast = parse_stmt_block(tokenizer.tokenize("{i=2;k=3}"))[0]
    assert ast == {'tag': 'block', 
        'statements': [
            {'tag': 'assign', 'target': {'tag': 'identifier', 'value': 'i'}, 'value': {'tag': 'number', 'value': 2}}, 
            {'tag': 'assign', 'target': {'tag': 'identifier', 'value': 'k'}, 'value': {'tag': 'number', 'value': 3}}
            ]}

    print(f"{tokenizer.OK} Parse Statement Block Rule Test Passed!")
def parse_stmt_block(tokens):
    """
    statement_block = "{" statement { ";" statement } "}"
    """
    ast = {"tag": "block", "statements": []}
    assert tokens[0]["tag"] == "l_curly", f"Malformed Statement Block Token -> {tokens[0]['tag']}"
    tokens = tokens[1:] # remove the first token being l_curly

    if tokens[0]["tag"] != "r_curly": # end of block
        statement, tokens = parse_stmt(tokens)
        # print(statement)
        ast["statements"].append(statement)
    while tokens[0]["tag"] == ";":
        statement, tokens = parse_stmt(tokens[1:])
        # print(statement)
        ast["statements"].append(statement)

    assert tokens[0]["tag"] == "r_curly", f"Malformed Statement Block Token -> {tokens[0]['tag']}"
    return ast, tokens[1:]


def parse_print_stmt(tokens):
    """
    print_statement = "print" [ expression ] ;
    """
    assert tokens[0]["tag"] == "print"
    tokens = tokens[1:]
    if tokens[0]["tag"] in ["}", ";", None]:
        # no expression
        return {"tag": "print", "value": None}, tokens
    else:
        value, tokens = parse_expr(tokens)
        return {"tag": "print", "value": value}, tokens
def test_parse_print_stmt():
    """
    print_statement = "print" [ expression ] ;
    """
    print(f"{tokenizer.INFO} Testing Parse Print Statement. . .")
    ast = parse_print_stmt(tokenizer.tokenize("print 1"))[0]
    assert ast == {"tag": "print", "value": {"tag": "number", "value": 1}}
    print(f"{tokenizer.OK} Testing Parse Print Statement Passed!")


def parse_if_stmt(tokens):
    """
    if_statement = "if" "(" expression ")" statement_block [ "else" statement_block ]
    """
    assert tokens[0]["tag"] == "if"
    tokens = tokens[1:]

    assert tokens[0]["tag"] == "l_paran"
    tokens = tokens[1:]

    condition, tokens = parse_expr(tokens)
    assert tokens[0]["tag"] == "r_paran"
    tokens = tokens[1:]

    then_statement, tokens = parse_stmt_block(tokens)
    else_statement = None

    if tokens[0]["tag"] == "else":
        tokens = tokens[1:]
        else_statement, tokens = parse_stmt_block(tokens)

    ast = {
        "tag":"if",
        "condition":condition,
        "then":then_statement,
        "else":else_statement,
    }

    return ast, tokens
def test_parse_if_stmt():
    """
    if_statement = "if" "(" expression ")" statement_block [ "else" statement_block ]
    """
    print(f"{tokenizer.INFO} Testing Parse If Statement. . .")

    ast , _= parse_if_stmt(tokenizer.tokenize("if(1){print(2)}"))
    assert ast == {
        'tag': 'if', 
            'condition': {'tag': 'number', 'value': 1}, 
        'then': 
            {'tag': 'block', 'statements': [
                    {'tag': 'print', 'value': {'tag': 'number', 'value': 2}}
                ]
            }, 
        'else': None
    }
    
    ast , _= parse_if_stmt(
            tokenizer.tokenize("if(1){print(2)}else{print(3)}")
        )
    assert ast == {'tag': 'if', 'condition': {'tag': 'number', 'value': 1}, 'then': {'tag': 'block', 'statements': [{'tag': 'print', 'value': {'tag': 'number', 'value': 2}}]}, 'else': {'tag': 'block', 'statements': [{'tag': 'print', 'value': {'tag': 'number', 'value': 3}}]}}

    print(f"{tokenizer.OK} Testing Parse If Statement Passed!")

def parse_while_stmt(tokens):
    """
    while_statement = "while" "(" expression ")" statement_block 
    """
    assert tokens[0]["tag"] == "while"
    tokens = tokens[1:]

    assert tokens[0]["tag"] == "l_paran", f"Expected 'l_paran', got {tokens[0]['tag']}"
    tokens = tokens[1:]

    condition, tokens = parse_relational_expr(tokens)

    print(condition)

    assert tokens[0]["tag"] == "r_paran", f"Expected 'r_paran', got {tokens[0]['tag']}"
    tokens = tokens[1:]

    do_statement, tokens = parse_stmt_block(tokens)
    ast = {
        "tag":"while",
        "condition":condition,
        "do":do_statement,
    }

    return ast, tokens
def test_parse_while_stmt():
    """
    while_statement = "while" "(" expression ")" statement_block 
    """
    print(f"{tokenizer.INFO} Testing Parse While Statement. . .")

    ast , _= parse_while_stmt(tokenizer.tokenize("while(1){print(2)}"))
    assert ast == {
        'tag': 'while', 
        'condition': {'tag': 'number', 'value': 1}, 
        'do': 
            {'tag': 'block', 'statements': [
                {'tag': 'print', 'value': {'tag': 'number', 'value': 2}}]}
    }
    print(f"{tokenizer.OK} Testing Parse While Statement Passed!")

def parse_for_loop(tokens):
    """
    condition_statement = relational_expression
    update_statement = assignment_statement
    initializer_statement = assignment_statement
    for_loop = "for" "(" initializer_statement condition_statement update_statement ")" statemenet_block
    """

    assert tokens[0]["tag"] == "for"
    tokens = tokens[1:]

    assert tokens[0]["tag"] == "l_paran"
    tokens = tokens[1:]

    # parse the statements (assignment, condition, update)
    control = []

    # print("Looking at Init")
    # print(tokens, end="\n\n")

    assignment_stmt, tokens = parse_assignment_stmt(tokens)
    control.append(["init_stmt",assignment_stmt])
    assert tokens[0]["tag"] == ";"
    tokens = tokens[1:]

    # print("After Init")
    # print(tokens, end="\n\n")

    condition_stmt, tokens = parse_relational_expr(tokens)
    control.append(["condition_stmt",condition_stmt])
    assert tokens[0]["tag"] == ";"
    tokens = tokens[1:]

    # print("After Condition")
    # print(tokens, end="\n\n")

    update_stmt, tokens = parse_assignment_stmt(tokens)
    control.append(["update_stmt",update_stmt])
    assert tokens[0]["tag"] == ";"
    tokens = tokens[1:]

    assert tokens[0]["tag"] == "r_paran"
    tokens = tokens[1:]

    loop_stmt, tokens = parse_stmt_block(tokens)
    ast = {
        "tag":"for",
        "control":control,
        "loop":loop_stmt,
    }

    return ast, tokens
def test_parse_for_loop():
    print(f"{tokenizer.INFO} Testing Parse For Loop. . .")
    ast , _= parse_for_loop(tokenizer.tokenize("for(i=0;i<10;i=i+1;){print(i)}"))

    assert ast == {
            'tag': 'for',
            'control': [
                ['init_stmt', {'tag': 'assign', 'target': {'tag': 'identifier', 'value': 'i'}, 'value': {'tag': 'number', 'value': 0}}],
                ['condition_stmt', {'tag': '<', 'left': {'tag': 'identifier', 'value': 'i'}, 'right': {'tag': 'number', 'value': 10}}],
                ['update_stmt', {'tag': 'assign', 'target': {'tag': 'identifier', 'value': 'i'}, 'value': {'tag': 'plus', 'left': {'tag': 'identifier', 'value': 'i'}, 'right': {'tag': 'number', 'value': 1}}}]
            ],
            'loop': {
                'tag': 'block', 'statements': [
                    {'tag': 'print', 'value': {'tag': 'identifier', 'value': 'i'}}
                ]
            }
        }
    
    print(f"{tokenizer.OK} Testing Parse For Loop Passed!")

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


def parse_expr_list(tokens):
    """
    expression_list = "(" [ expression { "," expression } ] ")"
    """
    assert tokens[0]["tag"] == "l_paran", f"Expected 'l_paran' but got {tokens[0]}"
    tokens = tokens[1:]
    expressions = []
    if tokens[0]["tag"] != "r_paran":
        expr, tokens = parse_expr(tokens)
        expressions.append(expr)
        while tokens[0]["tag"] == ",":
            tokens = tokens[1:]
            expr, tokens = parse_expr(tokens)
            expressions.append(expr)
    assert tokens[0]["tag"] == "r_paran", f"Expected 'r_paran' but got {tokens[0]}"
    return {"tag": "expression_list", "expressions": expressions}, tokens[1:]
def test_parse_expr_list():
    print(f"{tokenizer.INFO} Testing Parse Expression List. . .")
    
    # Test empty list
    tokens = tokenizer.tokenize("()")
    ast, tokens = parse_expr_list(tokens)
    expected = {"tag": "expression_list", "expressions": []}
    assert ast == expected, f"Expected {expected}, got {ast}"
    assert tokens[0]["tag"] is None

    # Test one expression
    tokens = tokenizer.tokenize("(1)")
    ast, tokens = parse_expr_list(tokens)
    expected = {"tag": "expression_list", "expressions": [{"tag": "number", "value": 1}]}
    assert ast == expected, f"Expected {expected}, got {ast}"
    assert tokens[0]["tag"] is None

    # Test multiple expressions
    tokens = tokenizer.tokenize("(1,2,3)")
    ast, tokens = parse_expr_list(tokens)
    expected = {
        "tag": "expression_list",
        "expressions": [
            {"tag": "number", "value": 1},
            {"tag": "number", "value": 2},
            {"tag": "number", "value": 3},
        ],
    }
    assert ast == expected, f"Expected {expected}, got {ast}"
    assert tokens[0]["tag"] is None
    print(f"{tokenizer.OK} Parse Expression List Rule Test Passed!")


def parse_identifier_list(tokens):
    """
    identifier_list = "(" [ identifier { "," identifier } ] ")"
    """
    assert tokens[0]["tag"] == "l_paran", f"Expected 'l_paran' but got {tokens[0]}"
    tokens = tokens[1:]
    identifiers = []
    if tokens[0]["tag"] != "r_paran":
        expr, tokens = parse_expr(tokens)
        identifiers.append(expr)
        while tokens[0]["tag"] == ",":
            tokens = tokens[1:]
            identifier, tokens = parse_expr(tokens)
            assert identifier["tag"] == "identifier", f"Expected 'identifier' but got {identifier['tag']}"
            identifiers.append(identifier)
    assert tokens[0]["tag"] == "r_paran", f"Expected 'r_paran' but got {tokens[0]}"
    return {"tag": "identifier_list", "identifiers": identifiers}, tokens[1:]
def test_parse_identifier_list():
    print(f"{tokenizer.INFO} Testing Parse Identifier List. . .")
    
    # Test empty list
    tokens = tokenizer.tokenize("()")
    ast, tokens = parse_identifier_list(tokens)
    expected = {"tag": "identifier_list", "identifiers": []}
    assert ast == expected, f"Expected {expected}, got {ast}"
    assert tokens[0]["tag"] is None

    # Test one expression
    tokens = tokenizer.tokenize("(x)")
    ast, tokens = parse_identifier_list(tokens)
    expected = {"tag": "identifier_list", "identifiers": [{"tag": "identifier", "value": "x"}]}
    assert ast == expected, f"Expected {expected}, got {ast}"
    assert tokens[0]["tag"] is None

    # Test multiple expressions
    tokens = tokenizer.tokenize("(x,y,z)")
    ast, tokens = parse_identifier_list(tokens)
    expected = {
        "tag": "identifier_list",
        "identifiers": [
            {"tag": "identifier", "value": "x"},
            {"tag": "identifier", "value": "y"},
            {"tag": "identifier", "value": "z"},
        ],
    }
    assert ast == expected, f"Expected {expected}, got -> {ast}"
    assert tokens[0]["tag"] is None
    print(f"{tokenizer.OK} Parse Identifier List Rule Test Passed!")


def parse_function_literal(tokens):
    """
    function_literal = "function" identifier_list statement_block 
    """
    assert tokens[0]["tag"] == "function", f"Expected 'function', got {tokens[0]}"
    tokens = tokens[1:]
    parameters, tokens = parse_identifier_list(tokens)
    statements, tokens = parse_stmt_block(tokens)
    ast = {
        "tag":"function",
        "parameters" : parameters,
        "statements" : statements
    }
    return ast, tokens
def test_parse_function_literal():
    """
    function_literal = "function" identifier_list statement_block 
    """
    print(f"{tokenizer.INFO} Testing Parse Function Literal. . .")

    ast, tokens = parse_function_literal(tokenizer.tokenize("function (x) {}"))
    assert ast == {'tag': 'function', 'parameters': {'tag': 'identifier_list', 'identifiers': [{'tag': 'identifier', 'value': 'x'}]}, 'statements': {'tag': 'block', 'statements': []}}
    assert tokens[0]["tag"] == None
    
    print(f"{tokenizer.OK} Parse Function Literal Rule Test Passed!")


def parse_function_stmt(tokens):
    """
    function_statement = "function" identifier identifier_list statement_block
    """
    function_token = tokens[0]
    identifier_token = tokens[1]
    assignment_token = {'tag': '=', 'position': identifier_token["position"], 'value': '='}
    tokens = [identifier_token, assignment_token, function_token ] + tokens[2:]
    return parse_function_literal(tokens)
def test_parse_function_stmt():
    """
    function_statement = "function" identifier identifier_list statement_block
    """
    print(f"{tokenizer.INFO} Testing Parse Function Statement. . .")

    tokens = tokenizer.tokenize("function foo(x) {}")
    ast, _ = parse_function_stmt(tokens)
    print(ast)

    print(f"{tokenizer.OK} Parse Function Statement Rule Test Passed!")

# Used to parse statements
def parse(tokens):
    ast, tokens = parse_stmt(tokens)
    return ast

def main():
    test_parse_factor()
    test_parse_term()
    test_parse_expr()
    test_parse_stmt()
    test_parse_print_stmt()
    test_parse_prgm()

    test_parse_arithmetic_expr()
    test_parse_relational_expr()
    test_parse_assignment_stmt()

    test_parse_logical_factor()
    test_parse_logical_term()
    test_parse_logical_expr()

    test_parse_stmt_block()

    test_parse_if_stmt()
    test_parse_while_stmt()
    test_parse_for_loop()

    test_parse_expr_list()
    test_parse_identifier_list()

    test_parse_function_literal()
    print(f"{tokenizer.INFO} Test Parse Function Statement In Development. . .")
    # test_parse_function_stmt()

    print(f"{tokenizer.OK} Parser is Functional!")

if __name__ == "__main__":
    main()