from sih26155.parsers.base.context import ParserContext
from sih26155.parsers.base.result import ParserOutput

def test_parser_context_section():
    context = ParserContext()

    assert context.current_section is None
    assert context.current_subsection is None

    context.enter_section("line vty 0 4")

    assert context.current_section == "line vty 0 4"
    assert context.current_subsection is None


def test_parser_context_subsection():
    context = ParserContext()

    context.enter_section("line vty 0 4")
    context.enter_subsection("authentication")

    assert context.current_section == "line vty 0 4"
    assert context.current_subsection == "authentication"


def test_parser_context_reset():
    context = ParserContext()

    context.enter_section("line vty 0 4")
    context.enter_subsection("authentication")
    context.reset()

    assert context.current_section is None
    assert context.current_subsection is None


def test_parser_output_defaults():
    output = ParserOutput()

    assert output.facts == []
    assert output.evidence == []
    assert output.unknown_lines == []