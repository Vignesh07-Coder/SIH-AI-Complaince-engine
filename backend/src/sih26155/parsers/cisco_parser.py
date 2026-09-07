"""Cisco IOS / IOS-XE parser for deterministic compliance evidence extraction."""

from __future__ import annotations

import re
from typing import List, Optional

from sih26155.core.core_contracts import Evidence, SecurityFact
from sih26155.parsers.base_parser import BaseParser


class CiscoParser(BaseParser):
    """Parse common Cisco configuration lines into canonical security facts."""

    _HOSTNAME_RE = re.compile(r"^hostname\s+(?P<name>\S+)$", re.IGNORECASE)
    _DOMAIN_NAME_RE = re.compile(r"^ip\s+domain-name\s+(?P<domain>\S+)$", re.IGNORECASE)
    _SSH_VERSION_RE = re.compile(r"^ip\s+ssh\s+version\s+(?P<version>\d+)$", re.IGNORECASE)
    _HTTP_SERVER_RE = re.compile(
        r"^(?P<negated>no\s+)?ip\s+http\s+server$", re.IGNORECASE
    )
    _HTTP_SECURE_SERVER_RE = re.compile(
        r"^(?P<negated>no\s+)?ip\s+http\s+secure-server$", re.IGNORECASE
    )
    _PASSWORD_ENCRYPTION_RE = re.compile(
        r"^(?P<negated>no\s+)?service\s+password-encryption$", re.IGNORECASE
    )
    _DOMAIN_LOOKUP_RE = re.compile(
        r"^(?P<negated>no\s+)?ip\s+domain-lookup$", re.IGNORECASE
    )
    _ENABLE_SECRET_RE = re.compile(
        r"^(?P<negated>no\s+)?enable\s+secret(?:\s+\d+)?(?:\s+.+)?$",
        re.IGNORECASE,
    )
    _USERNAME_RE = re.compile(
        r"^username\s+(?P<username>\S+)"
        r"(?:\s+privilege\s+(?P<privilege>\d+))?"
        r"(?:\s+(?P<credential_type>secret|password)(?:\s+\d+)?\s+"
        r"(?P<credential>.+))?$",
        re.IGNORECASE,
    )
    _LINE_VTY_RE = re.compile(
        r"^line\s+vty\s+(?P<start>\d+)\s+(?P<end>\d+)$", re.IGNORECASE
    )
    _TRANSPORT_INPUT_RE = re.compile(
        r"^transport\s+input(?:\s+(?P<value>.+))?$", re.IGNORECASE
    )
    _LOGIN_RE = re.compile(r"^login(?:\s+(?P<mode>local))?$", re.IGNORECASE)
    _EXEC_TIMEOUT_RE = re.compile(
        r"^exec-timeout\s+(?P<minutes>\d+)\s+(?P<seconds>\d+)$", re.IGNORECASE
    )
    _ACCESS_CLASS_RE = re.compile(
        r"^access-class\s+(?P<acl>\S+)\s+(?P<direction>in|out)$", re.IGNORECASE
    )

    @property
    def name(self) -> str:
        return "cisco"

    def parse(self, raw_data: str) -> List[SecurityFact]:
        facts: List[SecurityFact] = []
        current_section: Optional[str] = None

        for line_number, raw_line in enumerate(raw_data.splitlines(), start=1):
            stripped = raw_line.strip()

            if not stripped or stripped == "!":
                if not raw_line.startswith((" ", "\t")):
                    current_section = None
                continue

            if stripped.lower().startswith("line vty "):
                fact = self._parse_line_vty(stripped, raw_line, line_number)
                if fact is not None:
                    facts.append(fact)
                    current_section = "line vty"
                else:
                    current_section = None
                continue

            if raw_line.startswith((" ", "\t")) and current_section == "line vty":
                fact = self._parse_vty_subcommand(stripped, raw_line, line_number)
                if fact is not None:
                    facts.append(fact)
                continue

            current_section = None
            fact = self._parse_top_level(stripped, raw_line, line_number)
            if fact is not None:
                facts.append(fact)

        return facts

    def _parse_top_level(
        self, stripped: str, raw_line: str, line_number: int
    ) -> Optional[SecurityFact]:
        if match := self._HOSTNAME_RE.match(stripped):
            return self._fact(
                "device.hostname",
                match.group("name"),
                raw_line,
                line_number,
            )

        if match := self._DOMAIN_NAME_RE.match(stripped):
            return self._fact(
                "system.domain_name",
                match.group("domain"),
                raw_line,
                line_number,
            )

        if match := self._SSH_VERSION_RE.match(stripped):
            return self._fact(
                "management.ssh.version",
                int(match.group("version")),
                raw_line,
                line_number,
            )

        if match := self._HTTP_SERVER_RE.match(stripped):
            return self._fact(
                "management.http.server_enabled",
                not bool(match.group("negated")),
                raw_line,
                line_number,
            )

        if match := self._HTTP_SECURE_SERVER_RE.match(stripped):
            return self._fact(
                "management.http.secure_server_enabled",
                not bool(match.group("negated")),
                raw_line,
                line_number,
            )

        if match := self._PASSWORD_ENCRYPTION_RE.match(stripped):
            return self._fact(
                "security.password_encryption.enabled",
                not bool(match.group("negated")),
                raw_line,
                line_number,
            )

        if match := self._DOMAIN_LOOKUP_RE.match(stripped):
            return self._fact(
                "security.domain_lookup.enabled",
                not bool(match.group("negated")),
                raw_line,
                line_number,
            )

        if match := self._ENABLE_SECRET_RE.match(stripped):
            return self._fact(
                "authentication.enable_secret.present",
                not bool(match.group("negated")),
                raw_line,
                line_number,
            )

        if match := self._USERNAME_RE.match(stripped):
            privilege = match.group("privilege")
            return self._fact(
                "authentication.user",
                {
                    "username": match.group("username"),
                    "privilege": int(privilege) if privilege is not None else None,
                    "credential_type": match.group("credential_type"),
                    "credential_present": match.group("credential") is not None,
                },
                raw_line,
                line_number,
            )

        return None

    def _parse_line_vty(
        self, stripped: str, raw_line: str, line_number: int
    ) -> Optional[SecurityFact]:
        if match := self._LINE_VTY_RE.match(stripped):
            return self._fact(
                "access.line_vty.range",
                {
                    "start": int(match.group("start")),
                    "end": int(match.group("end")),
                },
                raw_line,
                line_number,
            )
        return None

    def _parse_vty_subcommand(
        self, stripped: str, raw_line: str, line_number: int
    ) -> Optional[SecurityFact]:
        if match := self._TRANSPORT_INPUT_RE.match(stripped):
            value = match.group("value")
            normalized = "none" if value is None else value.strip()
            return self._fact(
                "management.vty.transport_input",
                normalized,
                raw_line,
                line_number,
            )

        if match := self._LOGIN_RE.match(stripped):
            mode = match.group("mode") or "line-password"
            return self._fact(
                "management.vty.login_mode",
                mode.lower(),
                raw_line,
                line_number,
            )

        if match := self._EXEC_TIMEOUT_RE.match(stripped):
            return self._fact(
                "management.vty.exec_timeout",
                {
                    "minutes": int(match.group("minutes")),
                    "seconds": int(match.group("seconds")),
                },
                raw_line,
                line_number,
            )

        if match := self._ACCESS_CLASS_RE.match(stripped):
            return self._fact(
                "management.vty.access_class",
                {
                    "acl": match.group("acl"),
                    "direction": match.group("direction").lower(),
                },
                raw_line,
                line_number,
            )

        return None

    def _fact(
        self,
        rule_type: str,
        value: object,
        raw_line: str,
        line_number: int,
    ) -> SecurityFact:
        evidence = Evidence(
            source="cisco-config",
            raw_text=raw_line,
            line_number=line_number,
        )
        return SecurityFact(
            fact_id=f"{rule_type}:{line_number}",
            rule_type=rule_type,
            value=value,
            evidence=evidence,
        )


__all__ = ["CiscoParser"]
