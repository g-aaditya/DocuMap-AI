# DocuMap AI

**DocuMap AI** is an AI-powered documentation analysis tool that crawls help-center and documentation websites, extracts useful page content, and uses a Large Language Model (LLM) to identify product modules and submodules.

It provides two ways to run the workflow:
- A **Streamlit web interface** for entering documentation URLs and viewing the extraction result.
- A **command-line interface (CLI)** for running extraction and saving the result as JSON.

> **Project status:** Prototype / work in progress. The current implementation provides basic crawling, text extraction, and LLM-based module discovery. Review the limitations and security notes before using it on untrusted or production websites.

---

## Features

- **Documentation crawling:** Follows links from one or more starting URLs using a depth-first traversal.
- **Crawl limits:** Supports a maximum crawl depth and maximum page count through `config.toml`.
- **HTML content extraction:** Extracts headings, paragraphs, and list items while removing common page elements such as navigation, headers, footers, scripts, and styles.
- **AI-powered module discovery:** Uses the OpenAI API to infer product modules and their submodules from extracted documentation.
- **Streamlit interface:** Enter multiple URLs and view the generated result in a browser.
- **CLI support:** Run extraction from a terminal and save the model response to `output/modules.json`.
- **Configurable model:** Select the OpenAI model in `config.toml`.

## How it works

1. Provide one or more documentation or help-center URLs.
2. The crawler visits the starting pages and follows eligible links within its current domain-matching rule.
3. The content extractor removes common page-layout elements and collects headings, paragraphs, and list items.
4. The extracted text is sent to the configured OpenAI model.
5. The model is prompted to identify modules and submodules and return JSON.
6. The Streamlit interface displays the response, or the CLI writes it to `output/modules.json`.

## Technology stack

| Technology | Purpose |
|---|---|
| Python | Core application |
| Requests | Fetch web pages |
| Beautiful Soup 4 | Parse HTML and extract content |
| tldextract | Determine the registered domain used by the crawler |
| OpenAI Python SDK | Connect to the language model |
| Streamlit | Web interface |
| TOML | Application configuration |
| Rich | Console logging |

---

## Project structure

```text
documap-ai/
├── utils/
│   ├── __init__.py
│   ├── content_extractor.py
│   ├── crawler.py
│   ├── logger.py
│   └── module_agent.py
├── output/
├── config.toml
├── main.py
├── requirements.txt
├── streamlit_app.py
└── README.md
```

`output/` is created automatically when the CLI runs if it does not already exist.

## Requirements

- Python 3.9 or newer
- An OpenAI API key
- Internet access to reach the documentation websites and OpenAI API

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/<your-username>/documap-ai.git
cd documap-ai
```

Replace `<your-username>` with your GitHub username.

### 2. Create and activate a virtual environment

**macOS / Linux**

```bash
python3 -m venv .venv
source .venv/bin/activate
```

**Windows (PowerShell)**

```powershell
py -m venv .venv
.venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Configure your OpenAI API key

Set the key as an environment variable. This avoids hardcoding credentials in the source code.

**macOS / Linux**

```bash
export OPENAI_API_KEY="your-openai-api-key"
```

**Windows (PowerShell)**

```powershell
$env:OPENAI_API_KEY="your-openai-api-key"
```

Keep your API key private. Never commit it to GitHub or include it in screenshots, logs, or issue reports.

---

## Configuration

The application reads settings from `config.toml`.

```toml
[app]
max_depth = 2
timeout = 10
user_agent = "PulseModuleExtractor/1.0"

[llm]
provider = "openai"
model = "gpt-4o-mini"
temperature = 0.2

[output]
format = "json"
output_dir = "output"

[crawler]
allowed_domains_only = true
max_pages = 50
```

| Setting | Description | Default |
|---|---|---:|
| `app.max_depth` | Maximum link depth from each starting URL | `2` |
| `app.timeout` | Intended HTTP request timeout setting | `10` |
| `app.user_agent` | Intended crawler user-agent value | `PulseModuleExtractor/1.0` |
| `llm.provider` | Configured LLM provider label | `openai` |
| `llm.model` | OpenAI model name | `gpt-4o-mini` |
| `llm.temperature` | Intended model temperature | `0.2` |
| `output.format` | Intended output format | `json` |
| `output.output_dir` | Directory used for CLI output | `output` |
| `crawler.allowed_domains_only` | Intended same-domain crawling control | `true` |
| `crawler.max_pages` | Maximum number of pages crawled per starting URL | `50` |

