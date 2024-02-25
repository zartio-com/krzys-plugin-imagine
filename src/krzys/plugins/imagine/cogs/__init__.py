from .imagine import ImagineCog

try:
    from .imagine_faceswap import ImagineFaceSwapCog
except ModuleNotFoundError:
    pass
