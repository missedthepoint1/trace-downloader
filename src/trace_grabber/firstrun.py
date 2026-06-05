import shutil

from . import paths

_DEFAULT_CONFIG = (
    "output_dir: ~/Trace Videos\n"
    "check_interval_hours: 3\n"
    "quality: highest\n"
    "team_urls: []\n"
)

def ensure_config() -> None:
    cfg = paths.data_dir() / "config.yaml"
    if cfg.exists():
        return
    template = paths.resource_dir() / "config.yaml"
    if template.exists():
        shutil.copyfile(template, cfg)
    else:
        cfg.write_text(_DEFAULT_CONFIG)

# Chrome runtime lock/socket files that break a plain copy and aren't needed
# to preserve the login (the cookies are stored elsewhere in the profile).
_PROFILE_IGNORE = shutil.ignore_patterns(
    "Running*", "Singleton*", "*.sock", "*.lock", "lockfile")

def migrate_dev() -> None:
    """Dev-only one-time: copy an existing repo session/accounts into the data dir."""
    if paths.is_frozen():
        return
    data = paths.data_dir()
    if (data / ".migrated").exists() or (data / "accounts.json").exists():
        return
    repo = paths.resource_dir()
    if not (repo / "accounts.json").exists():
        return
    for name in ("accounts.json", "config.yaml", ".chrome-profile", "state", "profiles"):
        src = repo / name
        if not src.exists():
            continue
        dst = data / name
        if src.is_dir():
            shutil.copytree(src, dst, dirs_exist_ok=True,
                            ignore=_PROFILE_IGNORE, ignore_dangling_symlinks=True)
        else:
            shutil.copyfile(src, dst)
    (data / ".migrated").write_text("")

def init() -> None:
    migrate_dev()
    ensure_config()
