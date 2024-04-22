
class Button:
    def __init__(self):
        self.pushed = False

    def push(self):
        self.pushed = not self.pushed
