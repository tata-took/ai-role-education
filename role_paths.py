from pathlib import Path

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
