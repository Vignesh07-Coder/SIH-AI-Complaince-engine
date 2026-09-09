from __future__ import annotations

import re

from sih26155.core.contracts.parser import ParseResult
from sih26155.core.evidence.models import Evidence
from sih26155.core.facts.models import SecurityFact
from sih26155.core.schema.enums import ConfidenceSource


class CiscoIOSParser:
    """
    Deterministic parser for common Cisco IOS / IOS-XE
    security-relevant configuration.

    The parser intentionally extracts only semantics that we
    explicitly understand. Everything else remains in
    unknown_lines for the AI semantic-mapping stage.
    """

    _HOSTNAME_RE = re.compile(
        r"^hostname\s+(?P<name>\S+)$",
        re.IGNORECASE,
    )

    _SSH_VERSION_RE = re.compile(
        r"^ip\s+ssh\s+version\s+(?P<version>\d+)$",
        re.IGNORECASE,
    )

    _HTTP_SERVER_RE = re.compile(
        r"^(?P<negated>no\s+)?ip\s+http\s+server$",
        re.IGNORECASE,
    )

    _DOMAIN_NAME_RE = re.compile(
        r"^ip\s+domain[- ]name\s+(?P<domain>\S+)$",
        re.IGNORECASE,
    )

    _LOGIN_BLOCK_RE = re.compile(
        r"^login\s+block-for\s+"
        r"(?P<block>\d+)\s+"
        r"attempts\s+(?P<attempts>\d+)\s+"
        r"within\s+(?P<within>\d+)$",
        re.IGNORECASE,
    )

    _LOGGING_RE = re.compile(
        r"^logging\s+.+$",
        re.IGNORECASE,
    )

    _LINE_VTY_RE = re.compile(
        r"^line\s+vty\s+(?P<start>\d+)(?:\s+(?P<end>\d+))?$",
        re.IGNORECASE,
    )

    _TRANSPORT_INPUT_RE = re.compile(
        r"^transport\s+input(?:\s+(?P<value>.+))?$",
        re.IGNORECASE,
    )

    _LOGIN_RE = re.compile(
        r"^login(?:\s+(?P<mode>local))?$",
        re.IGNORECASE,
    )

    _EXEC_TIMEOUT_RE = re.compile(
        r"^exec-timeout\s+(?P<minutes>\d+)(?:\s+(?P<seconds>\d+))?$",
        re.IGNORECASE,
    )

    @property
    def name(self) -> str:
        return "cisco-ios"

    def parse(
        self,
        config: str,
        source_file: str,
    ) -> ParseResult:

        facts: list[SecurityFact] = []
        evidence: list[Evidence] = []
        unknown_lines: list[str] = []

        current_section: str | None = None

        lines = config.splitlines()

        for line_number, raw_line in enumerate(lines, start=1):
            stripped = raw_line.strip()

            # ---------------------------------------------------------
            # Blank lines and Cisco section separators.
            # ---------------------------------------------------------

            if not stripped or stripped == "!":
                current_section = None
                continue

            # ---------------------------------------------------------
            # Section detection
            # ---------------------------------------------------------

            if self._LINE_VTY_RE.match(stripped):
                current_section = "line-vty"

                self._add_fact(
                    facts=facts,
                    evidence=evidence,
                    field="management.vty.range",
                    value=self._parse_vty_range(stripped),
                    raw_line=raw_line,
                    line_number=line_number,
                    source_file=source_file,
                )

                continue

            # ---------------------------------------------------------
            # VTY subcommands
            # ---------------------------------------------------------

            if (
                current_section == "line-vty"
                and raw_line.startswith((" ", "\t"))
            ):
                transport_facts = self._parse_vty_transport(
                    stripped=stripped,
                    raw_line=raw_line,
                    line_number=line_number,
                    source_file=source_file,
                )

                if transport_facts is not None:
                    for fact, ev in transport_facts:
                        facts.append(fact)
                        evidence.append(ev)

                    continue

                parsed = self._parse_vty_subcommand(
                    stripped=stripped,
                    raw_line=raw_line,
                    line_number=line_number,
                    source_file=source_file,
                )

                if parsed is not None:
                    fact, ev = parsed
                    facts.append(fact)
                    evidence.append(ev)
                else:
                    unknown_lines.append(raw_line)

                continue

            # ---------------------------------------------------------
            # Top-level commands
            # ---------------------------------------------------------

            parsed = self._parse_top_level(
                stripped=stripped,
                raw_line=raw_line,
                line_number=line_number,
                source_file=source_file,
            )

            if parsed is not None:
                fact, ev = parsed
                facts.append(fact)
                evidence.append(ev)
            else:
                unknown_lines.append(raw_line)

        return ParseResult(
            facts=facts,
            evidence=evidence,
            unknown_lines=unknown_lines,
        )

    # =================================================================
    # TOP LEVEL
    # =================================================================

    def _parse_top_level(
        self,
        stripped: str,
        raw_line: str,
        line_number: int,
        source_file: str,
    ) -> tuple[SecurityFact, Evidence] | None:

        # hostname EDGE-01
        match = self._HOSTNAME_RE.match(stripped)

        if match:
            return self._make_fact(
                field="device.hostname",
                value=match.group("name"),
                raw_line=raw_line,
                line_number=line_number,
                source_file=source_file,
            )

        # ip ssh version 2
        match = self._SSH_VERSION_RE.match(stripped)

        if match:
            return self._make_fact(
                field="management.ssh.version",
                value=int(match.group("version")),
                raw_line=raw_line,
                line_number=line_number,
                source_file=source_file,
            )

        # ip http server / no ip http server
        match = self._HTTP_SERVER_RE.match(stripped)

        if match:
            return self._make_fact(
                field="management.http.enabled",
                value=not bool(match.group("negated")),
                raw_line=raw_line,
                line_number=line_number,
                source_file=source_file,
            )

        # ip domain-name example.com
        match = self._DOMAIN_NAME_RE.match(stripped)

        if match:
            return self._make_fact(
                field="system.domain_name",
                value=match.group("domain"),
                raw_line=raw_line,
                line_number=line_number,
                source_file=source_file,
            )

        # login block-for 120 attempts 3 within 60
        match = self._LOGIN_BLOCK_RE.match(stripped)

        if match:
            value = {
                "enabled": True,
                "block_seconds": int(match.group("block")),
                "attempts": int(match.group("attempts")),
                "window_seconds": int(match.group("within")),
            }

            return self._make_fact(
                field="authentication.login_protection",
                value=value,
                raw_line=raw_line,
                line_number=line_number,
                source_file=source_file,
            )

        # logging buffered / logging host ...
        if self._LOGGING_RE.match(stripped):
            return self._make_fact(
                field="logging.enabled",
                value=True,
                raw_line=raw_line,
                line_number=line_number,
                source_file=source_file,
            )

        return None

    # =================================================================
    # VTY TRANSPORT
    # =================================================================

    def _parse_vty_transport(
        self,
        stripped: str,
        raw_line: str,
        line_number: int,
        source_file: str,
    ) -> list[tuple[SecurityFact, Evidence]] | None:

        match = self._TRANSPORT_INPUT_RE.match(stripped)

        if not match:
            return None

        value = match.group("value")

        if value is None:
            protocols: list[str] = []
        else:
            protocols = value.lower().split()

        # Cisco VTY transport semantics:
        #
        # transport input ssh
        #   -> SSH enabled, Telnet disabled
        #
        # transport input telnet ssh
        #   -> SSH enabled, Telnet enabled
        #
        # transport input none
        #   -> SSH disabled, Telnet disabled

        ssh_enabled = "ssh" in protocols
        telnet_enabled = "telnet" in protocols

        ssh_fact, ssh_evidence = self._make_fact(
            field="management.ssh.enabled",
            value=ssh_enabled,
            raw_line=raw_line,
            line_number=line_number,
            source_file=source_file,
        )

        telnet_fact, telnet_evidence = self._make_fact(
            field="management.telnet.enabled",
            value=telnet_enabled,
            raw_line=raw_line,
            line_number=line_number,
            source_file=source_file,
        )

        return [
            (ssh_fact, ssh_evidence),
            (telnet_fact, telnet_evidence),
        ]

    # =================================================================
    # VTY SUBCOMMANDS
    # =================================================================

    def _parse_vty_subcommand(
        self,
        stripped: str,
        raw_line: str,
        line_number: int,
        source_file: str,
    ) -> tuple[SecurityFact, Evidence] | None:

        # login
        # login local
        match = self._LOGIN_RE.match(stripped)

        if match:
            mode = match.group("mode")

            return self._make_fact(
                field="management.vty.login_mode",
                value=mode.lower() if mode else "line-password",
                raw_line=raw_line,
                line_number=line_number,
                source_file=source_file,
            )

        # exec-timeout 5 0
        match = self._EXEC_TIMEOUT_RE.match(stripped)

        if match:
            value = {
                "minutes": int(match.group("minutes")),
                "seconds": int(match.group("seconds") or 0),
            }

            return self._make_fact(
                field="management.vty.exec_timeout",
                value=value,
                raw_line=raw_line,
                line_number=line_number,
                source_file=source_file,
            )

        return None

    # =================================================================
    # FACT / EVIDENCE CREATION
    # =================================================================

    def _make_fact(
        self,
        field: str,
        value: object,
        raw_line: str,
        line_number: int,
        source_file: str,
    ) -> tuple[SecurityFact, Evidence]:

        evidence_id = (
            f"evidence:cisco-ios:{source_file}:{line_number}"
        )

        evidence = Evidence(
            source_file=source_file,
            raw_text=raw_line,
            line_number=line_number,
            source_type="configuration",
            parser=self.name,
            confidence=1.0,
        )

        fact = SecurityFact(
            field=field,
            value=value,
            confidence=1.0,
            source=ConfidenceSource.DETERMINISTIC,
            evidence_id=evidence_id,
        )

        return fact, evidence

    def _add_fact(
        self,
        facts: list[SecurityFact],
        evidence: list[Evidence],
        field: str,
        value: object,
        raw_line: str,
        line_number: int,
        source_file: str,
    ) -> None:

        fact, ev = self._make_fact(
            field=field,
            value=value,
            raw_line=raw_line,
            line_number=line_number,
            source_file=source_file,
        )

        facts.append(fact)
        evidence.append(ev)

    # =================================================================
    # VTY RANGE
    # =================================================================

    def _parse_vty_range(
        self,
        stripped: str,
    ) -> dict[str, int]:

        match = self._LINE_VTY_RE.match(stripped)

        if not match:
            return {}

        start = int(match.group("start"))
        end = match.group("end")

        return {
            "start": start,
            "end": int(end) if end is not None else start,
        }