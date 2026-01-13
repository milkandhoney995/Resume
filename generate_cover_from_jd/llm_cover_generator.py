import json
import re
from openai import OpenAI

client = OpenAI()

SYSTEM_PROMPT = """
You are a professional career consultant.
Write concise, high-quality English cover letters for global tech companies.
"""

USER_PROMPT = """
Generate a cover letter in valid YAML format:

cover:
  company:
  position:
  opening:
  why_me:
  experience:
    - ...
    - ...
  closing:

Rules:
- Professional and concise
- Frontend-focused
- No generic filler text

IMPORTANT:
- Output ONLY valid YAML
- Do NOT include explanations
- Do NOT include ``` or ```yaml
- The output MUST start with "cover:"

Input:
{input_json}
"""

# YAML抽出用関数
def extract_yaml(text: str) -> str:
    """
    LLM出力から YAML 本体だけを安全に抽出する
    """
    # ```yaml ``` を除去
    text = re.sub(r"```yaml|```", "", text, flags=re.IGNORECASE).strip()

    # cover: 以降だけを切り出す
    match = re.search(r"(cover:\s[\s\S]+)", text)
    if not match:
        raise ValueError("YAML block starting with 'cover:' not found")

    return match.group(1).strip()


def generate_cover_yaml(llm_input: dict) -> str:
    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {
                "role": "user",
                "content": USER_PROMPT.format(
                    input_json=json.dumps(llm_input, indent=2)
                ),
            },
        ],
        temperature=0.4,
    )

    content = response.choices[0].message.content
    if content is None:
        raise RuntimeError("LLM response content is None")

    yaml_text = extract_yaml(content)
    return yaml_text