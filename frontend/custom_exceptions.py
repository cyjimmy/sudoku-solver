class InvalidFileDataException(Exception):
    def __init__(self, filename):
        super().__init__(f"The data inside the file: {filename} is invalid. Please provide valid data.")
