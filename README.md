# Shubham.ai — Google-Style AI Resume Search & Chat Agent

A premium, Google-style resume search engine and interactive chat interface powered by **Azure AI Foundry**. The application dynamically references a deployed Azure AI Agent to query candidate details, skills, projects, and contact information.

## 🚀 Live Search Experience
The app replicates a Google Search interface with:
- **AI Overview**: Direct, generated answers from the Azure AI Agent matching search queries.
- **Tabbed Filtering**: Clickable tabs (**All**, **Skills**, **Projects**, **Contact**) that trigger specialized agent queries and filter results.
- **Knowledge Panel**: A structured sidebar summary of the candidate.
- **Interactive Chat Agent**: A persistent chat panel to converse directly with Shubham's resume assistant.

---

## 🛠️ Tech Stack
- **Backend**: Python 3.10+, Azure AI Projects SDK, OpenAI client interface
- **Frontend**: Streamlit (Python) & HTML5/Vanilla CSS/JavaScript (standalone template)
- **AI Engine**: Azure AI Foundry Agent Reference API (`gpt-4.1-mini` or similar)

---

## 📦 Getting Started

### 1. Prerequisites
- Python 3.10 or higher
- An Azure AI Foundry Project with a deployed Agent

### 2. Installation
Clone the repository and install the dependencies:
```bash
git clone https://github.com/yourusername/azure-ai-resume-search.git
cd azure-ai-resume-search
pip install -r requirements.txt
```

### 3. Configuration
Create a `.env` file in the root directory:
```env
# Azure AI Foundry Inference Endpoint Configuration
AZURE_FOUNDRY_ENDPOINT=https://your-foundry-endpoint.services.ai.azure.com/api/projects/proj-default
AZURE_FOUNDRY_API_KEY=your_azure_foundry_api_key

# Agent Reference Configuration
AZURE_FOUNDRY_AGENT_NAME=shubham-resume-agent
AZURE_FOUNDRY_AGENT_VERSION=2
```

### 4. Running the App
Start the Streamlit application:
```bash
streamlit run app.py
```
Open `http://localhost:8501` in your browser.
