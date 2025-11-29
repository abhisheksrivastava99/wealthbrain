import pandas as pd
from langchain_experimental.agents.agent_toolkits import create_pandas_dataframe_agent
from langchain_openai import ChatOpenAI
import os

class AnalystAgent:
    def __init__(self, family_name: str = "Wayne"):
        self.df = pd.read_csv("data/portfolio.csv")
        # Filter by family
        self.df = self.df[self.df['Family'] == family_name]
        
        self.llm = ChatOpenAI(model="gpt-4o", temperature=0)
        self.agent = create_pandas_dataframe_agent(
            self.llm,
            self.df,
            verbose=True,
            allow_dangerous_code=True, # Required for Pandas agent to execute Python
            agent_type="openai-tools",
        )

    def run(self, query: str) -> str:
        """
        Executes the query against the portfolio dataframe.
        """
        system_prompt = """
        You are a Data Analyst for a Family Office. You have access to a dataframe `df`.
        When asked for 'Total', sum the `Value_USD` column.
        When asked for 'Liquidity', filter by the `Liquidity` column.
        Always output the final answer in a complete sentence: 'The total value is $X'.
        """
        
        # We prepend the system prompt to the query to guide the agent
        full_query = f"{system_prompt}\n\nQuery: {query}"
        
        try:
            response = self.agent.invoke(full_query)
            return response["output"]
        except Exception as e:
            return f"Error executing analyst query: {str(e)}"

if __name__ == "__main__":
    # Test the agent
    from dotenv import load_dotenv
    load_dotenv()
    
    if not os.getenv("OPENAI_API_KEY"):
        print("Please set OPENAI_API_KEY in .env file")
    else:
        agent = AnalystAgent()
        print(agent.run("What is the total value of the portfolio?"))
