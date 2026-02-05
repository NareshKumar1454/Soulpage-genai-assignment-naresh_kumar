"""
Command Line Interface for the Conversational Knowledge Bot
100% FREE - DeepSeek via OpenRouter
"""
import os
import sys
from bot_core import DeepSeekBot
from dotenv import load_dotenv

load_dotenv()


def main():
    """Main CLI function"""
    print("=" * 70)
    print("🤖 DEEPSEEK KNOWLEDGE BOT - COMMAND LINE VERSION")
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
    print("-"*60)
    
    mode = input("\nSelect mode (1/2/3): ").strip()
    
    if mode == "3":
        model = input("Model [deepseek/deepseek-chat]: ").strip() or "deepseek/deepseek-chat"
        temp = input("Temperature [0.7]: ").strip()
        temperature = float(temp) if temp else 0.7
        use_agent = input("Use agent? (y/n): ").strip().lower() == 'y'
    elif mode == "2":
        model = "deepseek/deepseek-chat"
        temperature = 0.7
        use_agent = False
    else:  # Default to agent mode
        model = "deepseek/deepseek-chat"
        temperature = 0.7
        use_agent = True
    
    # Initialize bot
    print(f"\n🚀 Initializing {'Agent' if use_agent else 'Simple'} mode...")
    
    try:
        if use_agent:
            bot = ConversationalKnowledgeBot(
                model_name=model,
                temperature=temperature
            )
            print("✅ Smart Agent initialized with tools!")
        else:
            bot = create_simple_bot()
            print("✅ Simple chat bot initialized!")
    except Exception as e:
        print(f"❌ Failed to initialize bot: {e}")
        return
    
    print("\n" + "="*60)
    print("💬 CHAT COMMANDS:")
    print("- Type your message to chat")
    print("- 'clear' - Clear conversation")
    print("- 'history' - Show conversation history")
    print("- 'mode' - Switch between simple/agent mode")
    print("- 'quit' or 'exit' - End session")
    print("="*60)
    print("\nDeepSeek is ready! Start chatting...\n")
    
    message_count = 0
    
    while True:
        try:
            # Get user input
            user_input = input("\n👤 You: ").strip()
            
            # Check commands
            if user_input.lower() in ['quit', 'exit', 'q', 'bye']:
                print("\n🤖 Bot: Goodbye! Thanks for chatting with DeepSeek! 👋")
                break
            
            elif user_input.lower() == 'clear':
                if hasattr(bot, 'memory'):
                    bot.memory.clear()
                print("✅ Conversation cleared!")
                continue
            
            elif user_input.lower() == 'history':
                if hasattr(bot, 'memory'):
                    history = bot._get_chat_history()
                    print("\n📜 Conversation History:")
                    print(history)
                else:
                    print("ℹ️ History not available in simple mode")
                continue
            
            elif user_input.lower() == 'mode':
                print("Switching modes requires restart. Please restart the bot.")
                continue
            
            elif not user_input:
                continue
            
            # Process message
            message_count += 1
            print(f"\n🤖 Bot: ", end="")
            
            # Get response
            if use_agent:
                response = bot.chat(user_input)
            else:
                response = bot.run(user_input)
            
            print(response)
            
            # Show stats every 5 messages
            if message_count % 5 == 0:
                print(f"\n📊 Stats: {message_count} messages exchanged")
        
        except KeyboardInterrupt:
            print("\n\n🤖 Bot: Goodbye! 👋")
            break
        except Exception as e:
            print(f"\n❌ Error: {str(e)[:100]}")

if __name__ == "__main__":
    main()