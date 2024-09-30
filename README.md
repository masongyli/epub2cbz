Convert an epub file to a cbz file

What it does is simply extract all images from the epub file and compress them into a zip file with the extension changed to cbz.


# Installation
Cd into the project folder and execute
```
mkdir .venv
pipenv install
```
Then all dependencies would be installed in .venv folder

# Usage
```
pipenv run python3 main.py path/to/epub_file.epub
```

Then it would create a cbz file at path/to/epub_file.cbz
