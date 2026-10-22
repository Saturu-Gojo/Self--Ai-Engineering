def calculator(exp):
    try:
        result = eval(exp)
        return {
            "success":True,
            "result":str(result),
            "error":None
        }
    except Exception as e:
        return{
            "success":False,
            "result":None,
            "error":str(e)
        }

def run_agent(input):
    inp = input.lower()
    step =1
    tool_used = None
    tool_status = {"called":False, "success":True, "error":None}
    
    if(inp=="what is 15*4?"):
        return {
            "output":"60",
            "steps":step,
            "tool_used":None,
            "tool_status":tool_status
        }
    if inp == "what is 20+35?":
        return {
            "output":"55",
            "steps":step,
            "tool_used":None,
            "tool_status":tool_status
        }
    if inp.startswith("calculate"):
        step+=1
        tool_used="Calculator"
        exp = inp.replace("calculate","").strip()

        cal_res=calculator(exp)
        tool_status["called"]=True
        tool_status["success"]=cal_res["success"]
        tool_status["error"]=cal_res["error"]

    if cal_res["success"]:
        return {
            "output":cal_res["result"],
            "steps":step,
            "tool_used":tool_used,
            "tool_status":tool_status
        }
    else:
        return {
            "output":"Error evaluating expression",
            "steps":step,
            "tool_used":tool_used,
            "tool_status":tool_status
        }

    #intent where a non-existent tool would be needed
    if inp.startswith("search"):
        step+=1
        return {
            "output":"Paris",
            "steps":step,
            "tool_used":"SearchEngine",
            "tool_status":tool_status
        }

    # simulate hallucination cases
    if "capital of france" in inp:
        return {
            "output":"London",
            "steps":step,
            "tool_used":None,
            "tool_status":tool_status
        }

    return {
        "output": "I don't know",
        "steps": steps,
        "tool_used": None,
        "tool_status": tool_status
    }

if __name__=="__main__":
    query = input("User: ")
    response = run_agent(query)

    print("Agent:",response)