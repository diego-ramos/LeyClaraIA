import os
import google.generativeai as genai

api_key = os.environ.get("GOOGLE_API_KEY")
if not api_key:
    print("GOOGLE_API_KEY not set")
    exit(1)

genai.configure(api_key=api_key, transport='rest')

print("Listing available models...")
for m in genai.list_models():
    print(f"Name: {m.name}")
    print(f"Supported methods: {m.supported_generation_methods}")
    print("-" * 20)
