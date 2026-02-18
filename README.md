# infosci-spark-client

    A simple Python client for the Information Science Department Spark API.

## Installation

```bash
pip install git+https://github.com/mrpeterss/infosci-spark-client.git
```

## Quick Start

```python
from infosci_spark_client import LLMClient

# Initialize with your API key
client = LLMClient(api_key="your-api-key")

# Non-streaming chat
response = client.chat([
    {"role": "user", "content": "What is the best seafood?"}
])
print(response["content"])

# Streaming chat
for chunk in client.chat([
    {"role": "user", "content": "What is the best seafood?"}
], stream=True):
    print(chunk["content"], end="", flush=True)
```

## Features

- Simple and intuitive API
- Support for streaming and non-streaming responses
- Optional reasoning/thinking display
- Configurable reasoning levels
- Full type hints for better IDE support

## API Reference

### LLMClient

#### `__init__(api_key: str, base_url: str = "https://4300spark.infosci.cornell.edu")`

Initialize the LLM client.

**Parameters:**
- `api_key` (str): Your API key for authentication
- `base_url` (str): Base URL for the API (default: https://4300spark.infosci.cornell.edu)

#### `chat(messages: List[Dict[str, str]], stream: bool = False, show_thinking: bool = False, reasoning_level: Optional[str] = None)`

Send a chat request to the API.

**Parameters:**
- `messages` (List[Dict[str, str]]): List of message dictionaries with 'role' and 'content' keys
- `stream` (bool): Whether to stream the response (default: False)
- `show_thinking` (bool): Whether to include the model's reasoning process (default: False)
- `reasoning_level` (Optional[str]): Reasoning level - "low", "medium", or "high" (default: None)

**Returns:**
- If `stream=False`: Dict with 'content' and 'reasoning' keys
- If `stream=True`: Generator that yields dicts with 'content' and 'reasoning' keys

**Example:**

```python
# Non-streaming with reasoning
response = client.chat(
    messages=[{"role": "user", "content": "Explain quantum computing"}],
    show_thinking=True,
    reasoning_level="high"
)
print("Content:", response["content"])
print("Reasoning:", response["reasoning"])

# Streaming
for chunk in client.chat(
    messages=[{"role": "user", "content": "Tell me a story"}],
    stream=True
):
    print(chunk["content"], end="", flush=True)
```

## Requirements

- Python 3.7+
- requests >= 2.25.0

## License

MIT License

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Issues

If you encounter any issues, please report them on the [GitHub Issues page](https://github.com/mrpeterss/infosci-spark-client/issues).
