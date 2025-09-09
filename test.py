# from groq import Groq

# # Ganti dengan API key kamu
# client = Groq(api_key="")

# chat_completion = client.chat.completions.create(
#     messages=[
#         {
#             "role": "user", 
#             "content": "ibu kota baru Indonesia"
#         }
#     ],
#     model="openai/gpt-oss-20b",
#     temperature=1,
#     max_completion_tokens=2048,
#     top_p=1,
#     stream=False,
#     stop=None,
#     tool_choice="required",  # Force to use the tool
#     tools=[
#         {
#             "type": "browser_search"  # Groq will use internal search
#         }
#     ]
# )

# print(chat_completion.choices[0].message.content)


from groq import Groq
import json

client = Groq(api_key="")

response = client.chat.completions.create(
    model="compound-beta",
    messages=[
        {
            "role": "user",
            "content": "Apa ibu kota baru Indonesia?"
        }
    ]
)

# Final output
print(json.dumps(response.choices[0].message.content, indent=2))

# Reasoning + internal tool calls
print(json.dumps(response.choices[0].message.reasoning, indent=2))

# Search results from the tool calls
if response.choices[0].message.executed_tools:
    print(json.dumps(response.choices[0].message.executed_tools[0].search_results, indent=2))
