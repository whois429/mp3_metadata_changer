import logging
from pathlib import Path

import eyed3

INPUT_FOLDER = "input"
DELIMITER = " - "
LOGGING_LEVEL = logging.INFO

logging.basicConfig(level=LOGGING_LEVEL, format="%(levelname)s | %(message)s")


def change_metadata_for_file(file: Path) -> None:
    audio = eyed3.load(file)
    audio.initTag(version=(2, 3, 0))

    imagedata = ""
    for image in Path(f"{Path.cwd()}/{INPUT_FOLDER}").iterdir():
        if all([
                str(image).endswith((".png", ".jpg", ".jpeg")),
                image.stem == file.stem
            ]):
            with open(image, "rb") as image_file:
                imagedata = image_file.read()
            break

    if imagedata:
        audio.tag.images.set(3, imagedata, "image/jpeg", "cover")

    audio.tag.artist = file.stem.split(DELIMITER)[0].strip()
    audio.tag.title = file.stem.split(DELIMITER)[-1].strip()

    audio.tag.save()
    logging.info("'%s' is completed!\n", file.stem)


def change_metadata_for_files(folder: Path) -> None:
    logging.info("Album '%s':", folder.stem)
    imagedata = ""
    for image in folder.iterdir():
        if all([
                str(image).endswith((".png", ".jpg", ".jpeg")),
                image.stem == folder.stem
            ]):
            with open(image, "rb") as image_file:
                imagedata = image_file.read()
                break

    for item in folder.iterdir():
        if str(item).endswith(".mp3"):
            audio = eyed3.load(item)
            audio.initTag(version=(2, 3, 0))

            if imagedata:
                audio.tag.images.set(3, imagedata, "image/jpeg", "cover")

            audio.tag.artist = item.stem.split(DELIMITER)[0].strip()
            audio.tag.title = item.stem.split(DELIMITER)[-1].strip()
            audio.tag.album = folder.stem

            audio.tag.save()
            logging.info("'%s' is completed!", item.stem)


def get_input_data() -> None:
    for item in Path(f"{Path.cwd()}/{INPUT_FOLDER}").iterdir():
        if item.is_dir():
            change_metadata_for_files(item)
        elif all([item.is_file(), str(item).endswith(".mp3")]):
            change_metadata_for_file(item)


def main() -> None:
    get_input_data()


if __name__ == "__main__":
    main()
