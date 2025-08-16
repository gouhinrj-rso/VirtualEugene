import os
from openai import OpenAI

_client = None

def _get_client():
    global _client
    if _client is None:
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise RuntimeError("OPENAI_API_KEY environment variable not set")
        _client = OpenAI(api_key=api_key)
    return _client

def run_agent(prompt: str, model: str = "gpt-4o-mini") -> str:
    """Send a prompt to the OpenAI API and return the response text.

    Parameters
    ----------
    prompt: str
        User instruction or question for the agent.
    model: str, optional
        OpenAI model to use.
    """
    client = _get_client()
    completion = client.responses.create(model=model, input=prompt)
    return completion.output_text
