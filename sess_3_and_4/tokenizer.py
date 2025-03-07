import re

INFO = "\033[33m"+"[*]"+"\033[0m"
OK = "\033[32m"+"[+]"+"\033[0m"
ERR = "\033[31m"+"[-]"+"\033[0m"

# Define patterns for tokens
patterns = [
    [r"\d+", "number"], # regex for one-or-more digits 0-9
    [r"\+", "plus"], # regex for finding one plus-sign
    [r"\-", "minus"],
    [r"\*", "times"],
    [r"\/", "division"],
    [r"\(", "l_paran"],
    [r"\)", "r_paran"],
    [r"\s+", "white_space"],
    [r".","error"]
]

# Compile the patterns
for pattern in patterns:
    pattern[0] = re.compile(pattern[0])

def tokenize(characters):
    try:
        # default setup
        tokens = []
        position = 0

        while position < len(characters):
            # Match pattern with regex, Match tag with "number" or "plus"
            for pattern,tag in patterns:
                match = pattern.match(characters, position)
                if match:
                    break
            assert match, f"{characters} | Should have a match!"

            # process errors
            if tag == "error":
                raise Exception("Syntax Error")

            token = {
                "tag":tag,
                "position":position,
                "value":match.group(0)
            }

            # convert number tag value to a proper number
            if token["tag"] == "number":
                token["value"] = int(token["value"])

            # do not append tokens that are white-spaces
            if token["tag"] != "white_space":
                tokens.append(token)

            position = match.end()

        # Push to indicate end of tokens
        endToken = {
            "tag":None,
            "value":None,
            "position":position
        }
        tokens.append(endToken)

        return tokens
    except Exception as e:
        print(f"{ERR} {e}")
        return -1

# ===============================================================
# ========================= TESTS ===============================
# ===============================================================

def test_basic_token():
    try:
        print(f"{INFO} Testing Basic Token. . .")

        examples = [
            ["+", "plus"],
            ["-", "minus"],
            ["*", "times"],
            ["/", "division"],
            ["(", "l_paran"],
            [")", "r_paran"]
        ]
        
        for example in examples:
            t = tokenize(example[0])[0]

            # Characteristics of the Token
            assert t["tag"] == example[1] # token type (number|plus)
            assert t["position"] == 0 # 
            assert t["value"] == example[0] # value is the same as the token symbol being passed (+)

        return 0
    except Exception as e:
        print(f"{ERR} {e}")
        return -1

def test_number_token():
    try:
        print(f"{INFO} Testing Number Token. . .")
        for s in ["1","11"]:
            t = tokenize(s)
            assert len(t) == 2
            assert t[0]["tag"] == "number"
            assert t[0]["value"] == int(s)
        return 0
    except Exception as e:
        print(f"{ERR} {e}")
        return -1

def test_multiple_tokens():
    try:
        print(f"{INFO} Testing Multiple Tokens. . .")
        tokens = tokenize("1+2")
        expectedTokens = [{'tag': 'number', 'position': 0, 'value': 1}, {'tag': 'plus', 'position': 1, 'value': '+'}, {'tag': 'number', 'position': 2, 'value': 2}, {'tag': None, 'value': None, 'position': 3}]
        assert tokens == expectedTokens
        return 0
    except Exception as e:
        print(f"{ERR} {e}")
        return -1

def test_white_space_tokens():
    try:
        print(f"{INFO} Testing White Space Tokens. . .")
        tokens = tokenize("4 + 7")
        expectedTokens = [{'tag': 'number', 'position': 0, 'value': 4}, {'tag': 'plus', 'position': 2, 'value': '+'}, {'tag': 'number', 'position': 4, 'value': 7}, {'tag': None, 'value': None, 'position': 5}]
        assert tokens == expectedTokens
        return 0
    except Exception as e:
        print(f"{ERR} {e}")
        return -1
    
def test_invalid_token():
    try:
        print(f"{INFO} Testing White Space Tokens. . .")
        tokens = tokenize("$4+7")
        assert tokens != -1, "Potential Invalid Token Detected!"
        return 0
    except Exception as e:
        print(f"{ERR} {e}")
        return -1

def main():
    assert test_basic_token() == 0
    print(f"{OK} Basic Token Test Passed!\n")

    assert test_number_token() == 0
    print(f"{OK} Number Token Test Passed!\n")

    assert test_multiple_tokens() == 0
    print(f"{OK} Multiple Tokens Test Passed!\n")

    assert test_white_space_tokens() == 0
    print(f"{OK} White Space Tokens Test Passed!\n")

    assert test_invalid_token() == -1
    print(f"{OK} Invalid Tokens Detected Passed!\n")

if __name__ == "__main__":
    main()