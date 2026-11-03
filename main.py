import argparse
import toml
import os
from utils.crawler import crawl
from utils.content_extractor import extract_clean_text
from utils.module_agent import extract_modules
from utils.logger import info

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--urls", nargs="+", required=True)
    args = parser.parse_args()

    config = toml.load("config.toml")
    os.makedirs(config["output"]["output_dir"], exist_ok=True)

    combined_text = ""
    for url in args.urls:
        pages = crawl(url, config["app"]["max_depth"], config["crawler"]["max_pages"])
        for _, soup in pages:
            combined_text += extract_clean_text(soup) + "\n"

    info("Running AI agent for module extraction...")
    result = extract_modules(combined_text, config["llm"]["model"], os.environ.get("OPENAI_API_KEY"))

    output_file = os.path.join(config["output"]["output_dir"], "modules.json")
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(result)

    info(f"Output saved at {output_file}")

if __name__ == "__main__":
    main()
