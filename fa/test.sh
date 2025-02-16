# follow https://docs.llamaindex.ai/en/stable/examples/llm/sambanovasystems/ and export the SAMBANOVA_API_KEY
#python main.py
    curl -X POST "http://127.0.0.1:8000/chat" \
      -H "Content-Type: application/json" \
      -d '{"messages": [{"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": "Tell me a joke."}]}'
