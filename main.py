import os
import ast

folder_path = "vulnerable-code-snippets/python"
file_extension = ".py"

os.makedirs("log", exist_ok=True)

converted_count = 0 
for root, dirs, files in os.walk(folder_path):
    for file in files:
        if file.endswith(file_extension):
            file_path = os.path.join(root, file)
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    source = f.read()
                    tree = ast.parse(source=source)
                    log_file_path = os.path.join("log", os.path.splitext(file)[0] + ".ast")
                    with open(log_file_path, "w", encoding="utf-8") as log_file:
                        log_file.write(ast.dump(tree, indent=4))
                    converted_count += 1
            except Exception as e:
                print(f"Error processing file: {file_path}")
                print(f"Error message: {str(e)}")

print(f"Number of files converted: {converted_count}")
