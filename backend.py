import os
from dotenv import load_dotenv
import azure.ai.projects
from openai import OpenAI

load_dotenv()

# ── Config ────────────────────────────────────────────────────────────────────
AZURE_ENDPOINT    = os.getenv("AZURE_FOUNDRY_ENDPOINT", "").rstrip("/")
AZURE_API_KEY     = os.getenv("AZURE_FOUNDRY_API_KEY", "")
AGENT_NAME        = os.getenv("AZURE_FOUNDRY_AGENT_NAME", "shubham-resume-agent")
AGENT_VERSION     = os.getenv("AZURE_FOUNDRY_AGENT_VERSION", "2")

# ── Client Initialization ──────────────────────────────────────────────────────
# Initialize the project client globally using OpenAI and the API key
openai_client = None
init_error = None

if AZURE_ENDPOINT and AZURE_API_KEY:
    try:
        base_url = f"{AZURE_ENDPOINT}/openai/v1"
        openai_client = OpenAI(
            base_url=base_url,
            api_key=AZURE_API_KEY,
        )
    except Exception as e:
        init_error = str(e)

# Resume data has been removed from backend. All resume details are served via the Azure AI agent.

# Keep variable names expected by app.py imports
# We keep AZURE_API_KEY as its real value so the OpenAI client can be re-initialized if needed.
AZURE_MODEL = "Agent Managed Model"

# ── Azure AI Foundry ──────────────────────────────────────────────────────────
def call_azure_agent(user_message: str, history: list[dict] | None = None) -> dict:
    """
    Calls Azure AI Foundry agent via the Responses API (agent_reference).
    Returns {"text": str, "error": bool, "source": "azure"}.
    """
    global openai_client, init_error

    if init_error:
        # Try to initialize again in case variables or tokens were updated
        try:
            base_url = f"{AZURE_ENDPOINT}/openai/v1"
            openai_client = OpenAI(
                base_url=base_url,
                api_key=AZURE_API_KEY,
            )
            init_error = None
        except Exception as e:
            return {
                "text": f"Azure Project Client initialization failed: {init_error or e}",
                "error": True,
                "source": "azure",
            }

    if not openai_client:
        try:
            base_url = f"{AZURE_ENDPOINT}/openai/v1"
            openai_client = OpenAI(
                base_url=base_url,
                api_key=AZURE_API_KEY,
            )
        except Exception as e:
            return {
                "text": f"Azure client not initialized: {e}",
                "error": True,
                "source": "azure",
            }

    try:
        # Build input message sequence. 
        input_messages = []
        if history:
            for msg in history:
                role = msg.get("role", "user")
                # Map standard roles if needed
                if role == "bot":
                    role = "assistant"
                # Support both key names: 'content' and 'text'
                content = msg.get("content") or msg.get("text") or ""
                input_messages.append({"role": role, "content": content})
        
        input_messages.append({"role": "user", "content": user_message})

        # Reference the agent using responses.create
        response = openai_client.responses.create(
            input=input_messages,
            extra_body={
                "agent_reference": {
                    "name": AGENT_NAME,
                    "version": AGENT_VERSION,
                    "type": "agent_reference"
                }
            },
        )

        text = response.output_text or "No response from agent."
        return {"text": text, "error": False, "source": "azure"}

    except Exception as e:
        return {"text": f"Error calling Azure Agent SDK: {e}", "error": True, "source": "azure"}


# ── Groq fallback (Disabled as per user request: "All answer must be in 'shubham-resume-agent' only") ──
def call_groq(user_message: str, history: list[dict] | None = None) -> dict:
    return {
        "text": "Fallback disabled. All answers must be serviced by the Azure AI Agent.",
        "error": True,
        "source": "groq"
    }


# ── Search results builder ────────────────────────────────────────────────────
def build_search_results(query: str) -> list[dict]:
    # Search snippet should be generated/informed by the agent or direct to the site.
    q = query.lower()
    results = [
        {
            "favicon": "L",
            "url": "www.linkedin.com/in/shubham-rangdal-685504203",
            "title": "Shubham Rangdal — AI/ML Engineer & Data Scientist",
            "snippet": (
                "Official LinkedIn profile of <b>Shubham Rangdal</b>. Connect to view "
                "professional experience, projects, achievements, and contact details."
            ),
            "ai_generated": True,
        },
        {
            "favicon": "E",
            "url": "mailto:shubhamrangdal2000@gmail.com",
            "title": "Contact Shubham Rangdal — Email & Phone",
            "snippet": (
                "Get in touch with <b>Shubham Rangdal</b>. Email: shubhamrangdal2000@gmail.com | "
                "Phone: 9730208424. Available for AI & Software Engineer roles."
            ),
            "ai_generated": False,
        }
    ]
    return results
