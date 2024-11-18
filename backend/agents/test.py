import asyncio
from crawl4ai import AsyncWebCrawler


# async def main():
#     async with AsyncWebCrawler(verbose=True) as crawler:
#         result = await crawler.arun(url="https://www.perplexity.ai/search/research-on-the-origin-of-equi-xIRtdoEFRv.Dp3fv57Tlfw")
#         print(f"Basic crawl result: {result.markdown[:500]}")  # Print first 500 characters
#         # save the result to a file
#         with open("perplexity_script_research.md", "w") as file:
#             file.write(result.markdown)
        
# asyncio.run(main())

import ollama
response = ollama.chat(model='llama3.2', messages=[
  {
    'role': 'user',
    'content': 'Why is the sky blue?',
  },
])
print(response['message']['content'])