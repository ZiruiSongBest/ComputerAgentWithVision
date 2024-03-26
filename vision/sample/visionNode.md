vision node:

'name': Node type

Node:

    class ActionNode:
    def __init__(self, name, description, type):
        self._name = name
        self._description = description
        self._return_val = ''
        self._relevant_code = {}
        self._next_action = {}
        self._status = False
        self._type = type