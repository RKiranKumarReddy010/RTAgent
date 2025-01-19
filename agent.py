from phi.agent import Agent
from phi.model.groq import Groq
from phi.model.ollama import Ollama
from phi.tools.yfinance import YFinanceTools
from phi.tools.duckduckgo import DuckDuckGo
from phi.tools.email import EmailTools
from phi.tools.shell import ShellTools
from phi.tools.searxng import Searxng
from phi.tools.youtube_tools import YouTubeTools

youtube_tool = Agent(
    tools=[YouTubeTools()],
    show_tool_calls=True,
    description="This is a agent that able to get data from youtube. either video summerisation or video search.",
    model=Groq(id="llama-3.3-70b-versatile"),
)

searxng = Searxng(
    host="http://172.17.2.0:8888",
    engines=[
        # Web Search Engines
        "google", "bing", "duckduckgo", "qwant", "yahoo", 
        
        # Academic & Research
        "google scholar", "semantic scholar", "base", "crossref",
        
        # Social Media
        "reddit", "twitter", "github", "gitlab", 
        
        # Multimedia
        "youtube", "vimeo", "soundcloud", "flickr", 
        
        # News
        "google news", "bing news", "yahoo news", "reuters",
        
        # Specialized Engines
        "wikipedia", "wikidata", "stackexchange", 
        
        # File & Torrent
        "1337x", "piratebay", "nyaa", 
        
        # Coding & Tech
        "dockerhub", "npm", "pypi", "arch linux",
        
        # Geospatial
        "openstreetmap", "google maps",
        
        # Specialized Vertical Searches
        "bandcamp", "genius", "discogs", # Music
        "arxiv", "pubmed", # Scientific Research
        "stackoverflow" # Programming Q&A
    ],
    fixed_max_results=5,
    news=True,
    science=True,
)


receiver_email = "ki2003167@gmail.com"
sender_email = "rkirankumarreddygenaisj@gmail.com"
sender_name = "Kiran Reddy"
sender_passkey = "eufu uvls crzg xwkh"

mail_agent = Agent(
    name="Email Agent",
    tools=[
        EmailTools(
            receiver_email=receiver_email,
            sender_email=sender_email,
            sender_name=sender_name,
            sender_passkey=sender_passkey,
        )
    ],
    model=Ollama(id='llama3.2:1b'),
)

web_search_agent = Agent(
    name="Web Search Agent",
    role="Search the web for information and get the top 10 site links related to query.",
    model=Groq(id="llama-3.3-70b-versatile"),
    tools=[DuckDuckGo()],
    instructions=["Always include the source"],
    show_tool_calls=True,
    markdown=True,
)


finance_agent = Agent(
    name = "Finance Agent",
    model=Ollama(id='llama3.2:1b'),
    tools=[YFinanceTools(stock_price=True,analyst_recommendations=True,stock_fundamentals=True)],
    instructions=["Display the output using tabular data"],
    show_tool_calls=True,
    markdown=True
)

multi_agent = Agent(
    team=[finance_agent,mail_agent,youtube_tool],
    instructions=  ["always include the source", "Display the output as tabular format"],
    model=Groq(id="llama-3.3-70b-versatile"),
    show_tool_calls=True,
    markdown=True,
)


while(1):
    a = input(" Your Query: ")
    multi_agent.print_response(a)
