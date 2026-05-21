import os

from azure.ai.projects import AIProjectClient
from azure.core.credentials import AzureKeyCredential
from dotenv import load_dotenv

load_dotenv()

endpoint = os.getenv("AZURE_FOUNDRY_ENDPOINT", "").rstrip("/")
api_key = os.getenv("AZURE_FOUNDRY_API_KEY", "")

if not endpoint or not api_key:
    raise SystemExit("Set AZURE_FOUNDRY_ENDPOINT and AZURE_FOUNDRY_API_KEY in .env")

try:
    project_client = AIProjectClient(
        endpoint=endpoint,
        credential=AzureKeyCredential(api_key),
    )
    print("Success initializing with AzureKeyCredential!")

    my_agent = os.getenv("AZURE_FOUNDRY_AGENT_NAME", "shubham-resume-agent")
    my_version = os.getenv("AZURE_FOUNDRY_AGENT_VERSION", "2")

    openai_client = project_client.get_openai_client()

    response = openai_client.responses.create(
        input=[{"role": "user", "content": "Tell me what you can help with."}],
        extra_body={"agent_reference": {"name": my_agent, "version": my_version, "type": "agent_reference"}},
    )
    print(f"Response: {response.output_text}")
except Exception as e:
    print(f"Error: {e}")
