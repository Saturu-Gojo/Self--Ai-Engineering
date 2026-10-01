def run_agent(input):
    inp = input.lower()
    if(inp=="what is 15*4?"):
        return "60"
    if inp == "what is 20 + 35?":
        return "55"

    return "I don't know"

if __name__=="__main__":
    query = input("User: ")
    response = run_agent(query)

    print("Agent:",response)