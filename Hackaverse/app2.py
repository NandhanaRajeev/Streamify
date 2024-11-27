import os
from django.http import JsonResponse
from django.shortcuts import render
from django.views import View
from langchain_groq import ChatGroq
from langchain_community.tools import WikipediaQueryRun
from langchain_community.utilities import WikipediaAPIWrapper
from langchain_community.tools import GoogleSearchResults
from langchain_community.utilities import GoogleSearchAPIWrapper
from langchain_core.prompts import ChatPromptTemplate
from langchain.agents import create_tool_calling_agent, AgentExecutor


class MovieRecommendationView(View):
    def get(self, request):
        # Rendering the movie recommendation page
        return render(request, 'movie_recommendation.html')

    def post(self, request):
        input_text = request.POST.get('query', '')
        
        # Check if the query parameter is empty
        if not input_text:
            return JsonResponse({"error": "No query provided"}, status=400)

        try:
            # Initialize the LLM and tools
            LLM = ChatGroq(temperature=0.30, groq_api_key="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", model_name="llama3-8b-8192")
            wiki_api_wrapper = WikipediaAPIWrapper(top_k_results=4, doc_content_chars_max=2000)
            tool = WikipediaQueryRun(api_wrapper=wiki_api_wrapper)
            goo_api_wrapper = GoogleSearchAPIWrapper(k=4, search_engine="google")
            tool2 = GoogleSearchResults(api_wrapper=goo_api_wrapper)

            tools = [tool, tool2]
            MEMORY_KEY = "chat_history"
            
            # Define the prompt template
            prompt = ChatPromptTemplate.from_messages(
                [
                    ("system", '''
                        You are an assistant tasked with helping users find the best movies and series according to their specific queries.
                        1. Break down the user queries into multiple sub-queries...
                        10. Please also find the IMDB Ratings for the results which you are showing.
                    '''),
                    ("user", input_text),
                ]
            )

            # Create and execute the agent
            agent = create_tool_calling_agent(LLM, tools, prompt)
            agent_execute = AgentExecutor(agent=agent, tools=tools, verbose=True)
            
            output = agent_execute.invoke({"input": input_text})

            # Return the recommendation in JSON format
            return JsonResponse({"recommendations": output["output"]})

        except Exception as e:
            # Log the error and send a response
            print(f"Error occurred: {str(e)}")
            return JsonResponse({"error": f"An error occurred: {str(e)}"}, status=500)