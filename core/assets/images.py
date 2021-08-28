from enum import Enum
import pygame
from core.assets.assets import Assets, CustomAssets
from core.assets.image import Image


class Images(Enum):
    BACKPACK = Image("BackPack", "backpack1", 0)
    HEALTH = Image("Health", "health", 1)
    LEVEL = Image("Level", "level", 2)
    MANA = Image("Mana", "mana", 3)

    @staticmethod
    def getImage(iden):
        for image in Images:
            if image.value.id == iden:
                return image.value
        return None

    @staticmethod
    def load():
        for image in Images:
            if image.value.texturePath is not None:
                try:
                    image.value.image = pygame.transform.scale(
                        Assets[image.value.texturePath.upper()].value.image, (64, 64))
                    image.value.rect = image.value.image.get_rect()
                except KeyError:
                    try:
                        image.value.image = pygame.transform.scale(
                            CustomAssets[image.value.texturePath.upper()].value.image, (64, 64))
                        image.value.rect = image.value.image.get_rect()
                    except KeyError:
                        pass

    @staticmethod
    def getImageFromName(n):
        try:
            return Images[n.upper()].value
        except KeyError:
            return None
