import os
import sys
from dotenv import load_dotenv

# Load env vars
load_dotenv()

def test_analyst():
    print("\n--- Testing Analyst Agent ---")
    try:
        from agents.analyst import AnalystAgent
        agent = AnalystAgent()
        # Simple query that might work even without complex LLM reasoning if the agent is robust, 
        # but it definitely needs OpenAI key.
        if not os.getenv("OPENAI_API_KEY"):
            print("SKIPPING: No OPENAI_API_KEY found.")
            return
            
        response = agent.run("What is the total value of the portfolio?")
        print(f"Response: {response}")
    except Exception as e:
        print(f"FAILED: {e}")

def test_lawyer():
    print("\n--- Testing Lawyer Agent ---")
    try:
        from agents.lawyer import LawyerAgent
        if not os.getenv("OPENAI_API_KEY"):
            print("SKIPPING: No OPENAI_API_KEY found.")
            return
            
        agent = LawyerAgent()
        response = agent.run("Who are the beneficiaries?")
        print(f"Response: {response}")
    except Exception as e:
        print(f"FAILED: {e}")

def test_researcher():
    print("\n--- Testing Researcher Agent ---")
    try:
        from agents.researcher import ResearcherAgent
        if not os.getenv("PERPLEXITY_API_KEY"):
            print("SKIPPING: No PERPLEXITY_API_KEY found.")
            return
            
        agent = ResearcherAgent()
        response = agent.run("What is the current inflation rate in the UK?")
        print(f"Response: {response}")
    except Exception as e:
        print(f"FAILED: {e}")

def test_router():
    print("\n--- Testing Router Agent ---")
    try:
        from agents.router import RouterAgent
        if not os.getenv("OPENAI_API_KEY"):
            print("SKIPPING: No OPENAI_API_KEY found.")
            return
            
        agent = RouterAgent()
        response = agent.route_and_execute("How much is my Villa worth?")
        print(f"Response: {response}")
    except Exception as e:
        print(f"FAILED: {e}")

if __name__ == "__main__":
    print("Starting System Verification...")
    test_analyst()
    test_lawyer()
    test_researcher()
    test_router()
    print("\nVerification Complete.")
