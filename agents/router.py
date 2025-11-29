from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from agents.analyst import AnalystAgent
from agents.lawyer import LawyerAgent
from agents.researcher import ResearcherAgent

class RouterAgent:
    def __init__(self, family_name: str = "Wayne"):
        self.llm = ChatOpenAI(model="gpt-4o", temperature=0)
        self.analyst = AnalystAgent(family_name=family_name)
        self.lawyer = LawyerAgent(family_name=family_name)
        self.researcher = ResearcherAgent(family_name=family_name)

    def route_and_execute(self, query: str) -> dict:
        """
        Analyzes the query and routes it to the appropriate agent.
        Returns a dictionary with 'agent' and 'response'.
        """
        system_prompt = """
        You are the Wealth Concierge Router. 
        Analyze the user's question and output ONLY the name of the single tool to use.
        
        TOOLS:
        1. 'Analyst': Use ONLY for questions about internal data facts. 
           - Examples: "How much cash do I have?", "What is my total AUM?", "List my tech stocks."
           - Keywords: Value, Amount, List, Allocation, Liquidity.
           
        2. 'Lawyer': Use for questions about legal documents.
           - Examples: "Who is the beneficiary?", "What are the trust terms?", "Can I sell this?"
           
        3. 'Researcher': Use for questions about external market trends, news, OR their impact on the portfolio.
           - CRITICAL: If the user asks "How does X affect my portfolio?", use RESEARCHER.
           - Examples: "Impact of tariffs on my stocks?", "Outlook for Tech sector?", "Tax implications of..."
        
        4. 'Hybrid': Use ONLY if the user asks two distinct questions that require combining internal facts AND external news.
           - Example: "What is the value of my Apple stock AND what is the latest news on Apple?"
        """
        
        prompt = ChatPromptTemplate.from_messages(
            [
                ("system", system_prompt),
                ("human", "{input}"),
            ]
        )
        
        chain = prompt | self.llm | StrOutputParser()
        
        try:
            route = chain.invoke({"input": query}).strip()
            print(f"DEBUG: Routed to {route}")
            
            if "Analyst" in route:
                result = {"agent": "Analyst", "response": self.analyst.run(query)}
            elif "Lawyer" in route:
                result = {"agent": "Lawyer", "response": self.lawyer.run(query)}
            elif "Researcher" in route:
                result = {"agent": "Researcher", "response": self.researcher.run(query)}
            elif "Hybrid" in route:
                print("DEBUG: Executing Hybrid Logic...")
                
                # Smart Context Fetching for Hybrid Queries
                # If the user asks about "impact" or "affect", we bypass the Analyst LLM and 
                # directly inject the raw portfolio dataframe to ensure the Combiner sees ALL assets.
                if any(keyword in query.lower() for keyword in ["affect", "impact", "influence", "consequence", "outlook"]):
                    print("DEBUG: Detected Impact Query - Injecting full portfolio dataframe...")
                    # Get the dataframe directly from the analyst agent instance
                    portfolio_str = self.analyst.df.to_markdown(index=False)
                    analyst_resp = f"Current Portfolio Holdings:\n{portfolio_str}"
                else:
                    # Default to passing the raw query
                    analyst_resp = self.analyst.run(query)

                researcher_resp = self.researcher.run(query)
                
                # DEBUG PRINT
                print(f"DEBUG - Analyst Says: {analyst_resp}") 
                print(f"DEBUG - Researcher Says: {researcher_resp}")

                # The Combiner Prompt: explicitly handles errors/empty responses
                combiner_prompt = f"""
                You are the Chief Investment Officer. I have gathered information from two sources to answer the user's query.
                
                User Query: {query}
                
                Source 1 (Client's Portfolio Data): 
                {analyst_resp}
                
                Source 2 (External Market Intelligence): 
                {researcher_resp}
                
                Instructions:
                1. ANALYZE: Look at the specific assets listed in Source 1.
                2. CONNECT: Explicitly map the market trends in Source 2 to the specific assets in Source 1.
                   - Example: "The tariff war impacts your [Asset Name] because it is in the [Sector] sector..."
                3. IGNORE Source 1 if it says "I don't know" or is empty, and just provide the market news.
                4. FORMAT: Use a professional, advisory tone. Use bullet points for specific asset impacts.
                """
                
                combiner_response = self.llm.invoke(combiner_prompt).content
                result = {"agent": "Hybrid", "response": combiner_response}
            
            else:
                result = {"agent": "Unknown", "response": "I'm not sure how to route this query."}

            # Global Cleaning: Remove <think> tags from any agent's response
            if "response" in result and isinstance(result["response"], str):
                import re
                result["response"] = re.sub(r'<think>.*?</think>', '', result["response"], flags=re.DOTALL).strip()
            
            return result
                
        except Exception as e:
            return {"agent": "Error", "response": f"Routing error: {str(e)}"}

if __name__ == "__main__":
    from dotenv import load_dotenv
    load_dotenv()
    
    router = RouterAgent()
    print(router.route_and_execute("How much is my Villa worth?"))
