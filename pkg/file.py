from uuid import uuid4


def change_filename(filename: str) -> str:
    return f"{uuid4()}.{filename.split('.')[-1]}"
