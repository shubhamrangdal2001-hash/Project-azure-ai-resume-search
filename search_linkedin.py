import json

log_path = r"C:\Users\shubh\.gemini\antigravity\brain\6d6cef44-0fed-4d54-b753-e4a00de1d9e8\.system_generated\logs\transcript.jsonl"
with open(log_path, "r", encoding="utf-8") as f:
    for idx, line in enumerate(f):
        if "linkedin" in line.lower():
            try:
                step = json.loads(line)
                print(f"Match at line {idx} | Step {step.get('step_index')}: Source={step.get('source')}, Type={step.get('type')}")
                if "content" in step and step["content"]:
                    print(f"  Content: {step['content'][:300]}")
            except Exception as e:
                print(f"Error parsing line {idx}: {e}")
