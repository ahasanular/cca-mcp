"""
AIEnhancer: async, robust wrapper around Ollama HTTP API (instead of CLI subprocess).

Features:
- non-blocking async HTTP calls via httpx
- timeout and retries with exponential backoff
- robust JSON extraction from model output (with fallback to raw text)
- flexible configuration: model name, host, timeout, retries
- sync wrapper for legacy environments
"""

from __future__ import annotations

import asyncio
import json
import logging
import re
from dataclasses import dataclass
from typing import Any, Dict, Optional

import httpx

logger = logging.getLogger(__name__)


@dataclass
class AIEnhancer:
    model: str = "deepseek-coder:6.7b"
    ollama_host: str = "http://localhost:11434"  # base URL
    timeout: float = 3000.0  # request timeout
    retries: int = 2  # retry attempts
    retry_backoff: float = 1.5  # exponential backoff multiplier
    max_response_chars: Optional[int] = 200_000

    async def enhance(self, base_report: Dict[str, Any]) -> Dict[str, Any]:
        """
        Async entrypoint to enrich base_report using Ollama API.

        Returns a dict containing:
          - report_tree: original report
          - enhanced_summary: parsed JSON or {"text": raw}
          - raw_ai: raw model output
          - error: error message if something failed
        """
        prompt = self._build_prompt(base_report)

        attempt = 0
        last_exc: Optional[Exception] = None

        while attempt <= self.retries:
            try:
                raw = await self._call_ollama_api(prompt)
                parsed = self._parse_ai_output(raw)
                return {
                    "report_tree": base_report,
                    "enhanced_summary": parsed,
                    "raw_ai": raw,
                }
            except Exception as exc:
                last_exc = exc
                attempt += 1
                if attempt <= self.retries:
                    wait_for = (self.retry_backoff ** attempt)
                    logger.warning(
                        # "AIEnhancer attempt %d/%d failed: %s — retrying in %.1fs",
                        str(exc),
                        attempt,
                        self.retries,
                        exc,
                        wait_for,
                    )
                    await asyncio.sleep(wait_for)

        # If we reach here, all retries failed
        err_msg = str(last_exc) if last_exc else "Unknown error"
        logger.error("AIEnhancer failed after retries: %s", err_msg)
        return {
            "report_tree": base_report,
            "enhanced_summary": {"error": err_msg},
            "raw_ai": None,
            "error": err_msg,
        }

    def enhance_sync(self, base_report: Dict[str, Any]) -> Dict[str, Any]:
        """Sync wrapper for environments without asyncio."""
        return asyncio.run(self.enhance(base_report))

    def _build_prompt(self, base_report: Dict[str, Any]) -> str:
        heading = base_report.get("heading", "")
        tree = base_report.get("tree", "")
        details = base_report.get("details", "")

        """
        Placeholder for your custom prompt builder.
        Replace contents with your own logic later.
        """
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

    async def _call_ollama_api(self, prompt: str) -> str:
        """
        Call Ollama HTTP API asynchronously.
        Endpoint: POST /api/generate
        Docs: https://github.com/ollama/ollama/blob/main/docs/api.md
        """
        url = f"{self.ollama_host}/api/generate"

        payload = {
            "model": self.model,
            "prompt": prompt,
            "stream": False,  # easier parsing: whole response at once
        }

        async with httpx.AsyncClient(timeout=self.timeout) as client:
            resp = await client.post(url, json=payload)

        if resp.status_code != 200:
            raise RuntimeError(f"Ollama API error {resp.status_code}: {resp.text}")

        data = resp.json()

        # Ollama API returns {"response": "..."} when stream=False
        output = data.get("response", "")
        if self.max_response_chars and len(output) > self.max_response_chars:
            logger.warning(
                "Truncating AI response from %d to %d chars",
                len(output),
                self.max_response_chars,
            )
            output = output[: self.max_response_chars]

        return output

    def _parse_ai_output(self, response: Optional[str]) -> Any:
        """
        Try to parse AI response as JSON, fallback to {"text": response}.
        """
        if not response:
            raise ValueError("Empty model response")

        # 1. Try direct parse
        try:
            return json.loads(response)
        except Exception:
            pass

        # 2. Try extract first {...} block
        try:
            start = response.find("{")
            end = response.rfind("}") + 1
            if start != -1 and end != -1 and end > start:
                return json.loads(response[start:end])
        except Exception:
            pass

        # 3. Regex fallback
        try:
            match = re.search(r"\{.*\}", response, flags=re.DOTALL)
            if match:
                return json.loads(match.group(0))
        except Exception:
            pass

        # 4. Fallback raw
        logger.debug("Falling back to raw text response; could not parse JSON.")
        return {"text": response}
