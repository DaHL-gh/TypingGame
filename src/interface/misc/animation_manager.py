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

    def add(self, animation: Animation, ignore_rebinding=False):
        animation.func(animation.start, animation.start, animation.end)

        if animation.id in self.animations_ids and ignore_rebinding:
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

    def update(self, curr_time: int):
        for anim in self.endings:
            if anim.end < curr_time - anim.start:
                anim.func(anim.start, anim.end, anim.end)
                self.remove(anim)
            else:
                break

        for anim in self.non_interval:
            anim.func(anim.start, curr_time, anim.end)

        for anim in self.with_interval:
            if curr_time > anim.last_work + anim.interval:
                iter_num = (curr_time - anim.start) // anim.interval
                anim.last_work = anim.start + anim.interval * iter_num
                anim.func(anim.start, anim.last_work, anim.end)


