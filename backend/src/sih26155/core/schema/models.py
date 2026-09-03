from pydantic import BaseModel, Field
from typing import Any


class DeviceInfo(BaseModel):
    vendor: str | None = None
    model: str | None = None
    platform: str | None = None
    os_version: str | None = None
    hostname: str | None = None


class SSHConfig(BaseModel):
    enabled: bool | None = None
    version: int | None = None


class HTTPConfig(BaseModel):
    enabled: bool | None = None


class TelnetConfig(BaseModel):
    enabled: bool | None = None


class LoginProtection(BaseModel):
    enabled: bool | None = None
    attempts: int | None = None
    window_seconds: int | None = None
    block_seconds: int | None = None


class ManagementConfig(BaseModel):
    ssh: SSHConfig = Field(default_factory=SSHConfig)
    http: HTTPConfig = Field(default_factory=HTTPConfig)
    telnet: TelnetConfig = Field(default_factory=TelnetConfig)


class AuthenticationConfig(BaseModel):
    login_protection: LoginProtection = Field(
        default_factory=LoginProtection
    )


class LoggingConfig(BaseModel):
    enabled: bool | None = None


class SecurityBaseline(BaseModel):
    device: DeviceInfo = Field(default_factory=DeviceInfo)
    management: ManagementConfig = Field(default_factory=ManagementConfig)
    authentication: AuthenticationConfig = Field(
        default_factory=AuthenticationConfig
    )
    logging: LoggingConfig = Field(default_factory=LoggingConfig)