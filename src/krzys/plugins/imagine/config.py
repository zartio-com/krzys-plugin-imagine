from ._internal import config as _internal_config
import krzys.core.config

generator_host: str = "http://192.168.69.172:7868"  # TODO: move to config
# comfyui_workflow: str = krzys.core.config.file_path("plugins", "imagine", "anime.json")
comfyui_workflow: str = krzys.core.config.file_path("plugins", "imagine", "comfyui_workflow_cascade.json")
# generator: generator_api.BaseGeneratorApi | None = None
# if _internal_config.generator == "comfyui":
#     generator = generator_api.ComfyUI()

# assert generator is not None
