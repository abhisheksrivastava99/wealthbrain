import os
import pandas as pd
from langchain_community.chat_models import ChatPerplexity
from langchain_core.prompts import ChatPromptTemplate

class ResearcherAgent:
    def __init__(self, family_name: str = "Wayne"):
        self.family_name = family_name
        self.portfolio_context = self._generate_portfolio_context(family_name)

    def _generate_portfolio_context(self, family_name: str) -> str:
        """
        Generates a portfolio context string from the CSV data for the specific family.
        """
        try:
            df = pd.read_csv("data/portfolio.csv")
            family_df = df[df['Family'] == family_name]
            
            if family_df.empty:
                return "Client Portfolio Profile: No data available."

            # Calculate Metrics
            total_aum = family_df['Value_USD'].sum()
            
            # Top Allocation by Asset Class
            allocation = family_df.groupby('Asset_Class')['Value_USD'].sum().sort_values(ascending=False)
            top_class = allocation.index[0] if not allocation.empty else "N/A"
            top_pct = (allocation.iloc[0] / total_aum * 100) if not allocation.empty else 0
            
            # Secondary Allocation
            second_class = allocation.index[1] if len(allocation) > 1 else "N/A"
            second_pct = (allocation.iloc[1] / total_aum * 100) if len(allocation) > 1 else 0
            
            # Cash Position
            cash_df = family_df[family_df['Asset_Class'] == 'Cash']
            cash_val = cash_df['Value_USD'].sum()
            cash_pct = (cash_val / total_aum * 100)
            
            # Top Assets Names (for flavor)
            top_assets = family_df.sort_values('Value_USD', ascending=False).head(3)['Asset_Name'].tolist()
            top_assets_str = ", ".join(top_assets)

            context = f"""
Client Portfolio Profile ({family_name} Family):
- Total AUM: ${total_aum:,.2f} USD
- Top Allocation: {top_pct:.1f}% {top_class}
- Secondary Allocation: {second_pct:.1f}% {second_class}
- Cash Position: {cash_pct:.1f}%
- Key Assets: {top_assets_str}
"""
            return context
        except Exception as e:
            return f"Client Portfolio Profile: Error loading data ({str(e)})"

    def run(self, query: str) -> str:
        """
        Executes the query against the Perplexity API with dynamic portfolio context.
        """
        pplx_api_key = os.getenv("PERPLEXITY_API_KEY")
        if not pplx_api_key:
            return "Error: PERPLEXITY_API_KEY not found in environment variables."

        try:
            chat = ChatPerplexity(
                temperature=0, 
                pplx_api_key=pplx_api_key, 
                model="sonar-reasoning"
            )
            
            system_prompt = """
You are the Chief Investment Strategist for an Ultra-High-Net-Worth Family Office. Your goal is to provide actionable market intelligence that is directly relevant to the client's specific portfolio.

Response Guidelines:

Persona: Be professional, objective, and concise. Avoid generic advice.

Contextual Relevance: You MUST explicitly mention how the market news impacts the specific assets listed in the 'Client Portfolio Profile'. (e.g., "This regulatory change is a tailwind for your US Tech holdings...").

Formatting:

Start with a "Bottom Line Up Front" (BLUF): A one-sentence summary in Bold.

Use ### Headers for distinct sections.

Use Bullet points for readability.

Citations:

Do NOT use inline citations like (Source: Bloomberg).

Instead, use small bracketed numbers like [1], inside the sentences.

At the very bottom of your response, create a section titled ### 📚 Sources and list the full source names/URLs there.

Input Structure:
User Question: {input}
{portfolio_context}
"""
            
            prompt = ChatPromptTemplate.from_messages(
                [
                    ("system", system_prompt),
                    ("human", "{input}"),
                ]
            )
            
            # Inject context into the prompt
            chain = prompt | chat
            response = chain.invoke({
                "input": query,
                "portfolio_context": self.portfolio_context
            })
            
            # Clean up response to remove <think> tags if present
            import re
            clean_content = re.sub(r'<think>.*?</think>', '', response.content, flags=re.DOTALL).strip()
            
            return clean_content
        except Exception as e:
            return f"Error executing researcher query: {str(e)}"

if __name__ == "__main__":
    from dotenv import load_dotenv
    load_dotenv()
    
    # Test with a specific family
    agent = ResearcherAgent(family_name="Lannister")
    print(f"Context Generated:\n{agent.portfolio_context}\n")
    print("-" * 50)
    print(agent.run("What is the outlook for gold mining?"))
