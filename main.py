from phi.agent import Agent
from phi.model.groq import Groq
from phi.model.ollama import Ollama 
from phi.tools.shell import ShellTools 
import json
from rich.console import Console
from rich.panel import Panel
from rich.json import JSON
from phi.agent import Agent
from phi.model.openai import OpenAIChat
from phi.storage.agent.sqlite import SqlAgentStorage
from phi.agent import Agent
from phi.model.openai import OpenAIChat
from phi.embedder.ollama import OllamaEmbedder
from phi.knowledge.csv import CSVUrlKnowledgeBase
from phi.vectordb.lancedb import LanceDb, SearchType

# Create a knowledge base from a PDF
knowledge_base = CSVUrlKnowledgeBase(
    urls=["https://phi-public.s3.amazonaws.com/recipes/ThaiRecipes.pdf"],
    # Use LanceDB as the vector database
    vector_db=LanceDb(
        table_name="recipes",
        uri="tmp/lancedb",
        search_type=SearchType.vector,
        embedder=OllamaEmbedder(model="nomic-embed-text:latest"),
    ),
)
knowledge_base.load(recreate=False)

agent = Agent(
    model=OpenAIChat(id="gpt-4o"),
    # Add the knowledge base to the agent
    knowledge=knowledge_base,
    show_tool_calls=True,
    markdown=True,
)

Shell_agent = Agent(
    name="Shell Agent",
    model=Ollama(id="mistral-nemo:latest"),
    #model=Groq(id="llama-3.3-70b-versatile"),
    tools=[ShellTools()],
    instructions=["You are responsible for executing the shell commands for windows os. "],
    show_tool_calls=True,
    markdown=True
)

Memory_agent = Agent(
    model=Ollama(id="mistral-nemo:latest"),
    #model=Groq(id="llama-3.3-70b-versatile"),
    storage=SqlAgentStorage(table_name="agent_sessions", db_file="tmp/agent_storage.db"),
    add_history_to_messages=True,
    description="You need to store the response locally. When i run a instruction always refer to previous results and instruction. Based on that run this for current state.",
)

console = Console()

Multi_agent = Agent(
    team=[Shell_agent],
    instructions=  ["always include the source.Also store the previous responses as memory."],
    model=Ollama(id="mistral-nemo:latest"),
    #model=Groq(id="llama-3.3-70b-versatile"),
    show_tool_calls=True,
    markdown=True,
)

def print_chat_history(agent):
    console.print(
        Panel(
            JSON(json.dumps([m.model_dump(include={"role", "content"}) for m in agent.memory.messages]), indent=4),
            title=f"Chat History for session_id: {agent.session_id}",
            expand=True,
        )
    )
#Memory_agent.print_response("Share a 2 sentence horror story", stream=True)
#print_chat_history(Multi_agent)
#Multi_agent.print_response("What was my first message?", stream=True)
#print_chat_history(Multi_agent)


while(True):
    query = input("Enter Your Query:")
    Multi_agent.print_response(query)
    if str(input("Are u want to close:(y/n)")) in  ["y","Y"]:
        break
    
