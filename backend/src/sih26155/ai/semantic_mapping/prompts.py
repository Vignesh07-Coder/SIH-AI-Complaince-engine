def build_mapping_prompt(unknown_text: str, context: str, similar_examples: list[dict]) -> str:
    """
    Builds the prompt sent to an LLM (if used) to interpret an unknown
    config line. Kept separate from logic so wording can be tuned freely.
    """
    examples_block = "\n".join(
        f"- '{e['source_text']}' -> field={e['field']}, value={e['value']}"
        for e in similar_examples
    ) or "None found."

    return f"""
You are identifying what an unrecognized network configuration line means.

Vendor/context: {context}
Unknown line: {unknown_text}

Similar known examples:
{examples_block}

Respond ONLY in JSON with exactly these fields: field, value, confidence (0-1), reason.
Do NOT include any compliance judgment (pass/fail/violation/severity).
"""