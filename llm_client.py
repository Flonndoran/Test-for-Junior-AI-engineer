import os
from dotenv import load_dotenv

load_dotenv()

class LLMClient:
    def __init__(self, model='gpt-3.5-turbo'):
        import openai
        self.model = model
        
        api_key = os.environ.get('OPENAI_API_KEY')
        if not api_key:
            raise ValueError("OPENAI_API_KEY not found")
        
        # Проверяем ключ на нелатинские символы
        if not api_key.isascii():
            raise ValueError(f"API key contains non-ASCII chars: {api_key[:10]}...")
        
        self.client = openai.OpenAI(api_key=api_key)
    
    def ask(self, data_summary, question):
        prompt = f"""Use ONLY data below. Answer in Russian.

DATA (year revenue growth% op_margin% net_margin%):
{data_summary}

Question: {question}

Answer in Russian:"""
        
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3,
            max_tokens=500
        )
        
        return response.choices[0].message.content