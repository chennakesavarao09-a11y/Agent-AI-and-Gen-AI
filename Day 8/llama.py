from llama_index.llms.groq import Groq

llm = Groq(
    model="openai/gpt-oss-120b",
    api_key=""
)

print("LlamaIndex AI Chatbot")
print("Type exit to stop")

while True:
    question = input("\nYou: ")

    if question.lower() == "exit":
        print("Chatbot: Goodbye!")
        break

    response = llm.complete(question)

    print("\nChatbot:", response)