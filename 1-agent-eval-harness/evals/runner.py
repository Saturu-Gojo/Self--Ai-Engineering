import time
import os
import sys
import json

#Add project root to python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

#import agent.py and evaluator.py
from agent.agent import run_agent
from evals.evaluator import evaluate


def load_dataset(path):
    with open(path,"r") as file:
        return json.load(file)


def run_evaluation(dataset):
    res = []

    for test_case in dataset:
        id = test_case["id"]
        input = test_case["input"]
        expected = test_case["expected"]

        start_time = time.time()

        actual = run_agent(input)

        latency = time.time() - start_time

        evaluation = evaluate(actual,expected)

        result = {
            "id":id,
            "input" : input,
            "expected":expected,
            "actual":actual,
            "passed":evaluation["passed"],
            "score":evaluation["score"],
            "latency":round(latency,4)

        }

        res.append(result)
    return res


def generate_report(res):
    total = len(res)
    passed = sum(
        1 for r in res
        if r["passed"]
    )
    failed = total - passed

    pass_rate = (passed/total)*100 if total>0 else 0

    avg_score = (
        sum(r["score"] for r in res)/total
        if total >0 
        else 0
    )
    avg_latency = (
        sum(r["latency"] for r in res)/total
        if total>0
        else 0
    )

    print("\n===================================")
    print("       AGENT EVALUATION REPORT")
    print("===================================")


    print(f"Total Tests:      {total}")
    print(f"Passed:           {passed}")
    print(f"Failed:           {failed}")
    print(f"Pass Rate:        {pass_rate:.2f}%")
    print(f"Average Score:    {avg_score:.2f}")
    print(f"Average Latency:  {avg_latency:.4f}s")

    print("\n-----------------------------------")
    print("TEST RESULTS")
    print("-----------------------------------")

    for r in res:
        status = "PASSED" if r["passed"] else "FAIL"

        print(
            f"{r['id']} |"
            f"{status}"
            f"Expected: {r['expected']} |"
            f"Actual : {r['actual']}"
        )

    failures = [
        result for result in res
        if not result["passed"]
    ]
    if failures:

        print("\n-----------------------------------")
        print("FAILURES")
        print("-----------------------------------")

        for result in failures:

            print(f"\nTest: {result['id']}")
            print(f"Input:    {result['input']}")
            print(f"Expected: {result['expected']}")
            print(f"Actual:   {result['actual']}")



if __name__=="__main__":
    dataset_path = os.path.join(
        os.path.dirname(__file__),
        "dataset.json"
    )

    dataset = load_dataset(dataset_path)

    results = run_evaluation(dataset)
    generate_report(results)

   