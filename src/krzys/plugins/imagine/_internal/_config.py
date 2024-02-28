import os
import pydantic

import krzys.core.config


_config_path = krzys.core.config.file_path("plugins", "imagine", "config.json")
_path = krzys.core.config.file_path("plugins", "imagine", "workflows")
if not os.path.exists(_path):
    os.makedirs(_path, exist_ok=True)
    with open(os.path.join(_path, "put_your_workflows_here"), "w") as f:
        f.write('')


class ImagineConfig(pydantic.BaseModel):
    generator: str = "comfyui"
    generator_host: str = "http://127.0.0.1:7868"
    comfyui_workflow_file: str = "workflows/comfyui_workflow.json"
    generation_sizes: dict[str, tuple[int, int]] = {
        "1:1": (1024, 1024),
        "2:3": (832, 1248),
        "3:2": (1248, 832),
        "16:9": (1280, 720),
        "9:16": (720, 1280)
    }

    def save(self):
        with open(_config_path, "w") as f:
            f.write(self.json(indent=4))

    @staticmethod
    def load():
        if not os.path.exists(_config_path):
            config = ImagineConfig()
            config.save()
            return config

        return ImagineConfig.parse_file(_config_path)


configuration = ImagineConfig.load()
