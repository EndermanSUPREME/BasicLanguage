INFO = "\033[33m"+"[*]"+"\033[0m"
OK = "\033[32m"+"[+]"+"\033[0m"
ERR = "\033[31m"+"[-]"+"\033[0m"

def evaluate(ast):
    if ast["tag"] == "number":
        return ast["value"]
    if ast["tag"] in ["plus","minus","times","division"]:
        left_value = evaluate(ast["left"])
        right_value = evaluate(ast["right"])

def test_evaluate_number():
    print(f"{INFO} Testing Evaluation of Number. . .")
    assert evaluate({"tag":"number", "value":4}) == 4, f"{ERR} Something went Wrong!"
    print(f"{OK} Test Passed!")

def main():
    test_evaluate_number()

if __name__ == "__main__":
    main()