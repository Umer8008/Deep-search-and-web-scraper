from langchain.agents import create_agent
from langchain_core.prompts import ChatPromptTemplate
from langchain_classic.output_parsers import StructuredOutputParser, ResponseSchema
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_mistralai import ChatMistralAI
from tools import web_search, web_scraper
import os
from dotenv import load_dotenv

load_dotenv()
llm=ChatGoogleGenerativeAI(model="gemini-3.6-flash", temperature=0)

# First Agent
def build_search_agent():
    return create_agent(
        model=llm,
        tools=[web_search],
            )

# Second Agent
def build_scraper_agent():
    return create_agent(
        model=llm,
        tools=[web_scraper],
        
    )

# ============================================================
# Writer chain (CORRECTED: added StructuredOutputParser)
# ============================================================
report_schemas = [
    ResponseSchema(name="introduction", description="Introduction section of the report"),
    ResponseSchema(name="key_findings", description="Minimum 3 well-explained key findings, as a bullet list"),
    ResponseSchema(name="conclusion", description="Conclusion section of the report"),
    ResponseSchema(name="sources", description="All URLs found in the research, as a list"),
]
report_parser = StructuredOutputParser.from_response_schemas(report_schemas)
report_format_instructions = report_parser.get_format_instructions()

writer_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are an expert research writer. Write clear, structured and insightful reports."),
    ("human", """Write a detailed research report on the topic below.

Topic: {topic}

Research Gathered:
{research}

Be detailed, factual and professional.

{format_instructions}"""),
]).partial(format_instructions=report_format_instructions)

writer_chain = writer_prompt | llm | report_parser

# ============================================================
# Critic chain (CORRECTED: added StructuredOutputParser)
# ============================================================
critic_schemas = [
    ResponseSchema(name="score", description="Score out of 10, e.g. '7/10'"),
    ResponseSchema(name="strengths", description="Strengths, as a bullet list"),
    ResponseSchema(name="areas_to_improve", description="Areas to improve, as a bullet list"),
    ResponseSchema(name="verdict", description="One line verdict"),
]
critic_parser = StructuredOutputParser.from_response_schemas(critic_schemas)
critic_format_instructions = critic_parser.get_format_instructions()

critic_prompt = ChatPromptTemplate.from_messages([
     ("system", "You are a sharp and constructive research critic. Be honest and specific."),
    ("human", """Review the research report below and evaluate it strictly.

Report:
{report}

{format_instructions}"""),
]).partial(format_instructions=critic_format_instructions)

critic_chain = critic_prompt | llm | critic_parser
