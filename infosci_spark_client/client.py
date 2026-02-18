"""
LLM Client for Information Science Department Spark API
"""

import json
import requests
from typing import List, Dict, Optional, Generator, Union


class LLMClient:
    """
    A client for interacting with the Information Science Department Spark API.
    
    Example usage:
        # Initialize with your API key
        client = LLMClient(api_key="your-api-key")
        
        # Non-streaming chat
        response = client.chat([
            {"role": "user", "content": "What is the best seafood?"}
        ])
        print(response)
        
        # Streaming chat
        for chunk in client.chat([
            {"role": "user", "content": "What is the best seafood?"}
        ], stream=True):
            print(chunk, end="", flush=True)
    """
    
    def __init__(self, api_key: str, base_url: str = "https://4300spark.infosci.cornell.edu"):
        """
        Initialize the LLM client.
        
        Args:
            api_key: Your API key for authentication
            base_url: Base URL for the API (default: https://4300spark.infosci.cornell.edu)
        """
        self.api_key = api_key
        self.base_url = base_url.rstrip("/")
        self.chat_endpoint = f"{self.base_url}/api/chat"
    
    def chat(
        self,
        messages: List[Dict[str, str]],
        stream: bool = False,
        show_thinking: bool = False,
        reasoning_level: Optional[str] = None
    ) -> Union[Dict, Generator[Dict, None, None]]:
        """
        Send a chat request to the API.
        
        Args:
            messages: List of message dictionaries with 'role' and 'content' keys
                     Example: [{"role": "user", "content": "Hello!"}]
            stream: Whether to stream the response (default: False)
            show_thinking: Whether to include the model's reasoning process (default: False)
                          If False, reasoning field will be empty
            reasoning_level: Optional reasoning level - "low", "medium", or "high" (default: None, uses API default)
            
        Returns:
            If stream=False: Dict with 'content' and 'reasoning' keys
            If stream=True: Generator that yields dicts with 'content' and 'reasoning' keys
            
            The 'reasoning' field will be empty string if show_thinking=False
            
        Raises:
            requests.RequestException: If the API request fails
            ValueError: If reasoning_level is not "low", "medium", "high", or None
        """
        # Validate reasoning_level
        valid_levels = {"low", "medium", "high", None}
        if reasoning_level not in valid_levels:
            raise ValueError(f"reasoning_level must be one of: 'low', 'medium', 'high', or None. Got: {reasoning_level}")
        
        payload = {
            "messages": messages,
            "stream": stream
        }
        
        # Add reasoning_level if specified
        if reasoning_level is not None:
            payload["reasoning_level"] = reasoning_level
                
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        if stream:
            return self._stream_chat(payload, headers, show_thinking)
        else:
            return self._non_stream_chat(payload, headers, show_thinking)
    
    def _non_stream_chat(self, payload: dict, headers: dict, show_thinking: bool = False) -> Dict:
        """
        Handle non-streaming chat requests.
        
        Args:
            payload: Request payload
            headers: Request headers
            show_thinking: If True, include reasoning; if False, reasoning will be empty
            
        Returns:
            Dict with 'content' and 'reasoning' keys
        """
        response = requests.post(
            self.chat_endpoint,
            json=payload,
            headers=headers
        )
        response.raise_for_status()
        
        # Parse OpenAI-compatible response format
        data = response.json()
        
        # Extract content from choices array
        if "choices" in data and len(data["choices"]) > 0:
            choice = data["choices"][0]
            message = choice.get("message", {})
            content = message.get("content", "")
            reasoning = message.get("reasoning_content", "") if show_thinking else ""
            
            return {
                "content": content,
                "reasoning": reasoning
            }
        
        # Fallback for unexpected format
        return {"content": str(data), "reasoning": ""}
    
    def _stream_chat(
        self, 
        payload: dict, 
        headers: dict, 
        show_thinking: bool = False
    ) -> Generator[Dict, None, None]:
        """
        Handle streaming chat requests.
        
        Args:
            payload: Request payload
            headers: Request headers
            show_thinking: If True, include reasoning in chunks; if False, reasoning will be empty
            
        Yields:
            Dicts with 'content' and 'reasoning' keys
        """
        response = requests.post(
            self.chat_endpoint,
            json=payload,
            headers=headers,
            stream=True
        )
        response.raise_for_status()
        
        # Process the streaming response (Server-Sent Events format)
        for line in response.iter_lines():
            if not line:
                continue
            
            line_str = line.decode('utf-8')
            
            # Skip SSE comments and empty lines
            if line_str.startswith(':') or not line_str.strip():
                continue
            
            # Remove "data: " prefix if present
            if line_str.startswith('data: '):
                line_str = line_str[6:]
            
            # Check for stream end marker
            if line_str.strip() == '[DONE]':
                break
                
            try:
                data = json.loads(line_str)
                
                # Extract delta content from OpenAI-compatible streaming format
                if "choices" in data and len(data["choices"]) > 0:
                    choice = data["choices"][0]
                    delta = choice.get("delta", {})
                    
                    # Get content and reasoning
                    content = delta.get("content", "")
                    reasoning = delta.get("reasoning_content", "") if show_thinking else ""
                    
                    # Always yield structured data
                    yield {
                        "content": content,
                        "reasoning": reasoning
                    }
                    
                    # Check if we're done
                    if choice.get("finish_reason"):
                        break
                    
            except json.JSONDecodeError:
                # Skip lines that aren't valid JSON
                continue
            except Exception as e:
                # Handle other errors gracefully
                continue
