import os
from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_community.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain

class LawyerAgent:
    def __init__(self, family_name: str = "Wayne"):
        self.family_name = family_name.lower()
        self.embeddings = OpenAIEmbeddings()
        self.vector_store = self._build_vector_store()
        self.llm = ChatOpenAI(model="gpt-4o", temperature=0)
        
    def _build_vector_store(self):
        """
        Loads documents, splits them, and creates a FAISS vector store.
        In a real app, this would persist to disk and load if exists.
        """
        # Load from specific family directory
        path = f"data/legal_docs/{self.family_name}"
        if not os.path.exists(path):
            print(f"Warning: Path {path} does not exist. Using default.")
            path = "data/legal_docs/wayne"
            
        loader = DirectoryLoader(path, glob="**/*.txt", loader_cls=TextLoader)
        docs = loader.load()
        
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=100
        )
        splits = text_splitter.split_documents(docs)
        
        vector_store = FAISS.from_documents(splits, self.embeddings)
        return vector_store

    def run(self, query: str) -> str:
        """
        Executes the query against the legal documents.
        """
        retriever = self.vector_store.as_retriever(search_type="mmr")
        
        system_prompt = (
            "You are a Lawyer for a Family Office. "
            "Use the following pieces of retrieved context to answer "
            "the question. If you don't know the answer, say that you "
            "don't know. Use three sentences maximum and keep the "
            "answer concise."
            "\n\n"
            "{context}"
        )
        
        prompt = ChatPromptTemplate.from_messages(
            [
                ("system", system_prompt),
                ("human", "{input}"),
            ]
        )
        
        question_answer_chain = create_stuff_documents_chain(self.llm, prompt)
        rag_chain = create_retrieval_chain(retriever, question_answer_chain)
        
        try:
            response = rag_chain.invoke({"input": query})
            return response["answer"]
        except Exception as e:
            return f"Error executing lawyer query: {str(e)}"

if __name__ == "__main__":
    from dotenv import load_dotenv
    load_dotenv()
    
    if not os.getenv("OPENAI_API_KEY"):
        print("Please set OPENAI_API_KEY in .env file")
    else:
        agent = LawyerAgent()
        print(agent.run("Who are the beneficiaries of the will?"))
