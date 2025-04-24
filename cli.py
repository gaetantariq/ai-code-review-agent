import argparse
import yaml
from agent.analyzer import analyze_code
from agent.llm_interface import LLMClient

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--file', type=str, required=True)
    parser.add_argument('--mode', type=str, default='strict')
    parser.add_argument('--provider', type=str, default=None)
    args = parser.parse_args()

    with open("config.yaml") as f:
        config = yaml.safe_load(f)

    provider = args.provider or config.get("default_provider")
    model = config[provider]["model"]
    client = LLMClient(provider, model, config)

    with open(args.file) as f:
        code = f.read()

    review = analyze_code(code, args.mode, client)

    with open("reviews/review_output.md", "w") as f:
        f.write(review)

    print("✅ Review saved to reviews/review_output.md")

if __name__ == "__main__":
    main()
