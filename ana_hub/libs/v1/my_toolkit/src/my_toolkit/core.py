def get_version():
    return "1.0.0"


class Processor:
    def __init__(self):
        self.version = get_version()

    def print_version(self):
        """印出當前模組的版本資訊"""
        print(f"Current Processor Version: {self.version}")

    def process(self, data):
        return f"Data handled: {data}"
