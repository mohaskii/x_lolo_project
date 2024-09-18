class Cookie:
    def __init__(self, dict : dict):
        self.dict  = dict
    def encode(self) -> str :
        return "; ".join([f"{key}={value}" for key, value in self.dict.items()])