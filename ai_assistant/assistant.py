import openai
import langsmith

# Initialize LangSmith with your API key
langsmith.api_key = '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'

openai.api_key = 'sk-jBF7Zi4kRM8VCc0xU25UbCGAuP4fipWe8jAVRiHzTQT3BlbkFJrxFL5I-o3gJn6H-B4ineZnsJ7C-MXvR_0oZyRMUV0A'

def ask_krishna(question):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": question}
        ]
    )
    return response['choices'][0]['message']['content']
