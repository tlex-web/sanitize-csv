import os
import re
from tabulate import tabulate


class CSVSanitizer:
    def __init__(self, cwd) -> None:
        self.cwd = cwd
        self.file_path = ""
        self.path_flag = ""
        self.delimiter = ""

    def init(self) -> None:
        print("-" * 60)
        print("CLI Application to sanitize the delimiter in csv files")
        print("-" * 60)
        print(f"CWD: {self.cwd}")
        print("-" * 60)

        table_information = [
            ["Parameter", "Description", "Value"],
            ["Path", "Provide the file path", "file.csv or C:/.../file.csv"],
            ["Flag", "Absolute or relative path", "a or r"],
            ["Delimiter", "Delimiter used in csv file", "e.g. ;"],
        ]

        print(tabulate(table_information, headers="firstrow", tablefmt="grid"))

        print("\n")

    def sanitize_file(self) -> list[str] | None:
        """
        Sanitize the files content from duplicate delimiters
        Beware: This software cannot distinguish between the semantics
        and the syntax. Check if the removal of the delimiter lowers
        the information of the file
        """

        with open(file=self.file_path, mode="r") as file:  # type: ignore
            readableStream = list(file.read())

            letter_count = 0
            counter = 0
            dic = {"count": [], "action": []}
            tmp = []

            for index, letter in enumerate(readableStream):
                if letter == self.delimiter:
                    letter_count += 1
                    dic["action"].append(f"Count: {counter}")

                if letter_count >= 1 and letter != self.delimiter:
                    letter_count = 0
                    dic["action"].append(f"Stop: {counter}")

                if letter_count > 1 and letter == self.delimiter:
                    dic["action"].append(f"Remove: {counter}")

                    tmp.append(index)

                counter += 1

            sanitized_list = [i for j, i in enumerate(readableStream) if j not in tmp]

            if len(tmp) == 0:
                print("No duplicate delimiter found")
                return None

            else:
                print("-" * 60)
                print(f"Removed {len(tmp)} from {len(readableStream)} data entries")
                print("-" * 60)

                return sanitized_list

    def get_params(self) -> dict[str, str]:
        """
        Get user input via STDIN and type check the data
        """
        while True:
            try:
                self.file_path = str(input("File Path: ")).strip()
                self.path_flag = str(input("Absolute or relative path: ")).strip()
                self.delimiter = str(input("Delimiter: ")).strip()

                if not isinstance(self.file_path, str):
                    raise TypeError("File path needs to be a string")

                if not re.match("", self.file_path):
                    raise ValueError("Provide a valid file name")

                if len(self.file_path) == 0:
                    raise ValueError("Provide a file path")

                if self.path_flag not in ["a", "r"]:
                    raise ValueError("Provide a valid flag (a or r)")

                if self.path_flag == "a":
                    if not os.path.exists(self.file_path):
                        raise FileNotFoundError("No file found")

                if self.path_flag == "r":
                    if not os.path.exists(f"{self.cwd}\\{self.file_path}"):
                        raise FileNotFoundError("No file found")

                if not isinstance(self.delimiter, str):
                    raise TypeError("Delimiter needs to be a string")

            except (TypeError, ValueError, FileNotFoundError) as e:
                print(e)

            else:
                break

        if self.path_flag == "a":
            return {"path": self.file_path, "sep": self.delimiter}
        else:
            return {"path": f"{self.cwd}\\{self.file_path}", "sep": self.delimiter}

    def export_file(self) -> None:
        """
        Export the resulting data as csv file
        """

        data = self.sanitize_file()

        try:
            if data is None:
                return
            else:
                with open(f"./{self.file_path.split('.')[0]}_san.csv", "x") as file:
                    file.write("".join(data))

        except FileExistsError as e:
            print(f"Cannot export: {e}")

    def run(self) -> None:
        self.init()
        self.get_params()
        self.export_file()


if __name__ == "__main__":
    CSVSanitizer(os.getcwd()).run()
