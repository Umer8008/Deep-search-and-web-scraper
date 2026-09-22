from langchain.tools import tool
from langchain_google_genai import ChatGoogleGenerativeAI

import requests

from bs4 import BeautifulSoup

from tavily import TavilyClient

import os

from dotenv import load_dotenv

from rich import print

from langchain_mistralai import ChatMistralAI

load_dotenv()

tavily_client = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))

llm = ChatGoogleGenerativeAI(
    model="gemini-3.6-flash",
    temperature=0
)


@tool
def web_search(query: str) -> str:

    """
    Perform a web search for recent and reliable information on a topic.
    Returns titles, urls and snippets using Tavily API and return the results.
    """

    try:
        response = tavily_client.search(
            query,
            max_results=5
        )

        output = []

        for r in response["results"]:
            output.append(
                f"Title: {r['title']}\n"
                f"URL: {r['url']}\n"
                f"Snippet: {r['content'][:300]}\n"
            )

        return "\n-------------------\n".join(output)

    except Exception as e:
        return f"An error occurred during web search: {str(e)}"


#print(web_search.invoke("What is the latest news on AI?"))
@tool
def web_scraper(url: str) -> str:
    """Scrape the content of a webpage and return the text."""
    try:
        response = requests.get(url,timeout=10,headers={"User-Agent": "Mozilla/5.0"},verify=False)
        soup = BeautifulSoup(response.content, "html.parser")
        for tag in soup(["script", "style", "header", "footer", "nav", "aside"]):
            tag.decompose()
        return soup.get_text(separator="\n", strip=True)[:3000]
    except Exception as e:
        return f"An error occurred while scraping the webpage: {str(e)}"
#print(web_scraper.invoke("https://en.wikipedia.org/wiki/Hindustan_Times") )   