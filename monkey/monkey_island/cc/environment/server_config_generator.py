from pathlib import Path


def create_default_config_file(path):
    default_config_path = f"{path}.default"
    default_config = Path(default_config_path).read_text()
    Path(path).write_text(default_config)
