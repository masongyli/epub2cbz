import re
from io import BytesIO
from pathlib import Path
import shutil
import zipfile
import sys

import ebooklib
from ebooklib import epub
from PIL import Image
from bs4 import BeautifulSoup


if __name__ == '__main__':
    # get the first arguement as the epub file
    epub_path = sys.argv[1]
    output_dir = sys.argv[1].split('.')[0]

    epub_object = epub.read_epub(epub_path)

    if not Path(output_dir).exists():
        Path(output_dir).mkdir()

    # cannot use epub_object.get_items_of_type(ebooklib.ITEM_IMAGE)
    # because it doesn't return image items in appearance order

    count = 1
    for document in epub_object.get_items_of_type(ebooklib.ITEM_DOCUMENT):
        html_str = str(document.get_content())
        soup = BeautifulSoup(html_str, 'html.parser')
        for img in soup.find_all('img'):
            img_href = img.get('src')

            if img_href is None:
                continue

            img_href = re.sub('\\.\\./', '', img_href) # remove '../'
            image_item = epub_object.get_item_with_href(img_href)

            if image_item is None:
                continue
            
            with Image.open(BytesIO(image_item.get_content())) as im:
                img_name = str(count).zfill(6) + '.' + img_href.split('.')[-1]
                # im.show()
                im.save(Path(output_dir) / img_name)
                count += 1

    with zipfile.ZipFile(output_dir + '.cbz', 'w') as z:
        for file in Path(output_dir).iterdir():
            z.write(file)
    
    # remove the folder output_dir
    shutil.rmtree(output_dir)
