
from pathlib import Path
import os
import yaml
from prod_assistant.logger.custom_logger import CustomLogger 

def _project_root() -> Path:
    # .../utils/config_loader.py -> parents[1] == project root
    return Path(__file__).resolve().parents[1]

def load_config(config_path: str | None = None) -> dict:
    """
    Resolve config path reliably irrespective of CWD.
    Priority: explicit arg > CONFIG_PATH env > <project_root>/config/config.yaml
    """
    env_path = os.getenv("CONFIG_PATH")
    if config_path is None:
        config_path = env_path or str(_project_root() / "config" / "config.yaml")
    
    logger = CustomLogger().get_logger(__file__)
    logger.info("Config data read from file", filename=config_path)
    path = Path(config_path)
    if not path.is_absolute():
        path = _project_root() / path

    if not path.exists():
        raise FileNotFoundError(f"Config file not found: {path}")

    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f) or {}
    

# if __name__ == "__main__":
#     # Example usage
#     config = load_config()
#     print(config)    