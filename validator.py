# To run this code you need to install the following dependencies:
# pip install google-genai

from google import genai
from google.genai import types
import csv

# Get all tokens from tokens.txt
def get_tokens(file_path):
    tokens = []
    with open(file_path, 'r') as f:
        for line in f:
            line = line.strip()
            if line:  # Skip blank lines
                tokens.append(line)
    return tokens

def generate(token):
    client = genai.Client(
        api_key=token,
    )

    model = "gemini-2.5-flash"
    contents = [
        types.Content(
            role="user",
            parts=[
                types.Part.from_text(text="""Respond hi to me. Don't say anything else."""),
            ],
        ),
    ]
    generate_content_config = types.GenerateContentConfig(
        thinking_config = types.ThinkingConfig(
            thinking_budget=0,
        ),
    )
    response_text = ""
    err = ""
    try:
        response = client.models.generate_content(
            model=model,
            contents=contents,
            config=generate_content_config,
        )
        response_text = response.text
    except Exception as e:
        err = str(e).replace("\n", "\\n")
        print(f"  Error: {err}", "-" * 20, sep="\n")
    return response_text, err

output_list = []
current_line = ""
tokens = get_tokens('tokens.txt')
for token in tokens:
    print(f"Testing token: {token}")
    response_text, err = generate(token)
    # keep the first and last 4 digits of the token
    token = token[:4] + "..." + token[-4:]
    if err == "":
        output_list.append([token, "pass"])
    else:
        output_list.append([token, err])

# save output to output.csv
with open('output.csv', 'w+', newline='') as f:
    writer = csv.writer(f)
    writer.writerows(output_list)
    print(f"Testing completed. Results saved to output.csv")