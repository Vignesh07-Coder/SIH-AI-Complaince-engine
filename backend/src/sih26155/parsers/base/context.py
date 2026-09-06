from dataclasses import dataclass


@dataclass
class ParserContext:
    """
    Tracks parsing context while walking through a configuration.

    Vendor-specific parsers may use this to represent hierarchical
    configuration sections.
    """

    current_section: str | None = None
    current_subsection: str | None = None

    def enter_section(self, section: str) -> None:
        """Enter a new top-level configuration section."""
        self.current_section = section
        self.current_subsection = None

    def enter_subsection(self, subsection: str) -> None:
        """Enter a nested configuration subsection."""
        self.current_subsection = subsection

    def reset(self) -> None:
        """Reset the parser context."""
        self.current_section = None
        self.current_subsection = None