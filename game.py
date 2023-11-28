class Game:
    def __init__(self, id, ruleset, map, timeout, source):
        self.id = id
        self.ruleset_name = ruleset['name']
        self.ruleset_version = ruleset['version']
        self.map = map
        self.timeout = timeout
        self.source = source