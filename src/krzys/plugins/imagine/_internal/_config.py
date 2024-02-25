import os

import krzys.core.config

generator = "comfyui"
generator_host = "http://localhost:7868"

config_path = krzys.core.config.file_path("plugins", "imagine", "config.json")
if not os.path.exists(config_path):
    os.makedirs(os.path.dirname(config_path), exist_ok=True)
    print("Creating config file at", config_path, "with default values")
    with open(config_path, "w") as f:
        f.write('{"generator": "comfyui", "generator_host": "http://localhost:7868"}')