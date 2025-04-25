import ast
import time
import cProfile
import io
import pstats
import re
import textwrap
import traceback
from collections import defaultdict
import streamlit as st

class CodeReviewTool:
    def __init__(self, code):
        self.code = code
        self.suggestions = []

    def evaluate_code_quality(self):
        """Evaluates code quality based on style rules."""
        try:
            tree = ast.parse(self.code)
        except SyntaxError as e:
            self.suggestions.append(f"Syntax Error: {e}")
            return

        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                doc = ast.get_docstring(node)
                if not doc:
                    self.suggestions.append(f"Function '{node.name}' is missing a docstring. Explain what the function does.")
                elif "param" not in doc and len(node.args.args) > 0:
                    self.suggestions.append(f"Function '{node.name}' has a docstring, but consider documenting the parameters.")

                if not re.match(r'^[a-z_][a-z0-9_]*$', node.name):
                    self.suggestions.append(f"Function '{node.name}' should follow snake_case naming convention.")

                if len(node.body) > 50:
                    self.suggestions.append(f"Function '{node.name}' is too long. Consider splitting into smaller functions.")

            if isinstance(node, ast.If):
                nested_level = self.get_nesting_level(node)
                if nested_level > 3:
                    self.suggestions.append("Function has nested conditions more than 3 levels deep. Consider refactoring.")

    def get_nesting_level(self, node):
        """Helper to compute nesting level of conditionals."""
        level = 0
        while isinstance(node, ast.If):
            node = node.body[0] if node.body else None
            level += 1
        return level

    def calculate_cyclomatic_complexity(self):
        """Calculates cyclomatic complexity of the code."""
        tree = ast.parse(self.code)
        complexity = 0
        for node in ast.walk(tree):
            if isinstance(node, (ast.If, ast.For, ast.While, ast.And, ast.Or, ast.Try, ast.With)):
                complexity += 1
        return complexity

    def analyze_performance(self):
        """Analyzes the performance of the code using cProfile."""
        try:
            wrapped_code = textwrap.indent(self.code, '    ')
            exec_code = f"""
def run_code():
{wrapped_code}

import time
start_time = time.time()
run_code()
end_time = time.time()
print(f"Execution Time: {{end_time - start_time:.4f}} seconds")
"""

            pr = cProfile.Profile()
            pr.enable()
            exec(exec_code, {})
            pr.disable()

            s = io.StringIO()
            ps = pstats.Stats(pr, stream=s)
            ps.strip_dirs().sort_stats('cumulative').print_stats()
            return s.getvalue()

        except Exception as e:
            return f"Performance analysis failed: {e}\n{traceback.format_exc()}"

    def generate_report(self):
        """Generates a full review report."""
        self.evaluate_code_quality()
        complexity = self.calculate_cyclomatic_complexity()
        performance = self.analyze_performance()

        report = "Code Review Report:\n\n"
        report += "1. Code Quality Suggestions:\n"
        if self.suggestions:
            for suggestion in self.suggestions:
                report += f"- {suggestion}\n"
        else:
            report += "No issues found with naming, style, or documentation.\n"

        report += f"\n2. Cyclomatic Complexity: {complexity}\n"
        report += f"\n3. Performance Analysis:\n{performance}"
        return report

def code_review_interface():
    """Streamlit interface for the code review tool."""
    st.title("🧪 Python Code Review Tool")
    st.markdown("This tool evaluates your Python code for style, complexity, and performance.")

    example_code = '''def add_numbers(x, y):
    """Adds two numbers.

    Args:
        x (int): First number
        y (int): Second number

    Returns:
        int: Sum of the two numbers
    """
    return x + y

def calc_sum(arr):
    """Sums a list of positive numbers.

    Args:
        arr (list): List of integers

    Returns:
        int: Total of positive numbers
    """
    total = 0
    for item in arr:
        if item > 0:
            total += item
    return total
'''

    user_code = st.text_area("Paste your Python code here:", value=example_code, height=300)

    if st.button("🔍 Run Review"):
        tool = CodeReviewTool(user_code)
        report = tool.generate_report()
        st.code(report, language='markdown')
