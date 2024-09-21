import openai
import langsmith

# Initialize LangSmith with your API key
langsmith.api_key = 'YOUR_LANGSMITH_API_KEY'

openai.api_key = 'YOUR_OPENAI_API_KEY'

def ask_krishna(question):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": question}
        ]
    )
    return response['choices'][0]['message']['content']
