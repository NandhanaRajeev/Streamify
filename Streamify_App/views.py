import os
from django.http import JsonResponse
from django.shortcuts import render,redirect
from django.views import View
from langchain_groq import ChatGroq
from dotenv import load_dotenv
from langchain_community.tools import WikipediaQueryRun
from langchain_community.utilities import WikipediaAPIWrapper
from langchain_community.tools import GoogleSearchResults
from langchain_community.utilities import GoogleSearchAPIWrapper
from langchain_core.prompts import ChatPromptTemplate
from langchain.agents import create_tool_calling_agent, AgentExecutor
from langchain_core.prompts import MessagesPlaceholder
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from .models import registrations
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

# Load environment variables from .env file
load_dotenv()

def movie_recommendation(request):
    if request.method == 'POST':
        input_text = request.POST['query']
        GOOGLE_API_KEY = "AIzaSyAu9dqPDzo7suh5zMsUOMrAaG_2JFJUw9Y"
        GOOGLE_CSE_ID = "320964686907d478a"

        # Check if the query parameter is empty
        if not input_text:
            return JsonResponse({"error": "No query provided"}, status=400)

        try:
            # Initialize the LLM (ChatGroq) and tools
            LLM = ChatGroq(
                temperature=0.30,
                groq_api_key="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",
                model_name="llama3-8b-8192"
            )

            # Creating tools objects to be used by the agent
            wiki_api_wrapper = WikipediaAPIWrapper(top_k_results=4, doc_content_chars_max=2000)
            wiki_tool = WikipediaQueryRun(api_wrapper=wiki_api_wrapper)

            # google_api_wrapper = GoogleSearchAPIWrapper(k=4, search_engine="google",google_api_key=GOOGLE_API_KEY,google_cse_id=GOOGLE_CSE_ID)
            # google_tool = GoogleSearchResults(api_wrapper=google_api_wrapper)
            wikidata_api_wrapper = WikidataAPIWrapper(top_k_results=4,doc_content_chars_max=2000)
            tool3 = WikidataQueryRun(api_wrapper=WikidataAPIWrapper())
            # List of tools to be used
            tools = [wiki_tool,tool3]

            # Define the memory key and prompt template for the agent
            MEMORY_KEY = "chat_history"
            prompt = ChatPromptTemplate.from_messages(
                [
                    ("system", '''
                        You are an assistant tasked with helping users find the best movies and series according to their specific queries.

                        1. Break down the user queries into multiple sub-queries to understand each aspect thoroughly.
                        2. Use all available tools to gather relevant context and ensure a comprehensive response.
                        3. Retrieve and recommend only those documents that are highly relevant to the user's queries, and explain why you selected that particular movie.
                        4. Provide a list of at least 5 movies with similar descriptions to the user's input and explain why you selected them.
                        5. Avoid directing users to other sources; they are relying on your expertise.
                        6. Do not disclose that you are using any tools to the user.
                        7. If you don't know the answer, simply say "I don't know."
                        8. For queries unrelated to movies and books, say "I don't know."
                        9. Ensure the recommended movies do not contain illegal or harmful content.
                        10. Include IMDB ratings for the movies.
                    '''),

                    MessagesPlaceholder(variable_name=MEMORY_KEY, optional=True),
                    ("user", "{input}"),
                    MessagesPlaceholder(variable_name="agent_scratchpad"),
                ]
            )

            # Creating and executing the agent
            agent = create_tool_calling_agent(LLM, tools, prompt)
            agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

            # Execute the query for movie recommendation
            output = agent_executor.invoke({"input": input_text, "tools": tools})
            movie_recommendations = output['output']
            

            # Return movie recommendations
            # return JsonResponse({"recommendations": movie_recommendations}, status=200)
            return JsonResponse({"recommendations": movie_recommendations}, status=200)

        except Exception as e:
            # Log the error and send a response
            print(f"Error occurred: {str(e)}")
            return JsonResponse({"error": f"An error occurred: {str(e)}"}, status=500)
    
    # Render the form or the page for GET request
    return render(request, 'movie.html')
    

# Render index page
def index(request):
    return render(request, 'index.html')

def analysis(request):
    return render(request, 'analysis.html')

# Render contact page
def sign_in(request):
    if request.method == 'POST':
        form_type = request.POST.get('form_type')  # Identify which form was submitted

        if form_type == 'signup':  # Handle Sign-Up
            email = request.POST.get('email')
            username = request.POST.get('username')
            password = request.POST.get('password')

            if User.objects.filter(username=username).exists():
                return render(request, 'sign_in.html', {'error': 'Username already used', 'active_form': 'signup'})

            # Create new user
            user = User.objects.create(username=username, password=make_password(password.strip()))
            user.save()

            registrations.objects.create(
                user=user,
                email=email
            )

            login(request, user)  # Log the user in after registration
            return redirect('home')

        elif form_type == 'login':  # Handle Login
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(username=username, password=password.strip())

            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                return render(request, 'sign_in.html', {'error': 'Invalid credentials', 'active_form': 'login'})

    return render(request, 'sign_in.html')
