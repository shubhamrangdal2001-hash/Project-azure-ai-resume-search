from azure.identity import AzureCliCredential
from azure.ai.projects import AIProjectClient

endpoint = "https://project1-resumeinhtml.services.ai.azure.com/api/projects/proj-default"

try:
    project_client = AIProjectClient(
        endpoint=endpoint,
        credential=AzureCliCredential(),
    )
    print("Project client created.")
    
    try:
        agent = project_client.agents.get("shubham-resume-agent")
        print(f"Agent found! Name: {agent.name}, ID/Details: {agent}")
    except Exception as e:
        print(f"Error getting agent: {e}")
        
    try:
        version = project_client.agents.get_version("shubham-resume-agent", "2")
        print(f"Version 2 found! Details: {version}")
    except Exception as e:
        print(f"Error getting version 2: {e}")

    try:
        version = project_client.agents.get_version("shubham-resume-agent", "1")
        print(f"Version 1 found! Details: {version}")
    except Exception as e:
        print(f"Error getting version 1: {e}")
except Exception as e:
    print(f"Outer error: {e}")
