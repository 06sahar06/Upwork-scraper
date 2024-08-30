OPENAI_API_KEY="insert your api key here"

import streamlit as st
import os
from crawl4ai import WebCrawler
from crawl4ai.extraction_strategy import LLMExtractionStrategy
from pydantic import BaseModel, Field

crawler = WebCrawler()

crawler.warmup()
url=st.text_input("lien à scraper")
result = crawler.run(url=f"{url}")

instructions = """
From the crawled content, extract all candidate details including:
- The full name of the candidate.
- The candidate's job success rate (e.g., 90%).
- The candidate's job title (e.g., Data Engineer).
- The candidate's country.

Each extracted candidate should be formatted as follows:
{
    "candidate_name": "John Doe",
    "job_success": "90%",
    "job_title": "Data Engineer",
    "candidate_country": "India"
}

Make sure to extract this information accurately, and if any information is missing, return "N/A" instead of an empty string.
"""


class CandidateInfo(BaseModel):
    candidate_name: str = Field(..., description="Name of the candidate.")
    job_success: str = Field(..., description="Job success of that candidate.")
    job_title: str = Field(..., description="the job title of the candidate .")
    candidate_country: str = Field (..., description= "the country of the candidate.")

url="https://www.upwork.com/nx/search/talent/?category_uid=531770282580668420&occupation_uid=1737190722364944386"
crawler = WebCrawler()
crawler.warmup()

result = crawler.run(
        url=url,
        word_count_threshold=1,
        extraction_strategy= LLMExtractionStrategy(
            provider= "groq/llama3-8b-8192",
            api_token = OPENAI_API_KEY,
            schema=CandidateInfo.schema(),
            extraction_type="schema",
            instruction=instructions
        ),
        bypass_cache=True,
    )

st.write(result.extracted_content)

