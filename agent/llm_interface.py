import requests
import openai
import yaml

class LLMClient:
    def __init__(self, provider, model, config):
        self.provider = provider
        self.model = model
        self.config = config
        if provider == "openai":
            openai.api_key = config["openai"]["api_key"]

    def run(self, prompt, code_snippet):
        full_prompt = f"{prompt}\n\n```python\n{code_snippet}\n```"
        if self.provider == "openai":
            return self._call_openai(full_prompt)
        elif self.provider == "ollama":
            return self._call_ollama(full_prompt)
        elif self.provider == "anthropic":
            return self._call_claude(full_prompt)

    def _call_openai(self, prompt):
        response = openai.ChatCompletion.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content

    def _call_ollama(self, prompt):
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={"model": self.model, "prompt": prompt}
        )
        return response.json()["response"]

    def _call_claude(self, prompt):
        headers = {
            "x-api-key": self.config["anthropic"]["api_key"],
            "content-type": "application/json"
        }
        data = {
            "model": self.model,
            "prompt": prompt,
            "max_tokens_to_sample": 1024
        }
        response = requests.post("https://api.anthropic.com/v1/complete", headers=headers, json=data)
        return response.json()["completion"]
