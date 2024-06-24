from dataclasses import dataclass
from typing import Callable


@dataclass
class Animation:
    id: str
    func: Callable
    start: int
    interval: int | None = None
    end: int | None = None

    def __post_init__(self):
        self.last_work = self.start


class AnimationManager:
    def __init__(self):
        self.animations_ids: dict[str, Animation] = {}

        self.non_interval: list[Animation] = []
        self.with_interval: list[Animation] = []

        self.endings: list[Animation] = []

    def get(self, id: str):
        for a in self.non_interval:
            if a.id == id:
                return a

        for a in self.with_interval:
            if a.id == id:
                return a

    def add(self, animation: Animation):
        animation.func(animation.start, animation.start, animation.end)

        if animation.id in self.animations_ids:
            print('WARNING: animation with this id already exists; it has been replaced')
        self.animations_ids[animation.id] = animation

        if animation.interval is None:
            self.non_interval.append(animation)
        else:
            self.with_interval.append(animation)

        if animation.end is not None:
            self.endings.append(animation)

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

    def go(self, time: int):
        for a in self.endings:
            if a.end < time - a.start:
                a.func(a.start, a.end, a.end)
                self.remove(a)
            else:
                break

        for a in self.non_interval:
            a.func(a.start, time, a.end)

        for a in self.with_interval:
            if time > a.last_work + a.interval:
                a.last_work += a.interval
                a.func(a.start, a.last_work, a.end)


