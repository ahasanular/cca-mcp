from code_context_analyzer.analyzer import Analyzer

from utils.formatter import CustomFormatter


class CustomAnalyzer(Analyzer):
    def get_formatter(self, name: str = None):
        return CustomFormatter(
            method_preview=self.method_preview,
            doc_chars=self.doc_chars,
        )
