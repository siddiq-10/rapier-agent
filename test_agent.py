from agent.core import run_agent

if __name__ == "__main__":
    query = "Give me latest market insights about Razorpay and its competitors"
    result = run_agent(query)

    print("\n\n=========== FINAL ANSWER ===========")
    print(result)
    print("====================================")