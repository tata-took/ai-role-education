from pathlib import Path
import re

BASE_ROLES_DIR = Path("roles")
ACTIVE_DIR = BASE_ROLES_DIR / "active"
ARCHIVE_DIR = BASE_ROLES_DIR / "archive"


def get_active_role_dir(role_name: str, version: int) -> Path:
    return ACTIVE_DIR / role_name / f"v{version}"


def get_archive_role_dir(role_name: str, version: int) -> Path:
    return ARCHIVE_DIR / role_name / f"v{version}"


def evolve_role(role_name: str, current_version: int) -> int:
    """
    Handle directory transitions during role evolution:
    - move current active version into archive
    - create next version under active
    - return the new version number
    """
    old_dir = get_active_role_dir(role_name, current_version)
    new_version = current_version + 1
    new_active_dir = get_active_role_dir(role_name, new_version)
    archive_dir = get_archive_role_dir(role_name, current_version)

    archive_dir.parent.mkdir(parents=True, exist_ok=True)
    if old_dir.exists():
        old_dir.rename(archive_dir)

    new_active_dir.mkdir(parents=True, exist_ok=True)

    return new_version


def _role_prompt_sort_key(path: Path) -> tuple[int, str]:
    match = re.search(r"_v(\d+)\.md$", path.name)
    version = int(match.group(1)) if match else -1
    return (version, path.name)


def find_role_prompt(role_name: str) -> Path:
    """Return the latest prompt file for a given role name.

    The function searches for files that follow ``{role_name}_agent_prompt*.md``
    under ``roles/`` and prefers the highest version suffix (e.g. ``_v3``).
    """

    candidates = list(BASE_ROLES_DIR.glob(f"{role_name}_agent_prompt*.md"))
    if not candidates:
        raise FileNotFoundError(f"No prompt found for role '{role_name}'")

    candidates.sort(key=_role_prompt_sort_key, reverse=True)
    return candidates[0]


def load_role_prompt(role_name: str, *, explicit_path: Path | None = None) -> str:
    """Load the system prompt text for a role.

    Args:
        role_name: Logical role identifier (e.g., ``teacher``).
        explicit_path: When provided, load from this path instead of resolving
            the latest version.
    """

    path = explicit_path or find_role_prompt(role_name)
    return path.read_text(encoding="utf-8")
