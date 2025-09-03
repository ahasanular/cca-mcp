import subprocess
import json
from typing import Dict, Any

class AIEnhancer:
    def __init__(self, model: str = "deepseek-coder:6.7b", ollama_host: str = "http://localhost:11434"):
        self.model = model
        self.ollama_host = ollama_host

    def enhance(self, base_report: Dict[str, Any]) -> Dict[str, Any]:
        prompt = self._build_prompt(base_report)
        response = self._call_ollama(prompt)
        ai_output = self._parse_ai_output(response)

        return {
            "report_tree": base_report,
            "enhanced_summary": ai_output
        }

    def _build_prompt(self, base_report: Dict[str, Any]) -> str:
        heading = base_report.get("heading", "")
        tree = base_report.get("tree", "")
        details = base_report.get("details", "")

        prompt = f"""
    You are an AI assistant tasked with generating a detailed, structured project report from the following initial raw project data.

The goal of this report is twofold:
1. Help human developers quickly onboard, understand, and start contributing.
2. Provide an AI agent with sufficient structured context, metadata, and relationships to understand, reason about, and contribute to any module or feature autonomously.

---

### Input:

**Heading:**

{heading}

**Project Tree:**

{tree}

**Module Details:**

{details}

---

### Requirements for the report:
I don't want any extra texts, **The output MUST be a valid JSON object** with the following keys and values:

1. **high_level_summary:**  
   - Describe the overall project purpose, domain, and tech stack.  
   - Summarize project scale (files, classes, functions, constants).

2. **project_structure:**  
   - Present a clear explanation of the folder/module hierarchy.  
   - For each top-level package/folder, describe its responsibility or domain role.

3. **detailed_component_breakdown:**  
   - For each package/module, list major classes, functions, and constants.  
   - Explain the main role or logic encapsulated by each significant class or function.  
   - Provide notes about class hierarchies or inheritance relationships if present.

4. **Inter_module_relationships_workflows:**  
   - Describe how major components interact or depend on each other (e.g., how scheduling generation, validation, scoring, and tracking integrate).  
   - Highlight entry points such as command-line scripts, views, or management commands.

5. **metadata_for_AI_parsing:**  
   - Use bullet points, consistent formatting, and explicit labeling (e.g., Class, Function, Constant).  
   - Identify critical classes/functions with a brief description to aid automated reasoning.  
   - Optionally add notes about data flow or control flow relevant to the module.

6. **onboarding_guidance:**  
   - Suggest concrete steps for a human or AI to begin working with the project (e.g., key modules to understand first, how to run commands, tests).  
   - Mention any conventions or patterns used (like mixins, model inheritance).

The JSON should be well-formed, easy to parse, and suitable for both AI ingestion and human consumption (when pretty-printed).

---

The **Report style:**  
   - Clear, concise, and logically organized with headings, subheadings, and bullet points.  
   - Suitable for intermediate Python/Django developers and AI models.

### Generate the final project report now using the provided input.
    """
        return prompt

    def _call_ollama(self, prompt: str) -> str:
        result = subprocess.run(
            ["ollama", "run", self.model],
            input=prompt.encode("utf-8"),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )

        stdout = result.stdout.decode("utf-8")
        stderr = result.stderr.decode("utf-8")

        if result.returncode != 0:
            raise RuntimeError(f"Ollama Error: {stderr}")

        # Debugging line — PRINT or LOG the response
        # print("==== RAW AI OUTPUT ====")
        # print(stdout)
        # print("=======================")

        return stdout

    def _parse_ai_output(self, response: str) -> Dict[str, Any]:
        try:
            # Try to extract JSON from the output
            # return response
            start = response.find('{')
            end = response.rfind('}') + 1
            return json.loads(response[start:end])
        except Exception as e:
            raise ValueError(f"Failed to parse AI response: {str(e)}")
