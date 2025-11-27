# TODO consider a context manager that automatically removes a champ
# unless battleapi objects are created every time? If so need to gen string before and set.

from .action_system import ActionSystem


class BattleAPI:
    def __init__(self, champion, arena):
        self._champ = champion
        self._actions = []
        self._arena_state = self._generate_arena_state_string(arena)

    def move(self, displacement: tuple[int, int]):
        self._actions.append((ActionSystem.MOVE, self._champ, displacement))    

    def scan(self):
        return self._arena_state

    def _bind_champion(self, champion):
        self._champ = champion
    
    def _drain(self):
        actions = self._actions
        self._actions = []
        self._champ = None
        return actions

    def _generate_arena_state_string(self, arena):
        return "some state string"