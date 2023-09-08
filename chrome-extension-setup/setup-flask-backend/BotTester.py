from GPTconvo import GPT3Chatbot  # Import the appropriate chatbot class


def main():
    # Replace with your API key
    api_key = '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'

    # Create an instance of the chatbot
    bot = GPT3Chatbot(api_key)

    # Set an initial prompt if needed (uncomment and modify as necessary)
    # bot.set_initial_prompt("Your initial prompt goes here.")

    print("BotTester: Chat with the bot. Type 'exit' to quit.")

    while True:
        user_input = input("User: ")
        if user_input.strip().lower() == "exit":
            break
        response = bot.chat(user_input)
        print("Bot:", response)


if __name__ == "__main__":
    main()
