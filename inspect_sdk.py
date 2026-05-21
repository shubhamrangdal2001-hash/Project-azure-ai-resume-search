import inspect
from azure.ai.projects import AIProjectClient

# Print constructor signature
print("AIProjectClient constructor signature:")
print(inspect.signature(AIProjectClient.__init__))
