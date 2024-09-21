# assistant.py
import openai

openai.api_key = 'your-api-key'

def get_answer(question):
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=f"Answer this based on the Bhagavad Gita: {question}",
        max_tokens=150
    )
    return response.choices[0].text.strip()

if __name__ == "__main__":
    question = "What should I do in times of doubt?"
    print(get_answer(question))
