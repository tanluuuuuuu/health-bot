from langchain_core.prompts import ChatPromptTemplate
from langchain_core.prompts.prompt import PromptTemplate
import os

def load_prompt_template(template_name: str) -> PromptTemplate:
    """Load a prompt template from the prompts directory."""
    # Get the directory of the current file
    current_dir = os.path.dirname(os.path.abspath(__file__))
    # Go up one level to src directory
    src_dir = os.path.dirname(current_dir)
    # Path to the prompts directory
    prompts_dir = os.path.join(src_dir, "prompts")
    # Full path to the template file
    template_path = os.path.join(prompts_dir, f"{template_name}.jinja2")

    # Check if the template file exists
    if not os.path.exists(template_path):
        raise FileNotFoundError(f"Template file not found: {template_path}")

    # Read the template file
    with open(template_path, "r") as f:
        template_content = f.read()

    # Create and return a prompt template
    return PromptTemplate.from_template(template_content)