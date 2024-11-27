from langchain_groq import ChatGroq
from dotenv import load_dotenv
load_dotenv()
import os
from langchain_community.tools import WikipediaQueryRun
from langchain_community.utilities import WikipediaAPIWrapper
from langchain_community.tools import GoogleSearchResults
from langchain_community.utilities import GoogleSearchAPIWrapper
from langchain_community.tools.wikidata.tool import WikidataAPIWrapper, WikidataQueryRun
from langchain_core.prompts import ChatPromptTemplate
from langchain.agents import create_tool_calling_agent,AgentExecutor
from langchain_core.prompts import MessagesPlaceholder
from langchain_google_community import GoogleSearchAPIWrapper, GoogleSearchResults




LLM = ChatGroq(temperature=0.30, groq_api_key="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", model_name="llama3-8b-8192")

#Creating tools object to be used by the agent.
wiki_api_wrapper = WikipediaAPIWrapper(top_k_results=4,doc_content_chars_max=2000)
tool = WikipediaQueryRun(api_wrapper=wiki_api_wrapper)
# goo_api_wrapper = GoogleSearchAPIWrapper(k=4, search_engine="google")
# tool2 = GoogleSearchResults(api_wrapper=goo_api_wrapper)
wikidata_api_wrapper = WikidataAPIWrapper(top_k_results=4,doc_content_chars_max=2000)
tool3 = WikidataQueryRun(api_wrapper=WikidataAPIWrapper())

os.environ["GOOGLE_API_KEY"] = os.getenv("GOOGLE_API_KEY")
os.environ["GOOGLE_CSE_ID"] = os.getenv("GOOGLE_CSE_ID")

tools = [tool,tool3]

MEMORY_KEY = "chat_history"
prompt = ChatPromptTemplate.from_messages(
    [
        ('''
            "system",
            You are an assistant tasked with helping users find the best movies and series according to their specific queries.
           
            1.Break down the user queries into multiple sub-queries to understand each aspect thoroughly. And use the combined knowledge to get the context from the tools.
            2.Use all available tools to gather relevant context and ensure a comprehensive response. Do not rely on a single tool; cross-check multiple sources.
            3.Retrieve and recommend only those documents that are highly relevant to the user's queries. And also give the reason why you have selected that particular movie
            4.You have to give the list of atleast 5 movies which is having the same description which user has entered and also give the explanation why you have selected that
            5.Avoid directing users to other sources; they are relying on your expertise.
            6.User doesn't know that you are using any tools please don't tell users that you are using any tools.
            7. If you don't know the answer then simply write I don't know don't give unnecessary output.
            8. If you are getting queries which are not related to movie and books you will not give any response 
                simply say i don't know
            9. you are just recommending movie so please check information about illegal or harmful words
            10. Please also find the IMDB Ratings for the results which you are showing
            
           
            
            <tools>
            {tools}
            </tools>
            
                  
            
        '''),
        MessagesPlaceholder(variable_name=MEMORY_KEY,optional=True),
        ("user", "{input}"),
        MessagesPlaceholder(variable_name="agent_scratchpad"),
    ]
)

#Creating and executing Agent which will retrieve the context from the tools.
agent = create_tool_calling_agent(LLM,tools,prompt)
agent_execute = AgentExecutor(agent=agent,tools=tools, verbose=True)

input_text = ''' Give me the list of movies which is tamil which is comedy genre and actor is surya'''
output = agent_execute.invoke({"input":input_text,"tools":tools})
output["output"]