**Implementation note:** In the current code, the crawler hardcodes the request timeout and does not apply the configured user-agent or `allowed_domains_only` setting. The model temperature is also hardcoded in `utils/module_agent.py`. The table distinguishes intended configuration from settings currently applied by the implementation.

---

## Run the application

### Option 1: Streamlit web interface

Start the application:

```bash
streamlit run streamlit_app.py
```

Open the local address printed in the terminal (normally `http://localhost:8501`).

1. Enter one or more documentation URLs, one URL per line.
2. Enter your OpenAI API key in the password field, or set `OPENAI_API_KEY` in your environment.
3. Select **Extract Modules**.
4. Review the generated response in the Streamlit interface.

The current Streamlit interface displays the result; JSON file saving is currently implemented in the CLI workflow.

### Option 2: Command-line interface

Run the CLI with one or more starting URLs:

```bash
python main.py --urls https://example.com/docs
```

Multiple URLs can be supplied:

```bash
python main.py --urls https://docs.example.com https://support.example.org
```

The CLI writes the model response to:

```text
output/modules.json
```

The current CLI expects `OPENAI_API_KEY` to be available as an environment variable.

---

## Expected output

The LLM is prompted to return a JSON representation of modules and submodules. A typical target structure looks like this:

```json
[
  {
    "module": "User Management",
    "Description": "Features for managing users and their account access.",
    "Submodules": {
      "User Registration": "Allows new users to create an account.",
      "Role Management": "Allows administrators to assign and manage user roles."
    }
  },
  {
    "module": "Billing",
    "Description": "Features related to subscriptions and payments.",
    "Submodules": {
      "Subscription Management": "Allows users to view and manage subscriptions.",
      "Payment Methods": "Supports managing payment methods."
    }
  }
]
```

This is an **illustrative example of the intended output shape**, not a guaranteed result. The current implementation prompts the model to return JSON but does not enforce a JSON schema or validate the response before displaying or saving it.

---

## Current limitations

The following limitations are important when evaluating the current prototype:

- **Static HTML focus:** Pages that render their main content with client-side JavaScript may not expose all their content to the crawler.
- **Flattened content:** Extracted text is combined into one string. Original page hierarchy and source-page relationships are not preserved in the LLM input.
- **No guaranteed structured response:** The model is asked to return JSON, but the response is not validated against a schema.
- **Basic crawler controls:** The crawler uses a simple domain check and does not currently apply all crawler settings from `config.toml`.
- **No retry or caching layer:** Failed requests and repeated crawls are not managed through a robust retry or cache system.
- **No automated test suite:** The repository does not currently include automated tests.
- **Streamlit export:** The current UI displays the response but does not provide a dedicated JSON download workflow.

## Security and responsible use

This project fetches web pages and sends extracted text to an external LLM provider. Use it responsibly.

- Only crawl websites you own or have permission to access.
- Respect website terms, rate limits, and applicable crawling policies.
- Do not use the tool to access private, authenticated, or restricted documentation without authorization.
- Treat crawled page content as untrusted input.
- Do not expose API keys or other secrets in source control.
- Before using this crawler with arbitrary URLs or in a hosted environment, add protections against server-side request forgery (SSRF), including blocking localhost, private, link-local, and other non-public IP ranges. Re-check destinations after DNS resolution and redirects.
- Add stricter URL and hostname validation, request limits, and safer redirect handling before accepting untrusted URLs.

## Roadmap

Potential next improvements:

- Enforce structured JSON output and validate it against a defined schema.
- Preserve page URLs and heading hierarchy throughout extraction.
- Improve hostname and subdomain validation.
- Add SSRF protections and redirect validation.
- Apply all settings from `config.toml` consistently.
- Add retry handling, request throttling, and crawl caching.
- Add progress reporting and a JSON download button to Streamlit.
- Add automated tests for crawling, extraction, and LLM response handling.
- Add Docker support and a REST API.

## Contributing

Contributions and suggestions are welcome.

1. Fork the repository.
2. Create a feature branch: `git checkout -b feature/your-feature`.
3. Commit your changes: `git commit -m "Add your feature"`.
4. Push the branch: `git push origin feature/your-feature`.
5. Open a pull request describing the change.

For substantial changes, consider opening an issue first to discuss the proposed implementation.

## License

No license file is currently included with this project. Add a `LICENSE` file and update this section before distributing the repository. If you intend to use the MIT License, include the standard MIT license text and your copyright details.
