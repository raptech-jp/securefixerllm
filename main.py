import os
import ast
import json
from openai import OpenAI
# from dotenv import load_dotenv

folder_path = "vulnerable-code-snippets/python"
file_extension = ".py"

os.makedirs("log", exist_ok=True)
os.makedirs("fixed", exist_ok=True)

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
client = OpenAI()

def remove_python_code_markers(text):
    if text.startswith("```python") and text.endswith("```"):
        return text[len("```python"): -len("```")]
    else:
        return text


def gpt_repair(ast_tree_file):
    with open(ast_tree_file, "r", encoding="utf-8") as f:
        ast_tree = f.read()

    response = client.chat.completions.create(
        model="gpt-4-turbo",
        messages=[
            {"role": "system", "content": "抽象構文木から、極力機能を維持したままソースコードの脆弱性を修正し、それを返してください。返すのは抽象構文木ではなく、修正されたソースコードのみです。説明文は不要です。"},
            {"role": "user", "content": ast_tree}
        ]
    )
    responseCode = response.choices[0].message.content
    fixedCode = remove_python_code_markers(responseCode)
    # fixed_object = json.loads(responseCode)
    # dumped_object = json.dumps(fixed_object["fixedSource"], indent=2)
    fixed_file_path = os.path.join("fixed", os.path.splitext(
        os.path.basename(ast_tree_file))[0] + file_extension)
    with open(fixed_file_path, "w", encoding="utf-8") as fixed_file:
        fixed_file.write(fixedCode)
    print(fixedCode)


def main():
    converted_count = 0
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file.endswith(file_extension):
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, "r", encoding="utf-8") as f:
                        source = f.read()
                        tree = ast.parse(source=source)
                        log_file_path = os.path.join(
                            "log", os.path.splitext(file)[0] + ".ast")
                        with open(log_file_path, "w", encoding="utf-8") as log_file:
                            log_file.write(ast.dump(tree, indent=4))
                        converted_count += 1
                        gpt_repair(log_file_path)
                except Exception as e:
                    print(f"Error processing file: {file_path}")
                    print(f"Error message: {str(e)}")
    print(f"Number of files converted: {converted_count}")


if __name__ == "__main__":
    main()
