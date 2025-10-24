import json
from typing import Union


class FileManager:

    @staticmethod
    def readFile(filename: str) -> Union[str, object]:
        with open(filename, "r") as f:
            if filename.endswith(".json"):
                return json.load(f)
            return f.read()

    @staticmethod
    def writeFile(filename: str, content: str) -> None:
        with open(filename, "w") as f:
            if filename.endswith(".json"):
                json.dump(content, f)
            else:
                f.write(content)

    @staticmethod
    def jsonStringify(data: object) -> str:
        return json.dumps(data)
