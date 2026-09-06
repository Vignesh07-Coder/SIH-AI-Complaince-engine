from dataclasses import dataclass
from pathlib import Path


DEFAULT_MAX_FILE_SIZE = 10 * 1024 * 1024  # 10 MB


@dataclass(frozen=True)
class LoadedConfig:
    """
    Represents a successfully loaded configuration file.

    The loader is intentionally vendor-agnostic.
    It only validates and reads the configuration.
    """

    content: str
    source_file: str


class ConfigurationLoadError(Exception):
    """Raised when a configuration file cannot be safely loaded."""


def load_config(
    file_path: str | Path,
    *,
    max_file_size: int = DEFAULT_MAX_FILE_SIZE,
) -> LoadedConfig:
    """
    Load a network device configuration from a text file.

    Args:
        file_path:
            Path to the configuration file.

        max_file_size:
            Maximum allowed file size in bytes.

    Returns:
        LoadedConfig containing the decoded configuration and source name.

    Raises:
        ConfigurationLoadError:
            If the path is invalid, the file is too large, the file is
            empty, or the content cannot be decoded as UTF-8.
    """

    path = Path(file_path)

    if not path.exists():
        raise ConfigurationLoadError(
            f"Configuration file does not exist: {path}"
        )

    if not path.is_file():
        raise ConfigurationLoadError(
            f"Configuration path is not a file: {path}"
        )

    try:
        file_size = path.stat().st_size
    except OSError as exc:
        raise ConfigurationLoadError(
            f"Unable to inspect configuration file: {path}"
        ) from exc

    if file_size > max_file_size:
        raise ConfigurationLoadError(
            f"Configuration file is too large: {file_size} bytes "
            f"(maximum {max_file_size} bytes)"
        )

    if file_size == 0:
        raise ConfigurationLoadError(
            f"Configuration file is empty: {path}"
        )

    try:
        raw_content = path.read_bytes()
    except OSError as exc:
        raise ConfigurationLoadError(
            f"Unable to read configuration file: {path}"
        ) from exc

    # Configuration exports are expected to be text.
    # A NUL byte is a strong indicator that the uploaded file is binary
    # rather than a normal network configuration.
    if b"\x00" in raw_content:
        raise ConfigurationLoadError(
            f"Configuration file appears to be binary: {path}"
        )

    try:
        content = raw_content.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise ConfigurationLoadError(
            f"Configuration file is not valid UTF-8: {path}"
        ) from exc

    content = content.strip()

    if not content:
        raise ConfigurationLoadError(
            f"Configuration file contains no usable text: {path}"
        )

    return LoadedConfig(
        content=content,
        source_file=path.name,
    )