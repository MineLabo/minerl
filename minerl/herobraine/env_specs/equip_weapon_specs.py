# Copyright (c) 2020 All Rights Reserved
# Author: William H. Guss, Brandon Houghton

from minerl.herobraine.env_specs.human_controls import HumanControlEnvSpec
from minerl.herobraine.hero.mc import MS_PER_STEP, STEPS_PER_MS
from minerl.herobraine.hero.handler import Handler
import minerl.herobraine.hero.handlers as handlers
from typing import List

import minerl.herobraine
import minerl.herobraine.hero.handlers as handlers
from minerl.herobraine.env_spec import EnvSpec

TREECHOP_LENGTH = 8000
WEAPON = "iron_axe"


class EquipWeapon(HumanControlEnvSpec):
    def __init__(self, *args, **kwargs):
        if "name" not in kwargs:
            kwargs["name"] = "MineRLEquipWeapon-v0"

        super().__init__(
            *args, max_episode_steps=TREECHOP_LENGTH, reward_threshold=64.0, **kwargs
        )

    def create_rewardables(self) -> List[Handler]:
        return [
            # handlers.RewardForPickingItemInInventory([dict(type=WEAPON, reward=1.0)])
            # handlers.RewardForEquippingItem([dict(type=WEAPON, reward=5.0)])
        ]

    def create_agent_start(self) -> List[Handler]:
        return [handlers.RandomInventoryAgentStart({WEAPON: 1})]

    def create_observables(self) -> List[Handler]:
        return super().create_observables() + [
            # handlers.TypeObservation('mainhand', ALL_ITEMS)
        ]

    def create_agent_handlers(self) -> List[Handler]:
        return [
            # handlers.AgentQuitFromEquippingItem([
            #     dict(type=WEAPON)]
            # )
        ]

    def create_server_world_generators(self) -> List[Handler]:
        return [handlers.DefaultWorldGenerator(force_reset=True)]

    def create_server_quit_producers(self) -> List[Handler]:
        return [
            handlers.ServerQuitFromTimeUp((TREECHOP_LENGTH * MS_PER_STEP)),
            handlers.ServerQuitWhenAnyAgentFinishes(),
        ]

    def create_server_decorators(self) -> List[Handler]:
        return []

    def create_server_initial_conditions(self) -> List[Handler]:
        return [
            handlers.TimeInitialCondition(allow_passage_of_time=False),
            handlers.SpawningInitialCondition(allow_spawning=True),
        ]

    def determine_success_from_rewards(self, rewards: list) -> bool:
        return sum(rewards) >= self.reward_threshold

    def is_from_folder(self, folder: str) -> bool:
        return False

    def get_docstring(self):
        return ""