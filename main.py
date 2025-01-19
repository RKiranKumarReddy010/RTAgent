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


Shell_agent = Agent(
    name="Shell Agent",
    #model=Ollama(id="mistral-nemo:latest"),
    model=Groq(id="llama-3.3-70b-versatile"),
    tools=[ShellTools()],
    instructions=["You are responsible for executing the shell commands for windows os. "],
    show_tool_calls=True,
    markdown=True
)

Memory_agent = Agent(
    #model=Ollama(id="mistral-nemo:latest"),
    model=Groq(id="llama-3.3-70b-versatile"),
    storage=SqlAgentStorage(table_name="agent_sessions", db_file="tmp/agent_storage.db"),
    add_history_to_messages=True,
    description="You need to store the response locally. When i run a instruction always refer to previous results and instruction. Based on that run this for current state.",
)

console = Console()

Multi_agent = Agent(
    team=[Shell_agent],
    instructions=  ["always include the source.Also store the previous responses as memory."],
    #model=Ollama(id="mistral-nemo:latest"),
    model=Groq(id="llama-3.3-70b-versatile"),
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
