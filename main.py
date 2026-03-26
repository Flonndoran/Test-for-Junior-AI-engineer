import sys
import os
from dotenv import load_dotenv
from data_processor import load_and_process_data, get_data_summary
from llm_client import LLMClient

# Настройка кодировок для Windows
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

# Загружаем .env файл
load_dotenv()

def main():
    print("💰 Загрузка финансовых данных...")
    df = load_and_process_data('financial_data.csv')
    data_summary = get_data_summary(df)
    
    print(f"✅ Данные загружены. Период: {df['year'].min()} - {df['year'].max()} ({len(df)} лет)")
    
    print("🤖 Инициализация OpenAI...")
    try:
        client = LLMClient(model='gpt-3.5-turbo')
        print("✅ OpenAI подключен")
    except Exception as e:
        print(f"❌ Ошибка: {e}")
        print("Убедитесь, что в файле .env указан OPENAI_API_KEY")
        sys.exit(1)
    
    print("\n" + "="*50)
    print("💬 Финансовый AI-ассистент (OpenAI)")
    print("Введите 'exit' для выхода")
    print("="*50 + "\n")
    
    while True:
        try:
            question = input("📊 Ваш вопрос: ").strip()
            if question.lower() in ['exit', 'quit', 'выход']:
                print("До свидания!")
                break
            
            if not question:
                continue
            
            print("\n🤔 Анализирую...\n")
            answer = client.ask(data_summary, question)
            
            # Безопасный вывод ответа
            try:
                print(f"💡 Ответ: {answer}\n")
            except UnicodeEncodeError:
                # Если не получается вывести, пробуем другую кодировку
                print(f"💡 Ответ: {answer.encode('utf-8', errors='ignore').decode('utf-8')}\n")
            
        except UnicodeError as e:
            print(f"❌ Ошибка кодировки. Пожалуйста, введите вопрос на русском или английском языке\n")
        except Exception as e:
            print(f"❌ Ошибка: {e}\n")

if __name__ == "__main__":
    main()