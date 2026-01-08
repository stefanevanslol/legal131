import asyncio
from openai import AsyncOpenAI
import os

async def test_openai():
    # Hardcoded key from ai_analyzer.py
    api_key = "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"
    
    client = AsyncOpenAI(api_key=api_key)
    
    print(f"Testing OpenAI with model='gpt-5'...")
    try:
        response = await client.chat.completions.create(
            model="gpt-5",
            messages=[
                {"role": "user", "content": "Hello, are you working?"}
            ],
            timeout=10.0 # Set a timeout to avoid indefinite hanging
        )
        print("Success!")
        print(response.choices[0].message.content)
    except Exception as e:
        print(f"Error with gpt-5: {e}")
        
    print("\nTesting OpenAI with model='gpt-4o'...")
    try:
        response = await client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "user", "content": "Hello, are you working?"}
            ],
             timeout=10.0
        )
        print("Success!")
        print(response.choices[0].message.content)
    except Exception as e:
        print(f"Error with gpt-4o: {e}")

if __name__ == "__main__":
    asyncio.run(test_openai())
