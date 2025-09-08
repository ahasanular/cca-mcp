import logging
from typing import Any, Dict, List

from code_context_analyzer.formatters.default import LegacyCodeFormatter

logger = logging.getLogger(__name__)


class CustomFormatter(LegacyCodeFormatter):
    def format(self, parsed_data: List[Dict[str, Any]]) -> Dict[str, str]:
        """Generate the complete markup report with improved structure."""
        if not parsed_data:
            logger.warning("No data to format")
            return {
                "heading": "No Data",
                "tree": "No directory structure available",
                "details": "No code details available",
                "full": "No data to generate report",
            }

        self.parsed_data = parsed_data
        self.project_name = self._extract_project_name()

        heading = self._generate_heading()
        tree = self._generate_tree()
        description = self._generate_detailed_description()

        # Create structured output
        full_report = f"{heading}\n\n## Tree Structure:\n{tree}\n\n## Detailed Description:\n{description}"

        # Apply truncation if needed
        if self.truncate_total and len(full_report) > self.truncate_total:
            logger.warning(
                f"Report truncated from {len(full_report)} to {self.truncate_total} characters"
            )
            allowed_length = self.truncate_total
            truncated_report = (
                full_report[:allowed_length] + "\n\n... (truncated due to length)"
            )
            return {
                "heading": heading,
                "tree": tree,
                "details": description,
                "full": truncated_report,
                "truncated": True,
                "original_length": len(full_report),
            }

        return {
            "heading": heading,
            "tree": tree,
            "details": description,
            "full": full_report,
            "truncated": False,
        }
