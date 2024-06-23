from dataclasses import dataclass
from typing import Callable


@dataclass
class Animation:
    id: str
    func: Callable
    start: int
    interval: int | None = None
    end: int | None = None
    last_work: int = 0


class AnimationManager:
    def __init__(self):
        self.animations_ids: dict[str, Animation] = {}

        self.non_interval: list[Animation] = []
        self.with_interval: list[Animation] = []

        self.endless: list[Animation] = []
        self.endings: list[Animation] = []

    def add(self, animation: Animation):
        if animation.id in self.animations_ids:
            print('there is a problem')
        self.animations_ids[animation.id] = animation

        if animation.interval is None:
            self.non_interval.append(animation)
        else:
            self.with_interval.append(animation)

        if animation.end is not None:
            self.endings.append(animation)
        else:
            self.endless.append(animation)

    def pop(self, id: str):
        self.remove(self.animations_ids[id])
        self.animations_ids.pop(id)

    def remove(self, animation: Animation):
        if animation.interval is None:
            self.non_interval.remove(animation)
        else:
            self.with_interval.remove(animation)

        if animation.end is not None:
            self.endings.remove(animation)
        else:
            self.endless.remove(animation)

    def go(self, time: int):

        for a in self.endless:
            a.func(a.start, time, a.end)

        for a in self.endings:
            if a.end < time - a.start:
                a.func(a.start, a.end, a.end)
                self.remove(a)
            else:
                break

        for a in self.non_interval:
            a.func(a.start, time, a.end)

        for a in self.with_interval:
            if time - a.last_work > a.interval:
                a.func(a.start, time, a.end)
                a.last_work = time


