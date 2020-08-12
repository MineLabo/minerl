import abc
from abc import ABC
from minerl.herobraine.hero.handler import Handler


from minerl.herobraine.hero import handlers
from minerl.herobraine.hero.mc import INVERSE_KEYMAP
from minerl.herobraine.env_spec import EnvSpec

from typing import List

SIMPLE_KEYBOARD_ACITON = [
    "forward",
    "back",
    "left",
    "right",
    "jump",
    "sneak",
    "sprint",
    "attack"
]

class SimpleEmbodimentEnvSpec(EnvSpec, ABC):
    """
    A simple base environment from which all othe simple envs inherit.
    """


    def __init__(self, name, *args, resolution=(64,64), **kwargs):
        self.resolution = resolution
        super().__init__(name, *args, **kwargs)

    def create_observables(self) -> List[Handler]:
        return [
            handlers.POVObservation(self.resolution)
        ]
    
    def create_actionables(self) -> List[Handler]:
        """
        Simple envs have some basic keyboard control functionality, but
        not all.
        """
        return [
            handlers.KeybasedCommandAction(k, v) for k,v in INVERSE_KEYMAP.items()
            if k in SIMPLE_KEYBOARD_ACITON
        ] + [
            handlers.CameraAction()
        ]