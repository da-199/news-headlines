from typing import Dict, Any
from sources.nbc import nbc
from sources.abc import abc
from sources.nyt import nyt

class Main:

    def __init__(self):
        self.sources = {
            "nbc": nbc,
            "abc": abc,
            "nyt": nyt
        }

    def run_all(self) -> Dict[str, any]:
        output = {}
        for name, source in self.sources.items():
            source_output = source(event, context)
            output.update(source_output)

        return output

if __name__ == "__main__":
    event = ''
    context = ''
    main = Main()
    output = main.run_all()