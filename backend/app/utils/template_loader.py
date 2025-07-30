"""Template loading utilities for email templates."""

from pathlib import Path
from typing import Any

from jinja2 import Environment, FileSystemLoader, Template


class TemplateLoader:
    """Utility class for loading and rendering email templates using Jinja2."""

    def __init__(self, templates_dir: str | Path | None = None) -> None:
        """Initialize template loader with Jinja2 environment.

        Args:
            templates_dir: Path to templates directory. Defaults to backend/templates
        """
        if templates_dir is None:
            # Default to backend/templates directory
            current_dir = Path(__file__).parent
            self.templates_dir = current_dir.parent.parent / "templates"
        else:
            self.templates_dir = Path(templates_dir)

        # Create Jinja2 environment with FileSystemLoader
        self.env = Environment(
            loader=FileSystemLoader(self.templates_dir),
            autoescape=True,  # Auto-escape HTML for security
            trim_blocks=True,  # Remove trailing newlines
            lstrip_blocks=True,  # Strip leading whitespace
        )

    def load_template(self, template_name: str) -> Template:
        """Load template from file.

        Args:
            template_name: Name of the template file (e.g., "emails/user_verification.html")

        Returns:
            Template: Jinja2 template object

        Raises:
            TemplateNotFound: If template file doesn't exist
        """
        return self.env.get_template(template_name)

    def render_template(self, template_name: str, context: dict[str, Any]) -> str:
        """Load and render template with context variables.

        Args:
            template_name: Name of the template file (e.g., "emails/user_verification.html")
            context: Dictionary of variables to substitute in template

        Returns:
            str: Rendered template content
        """
        template = self.load_template(template_name)
        return template.render(**context)
