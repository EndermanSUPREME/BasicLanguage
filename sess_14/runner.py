import tokenizer
import parser
import evaluator
import sys

# read tokens from a file and evaluate the contents
def run(text):
    tokens = tokenizer.tokenize(text)
    ast = parser.parse(tokens)

    # print("\033[36m")
    # print(ast)
    # print("\033[0m")

    evaluator.evaluate(ast)

if __name__ == "__main__":
    if len(sys.argv) > 1:
        with open(sys.argv[1],"r") as f:
            source = f.read()
        run(source)
    else:
        print(f"{tokenizer.ERR} Usage: {sys.argv[0]} [files]")