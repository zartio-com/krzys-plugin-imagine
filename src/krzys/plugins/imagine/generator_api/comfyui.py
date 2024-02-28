import json
import os
import random
from urllib import request, parse

import krzys.core.config

from .base import BaseGeneratorApi
from .exception import PromptNotReadyException, BackendApiRequestException
from ..config import configuration


class ComfyUI(BaseGeneratorApi):
    _HOST: str = configuration.generator_host

    @staticmethod
    def queue_prompt(
            positive_prompt: str,
            negative_prompt: str,
            width: int,
            height: int,
            seed: int | None = None,
    ) -> str:
        with open(krzys.core.config.file_path('plugins', 'imagine', configuration.comfyui_workflow_file), "r") as f:
            workflow = f.read()

        workflow = json.loads(workflow.format(
            positive_prompt=positive_prompt.replace('"', '\\"'),
            negative_prompt=negative_prompt.replace('"', '\\"'),
            width=width,
            height=height,
            seed=seed or random.randint(0, 100000000)
        ))

        # noinspection PyBroadException
        try:
            response = json.loads(request.urlopen(
                request.Request("{}/prompt".format(ComfyUI._HOST), data=json.dumps({
                    "prompt": workflow,
                    "client_id": "krzys",
                }).encode("utf-8"))
            ).read())
        except Exception as e:
            raise BackendApiRequestException()

        return str(response["prompt_id"])

    @staticmethod
    def is_ready(prompt_id: str) -> bool:
        # noinspection PyBroadException
        try:
            res = json.loads(request.urlopen("{}/history/{}".format(ComfyUI._HOST, prompt_id)).read())
        except Exception:
            return False

        return prompt_id in res

    @staticmethod
    def get_result(prompt_id: str) -> list[bytes]:
        if not ComfyUI.is_ready(prompt_id):
            raise PromptNotReadyException()

        # noinspection PyBroadException
        try:
            res = json.loads(request.urlopen("{}/history/{}".format(ComfyUI._HOST, prompt_id)).read())
        except Exception:
            return []

        images: list[bytes] = []

        outputs = res[prompt_id]['outputs']
        for node_id in outputs:
            node_output = outputs[node_id]
            if 'images' not in node_output:
                continue

            for image in node_output['images']:
                # noinspection PyBroadException
                try:
                    images.append(request.urlopen("{}/view?filename={}&subfolder={}&type={}".format(
                        ComfyUI._HOST, image['filename'], image['subfolder'], image['type']
                    )).read())
                except Exception:
                    pass

        return images
