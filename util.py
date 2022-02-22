import pathlib


def save_text_to_file(filename, text):
    try:
        with open(filename, 'w', encoding="utf-8") as f:
            f.write(text)
    except FileNotFoundError:
        directory = '/'.join(filename.split("/")[:-1])
        pathlib.Path(directory).mkdir(parents=True, exist_ok=True)
        with open(filename, 'w') as f:
            f.write(text)
