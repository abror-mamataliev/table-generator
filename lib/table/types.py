class Table:

    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            self.__dict__[key] = value

    def _generate_html(self):
        pass

    def _generate_json(self):
        pass
    
    def _generate_excel(self):
        pass

    def generate_table(self):
        match self.format:
            case "html":
                self._generate_html()
            case "json":
                self._generate_json()
            case "excel":
                self._generate_excel()
            case _:
                raise ValueError("Invalid format")
