def classify_failure(agent_res, expected, expected_tool=None, timeout_limit=2.0, latency=0.0):
    """
    classify error into standard categories:
    - timeout
    - constraint_violation
    - wrong_tool
    - tool_failure
    - hallucination
    - wrong_answer

    """
    actual = str(agent_res['output']).strip()
    expected = str(expected).strip()
    tool_used=agent_res.get("tool_used")
    tool_status = agent_res.get("tool_status",{})

    if latency>timeout_limit:
        return "timeout"

    if tool_status.get("called") and not tool_status.get("success"):
        return "tool_failure"


    if expected_tool is not None and tool_used!=expected_tool:
        return "wrong_tool"

    max_allowed_step = 3
    if agent_res.get("steps",0)>max_allowed_step:
        return "constraint_violation"

    known_hallucination = ["london", "berlin", "madrid"]
    if actual.lower() in known_hallucination and actual.lower()!=expected.lower():
        return "hallucination"

    if actual!=expected:
        return "wrong_answer"
     



def evaluate(agent_res, expected, expected_tool=None, latency=0.0, timeout_limit=2.0):
    
   
    actual = str(agent_res["output"]).strip()
    expected = str(expected).strip()

    passed = (actual==expected) and (latency<=timeout_limit)

    if expected_tool is not None:
        passed = passed and (agent_res.get("tool_used")==expected_tool)

    failure_reason = None if passed else classify_failure(
        agent_res=agent_res,
        expected=expected,
        expected_tool=expected_tool,
        timeout_limit=timeout_limit,
        latency=latency
    )


    return {
        "passed":passed,
        "failure_reason":failure_reason
    }

if __name__ == "__main__":
    test_agent_res_1 = {
        "output": "60",
        "steps": 1,
        "tool_used": None,
        "tool_status": {"called": False, "success": True}
    }
    
    test_agent_res_2 = {
        "output": "70",
        "steps": 2,
        "tool_used": "Calculator",
        "tool_status": {"called": True, "success": True}
    }

    print(evaluate(test_agent_res_1, expected="70"))
    print(evaluate(test_agent_res_2, expected="70"))