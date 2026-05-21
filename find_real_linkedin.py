import os

path = r"d:\shubham_resume"
for root, dirs, files in os.walk(path):
    for file in files:
        if file.endswith((".py", ".html", ".env", ".txt")):
            file_path = os.path.join(root, file)
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    for line_num, line in enumerate(f, 1):
                        if "linkedin" in line.lower() and "linkedin.com/in/shubham" not in line.lower():
                            print(f"{file}:{line_num}: {line.strip()}")
            except Exception as e:
                pass
