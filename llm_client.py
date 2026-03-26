import os
import requests
import json

class LLMClient:
    """Клиент для работы с LLM (поддержка OpenAI и Ollama)"""
    
    def __init__(self, provider='ollama', model='llama3.2', api_key=None):
        self.provider = provider
        self.model = model
        
        if provider == 'openai':
            import openai
            self.client = openai.OpenAI(api_key=api_key or os.environ.get('OPENAI_API_KEY'))
    
    def ask(self, data_summary, question):
        """Отправляет запрос к LLM и возвращает ответ"""
        prompt = self._build_prompt(data_summary, question)
        
        if self.provider == 'openai':
            return self._ask_openai(prompt)
        elif self.provider == 'ollama':
            return self._ask_ollama(prompt)
        else:
            raise ValueError(f"Unknown provider: {self.provider}")
    
    def _build_prompt(self, data_summary, question):
        """Собирает промпт с инструкциями и данными"""
        return f"""Ты — финансовый ассистент. Твоя задача — отвечать на вопросы о финансовых показателях компании.

ПРАВИЛА:
1. Используй ТОЛЬКО данные, которые приведены ниже.
2. НЕ придумывай никаких числовых значений, которых нет в данных.
3. Если в данных нет информации для ответа — скажи об этом честно.
4. Отвечай понятно и структурированно.
5. При необходимости объясняй, как ты пришел к выводу.

ДАННЫЕ ПО ГОДАМ (2005-2024):
{data_summary}

ВОПРОС ПОЛЬЗОВАТЕЛЯ:
{question}

ОТВЕТ АССИСТЕНТА:"""
    
    def _ask_openai(self, prompt):
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3
        )
        return response.choices[0].message.content
    
    def _ask_ollama(self, prompt):
        url = "http://localhost:11434/api/generate"
        payload = {
            "model": self.model,
            "prompt": prompt,
            "stream": False,
            "options": {"temperature": 0.3}
        }
        response = requests.post(url, json=payload)
        return response.json()["response"]

if __name__ == "__main__":
    # Тестовый запуск (требуется запущенный Ollama)
    client = LLMClient(provider='ollama', model='llama3.2')
    test_data = "2006: revenue=$155,000, growth=29.2%, op_margin=24.5%, net_margin=24.5%"
    answer = client.ask(test_data, "В каком году был самый быстрый рост выручки?")
    print(answer)