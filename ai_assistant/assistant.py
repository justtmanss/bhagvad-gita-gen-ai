# assistant.py
import openai
import langsmith

# Initialize LangSmith with your API key
langsmith.api_key = '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'

openai.api_key = 'sk-jBF7Zi4kRM8VCc0xU25UbCGAuP4fipWe8jAVRiHzTQT3BlbkFJrxFL5I-o3gJn6H-B4ineZnsJ7C-MXvR_0oZyRMUV0A'

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
