from groq import Groq

API_KEY = "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"

client = Groq(api_key=API_KEY)

messages = []

print("Chatbot ready! (type 'quit' to exit)")
print("-" * 40)

while True:
    user_input = input("You: ")
    
    if user_input.lower() == "quit":
        print("Bye!")
        break
    
    messages.append({"role": "user", "content": user_input})
    
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=messages
    )
    
    reply = response.choices[0].message.content
    messages.append({"role": "assistant", "content": reply})
    
    print(f"Bot: {reply}")
    print()