import sys
from data_processor import load_and_process_data, get_data_summary
from llm_client import LLMClient

def main():
    print("💰 Загрузка финансовых данных...")
    df = load_and_process_data()
    data_summary = get_data_summary(df)
    
    print(f"✅ Данные загружены. Период: {df['year'].min()} - {df['year'].max()} ({len(df)} лет)")
    print("🤖 Инициализация AI-ассистента...")
    
    # Пытаемся использовать Ollama (локально), если не получается — предлагаем варианты
    try:
        client = LLMClient(provider='ollama', model='llama3.2')
        # Проверяем, доступен ли Ollama
        import requests
        requests.get("http://localhost:11434/api/tags", timeout=2)
        print("✅ Используется локальная модель через Ollama (llama3.2)")
    except:
        print("⚠️ Ollama не доступен. Попробуйте:")
        print("   1. Установить Ollama: https://ollama.ai")
        print("   2. Запустить: ollama pull llama3.2")
        print("   3. Запустить: ollama serve")
        print("\nИли используйте OpenAI (нужен API ключ):")
        api_key = input("Введите OpenAI API ключ (Enter для выхода): ").strip()
        if api_key:
            client = LLMClient(provider='openai', model='gpt-3.5-turbo', api_key=api_key)
            print("✅ Используется OpenAI")
        else:
            print("❌ Не удалось подключить LLM. Выход.")
            sys.exit(1)
    
    print("\n" + "="*50)
    print("💬 Финансовый AI-ассистент готов к работе")
    print("Введите 'exit' для выхода")
    print("="*50 + "\n")
    
    while True:
        question = input("📊 Ваш вопрос: ").strip()
        if question.lower() in ['exit', 'quit', 'выход']:
            print("До свидания!")
            break
        
        if not question:
            continue
        
        print("\n🤔 Анализирую...\n")
        try:
            answer = client.ask(data_summary, question)
            print(f"💡 Ответ: {answer}\n")
        except Exception as e:
            print(f"❌ Ошибка: {e}\n")

if __name__ == "__main__":
    main()