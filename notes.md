player champions need to plug into the system

- draw
- update (control loop)

needs to have config options to select submodules


class IGameObject:
    def handle_events(self, events): ...
    def update(self): ...
    def get_image(self): ...


class MyChampion(IGameObject):
    ...
    