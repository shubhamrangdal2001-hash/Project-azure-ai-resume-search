from azure.identity import AzureCliCredential
from azure.ai.projects import AIProjectClient

endpoint = "https://project1-resumeinhtml.services.ai.azure.com/api/projects/proj-default"

try:
    project_client = AIProjectClient(
        endpoint=endpoint,
        credential=AzureCliCredential(),
    )
    print("Project client created.")
    
    # List agents
    agents = project_client.agents.list()
    print("Agents list:")
    for agent in agents:
        print(f"Name: {agent.name}, ID: {agent.id}, Description: {agent.description}")
except Exception as e:
    print(f"Error listing agents: {e}")
