def evaluate(actual, expected):
    actual = str(actual).strip()
    expected = str(expected).strip()

    if actual==expected:
        return {
            "passed":True,
            "score":1.0
        }
    return {
        "passed":False,
        "score":0.0
    }

if __name__=="__main__":
    print(evaluate("60","70"))
    print(evaluate("70","60"))