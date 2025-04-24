import yaml

def load_prompt(mode):
    with open("prompts/templates.yaml") as f:
        templates = yaml.safe_load(f)
    return templates[mode]["description"]

def analyze_code(code, mode, llm_client):
    prompt = load_prompt(mode)
    review = llm_client.run(prompt, code)
    return review
