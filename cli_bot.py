"""
Command Line Interface for the Conversational Knowledge Bot
"""
from dotenv import load_dotenv
from bot_core import DeepSeekBot

load_dotenv()


def main():
    """Main CLI function"""
    print("=" * 70)
    print("🤖  KNOWLEDGE BOT - COMMAND LINE VERSION")
    print("=" * 70)
    print("\n📝 Commands:")
    print("  • Type your question and press Enter")
    print("  • 'search: <query>' - Web search")
    print("  • 'wiki: <query>' - Wikipedia lookup")
    print("  • 'clear' - Clear conversation memory")
    print("  • 'exit' or 'quit' - Exit program")
    print("\n" + "-" * 70 + "\n")
    
    bot = DeepSeekBot()
    
    while True:
        try:
            user_input = input("👤 You: ").strip()
            
            # Exit commands
            if user_input.lower() in ['exit', 'quit', 'bye']:
                print("\n🤖 Bot: Goodbye! Thanks for chatting!")
                break
            
            # Clear memory command
            if user_input.lower() == 'clear':
                bot.clear_memory()
                print("✅ Memory cleared\n")
                continue
            
            # Empty input
            if not user_input:
                continue
            
            print("🤖 Bot: ", end="", flush=True)
            
            # Process different command types
            if user_input.lower().startswith("search:"):
                search_query = user_input[7:].strip()
                print(f"\n📝 Searching for: {search_query}\n")
                response = bot.search_web(search_query)
            
            elif user_input.lower().startswith("wiki:"):
                wiki_query = user_input[5:].strip()
                print(f"\n📝 Looking up Wikipedia: {wiki_query}\n")
                response = bot.get_wikipedia(wiki_query)
            
            else:
                # Regular chat
                response = bot.chat(user_input)
            
            print(response)
            print()
            
        except KeyboardInterrupt:
            print("\n\n👋 Interrupted. Goodbye!")
            break
        except Exception as e:
            print(f"\n❌ Error: {e}\n")


if __name__ == "__main__":
    main()
