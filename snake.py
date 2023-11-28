class Snake:
    def __init__(self, id, name, health, body, latency, head, length, shout, squad, customizations):
        self.id = id
        self.name = name
        self.health = health
        self.body = [(part['x'], part['y']) for part in body]
        self.latency = latency
        self.head = (head['x'], head['y'])
        self.length = length
        self.shout = shout
        self.squad = squad
        self.customizations = customizations