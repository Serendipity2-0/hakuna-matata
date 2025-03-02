# organize the desktop
# moves images, videos, screenshots, and audio files
# into corresponding folders
import os
import shutil


audio = (
    ".3ga",
    ".aac",
    ".ac3",
    ".aif",
    ".aiff",
    ".alac",
    ".amr",
    ".ape",
    ".au",
    ".dss",
    ".flac",
    ".flv",
    ".m4a",
    ".m4b",
    ".m4p",
    ".mp3",
    ".mpga",
    ".ogg",
    ".oga",
    ".mogg",
    ".opus",
    ".qcp",
    ".tta",
    ".voc",
    ".wav",
    ".wma",
    ".wv",
)

video = (".webm", ".MTS", ".M2TS", ".TS", ".mov", ".mp4", ".m4p", ".m4v", ".mxf")

img = (
    ".jpg",
    ".jpeg",
    ".jfif",
    ".pjpeg",
    ".pjp",
    ".png",
    ".gif",
    ".webp",
    ".svg",
    ".apng",
    ".avif",
)

pdf = ".pdf"

excel = (".xlsx", ".xls", ".xlsm", ".csv")

markdown = ".md"


def is_audio(file):
    return os.path.splitext(file)[1] in audio


def is_video(file):
    return os.path.splitext(file)[1] in video


def is_image(file):
    return os.path.splitext(file)[1] in img


def is_screenshot(file):
    name, ext = os.path.splitext(file)
    return (ext in img) and "screenshot" in name.lower()


def is_pdf(file):
    return os.path.splitext(file)[1] in pdf


def is_excel(file):
    return os.path.splitext(file)[1] in excel

def is_markdown(file):
    return os.path.splitext(file)[1] in markdown


# Create destination folders if they don't exist
folders = ["AudioFiles", "Videos", "Images", "PDFFiles", "ExcelFiles", "MarkdownFiles"]
for folder in folders:
    folder_path = f"/Users/omkar/Downloads/{folder}"
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

os.chdir("/Users/omkar/Downloads")

for file in os.listdir():
    if is_audio(file):
        shutil.move(file, "/Users/omkar/Downloads/AudioFiles")
    elif is_video(file):
        shutil.move(file, "/Users/omkar/Downloads/Videos")
    elif is_image(file):
        shutil.move(file, "/Users/omkar/Downloads/Images")
    elif is_pdf(file):
        shutil.move(file, "/Users/omkar/Downloads/PDFFiles")
    elif is_excel(file):
        shutil.move(file, "/Users/omkar/Downloads/ExcelFiles")
    elif is_markdown(file):
        shutil.move(file, "/Users/omkar/Downloads/MarkdownFiles")
    else:
        print(f"Unknown file type: {file}")
        pass
