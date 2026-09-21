from agents import build_search_agent, build_scraper_agent, writer_chain, critic_chain

def run_research_pipeline(topic:str)->dict:
    state={}
    #===============================
    # step 1: search agent working
    #===============================
    print("\n"+"="*50)
    print("Search agent is gathering information...")
    print("="*50+"\n")
    search_agent=build_search_agent()
    search_results=search_agent.invoke({
        "messages":[("human",f"Conduct a web search on the topic: {topic}. Provide titles, urls and snippets of relevant information.")],
    })
    state["search_results"] = search_results["messages"][-1].content
    print("\n search results",state["search_results"])
    
    #===============================
    # Step 2: scraper agent working
    #===============================
    
    print("\n"+"="*50)  
    print("Scraper agent is gathering information...")
    print("="*50+"\n")  
    scraper_agent=build_scraper_agent()
    scraper_results= scraper_agent.invoke({
        "messages":[("human",
            f"Scrape the content of the following search results about '{topic}' ,"
            f"pick the most relevant URL and reliable sources and scrape it for deeper conctent, \n\n"
            f"Search Results:\n{state['search_results'][:800]}"
            )]
        })
    state["scraper_results"] = scraper_results["messages"][-1].content
    print("\n scraper results",state["scraper_results"])
    
    #===============================
    # Now calling chains
    #===============================
    
    # Step 3: Writer chain working

    print("\n" + "=" * 50)
    print("Writer chain is generating content...")
    print("=" * 50 + "\n")

    combined_research = f"Search Results:\n{state['search_results']}\n\nScraper Results:\n{state['scraper_results']}"

    state["Report"] = writer_chain.invoke({
        "topic": topic,
        "research": combined_research
    })

    print("\nFinal Report generated:")
    print(state["Report"])


# ===============================
# Step 4: Critic chain working
# ===============================

    print("\n" + "=" * 50)
    print("Critic chain is reviewing the content...")
    print("=" * 50 + "\n")

    state["Critic Review"] = critic_chain.invoke({
        "report": state["Report"]
    })

    print("\nCritic Review generated:")
    print(state["Critic Review"])

    return state


if __name__ == "__main__":
    topic = input("Enter the research topic: ")
    final_state = run_research_pipeline(topic)

    print("\nResearch pipeline completed successfully.")