#!/usr/bin/env python3

from io import TextIOWrapper
from bs4 import BeautifulSoup
import re
import argparse

DEFAULT_TEMPLATE = "template.html"
DEFAULT_OUTPUT = "gen.html"
DEFAULT_INPUT = "input.txt"


class Section:
    """
    Parsed section of text.
    OOP isn't really necessary for this, but it does make it slightly easier.
    """

    def __init__(self, type: str, content: str, id: int):
        self.type = type
        self.content = content
        self.id = id
        self.slide = None
        self.image = None
        self.find_image_links()

        if type == "title":
            # *_ gathers the other lines and discards them, only the first two are needed
            # functional programming thing
            (title, sub_title, *_) = self.content.splitlines()
            title_card = title_card_factory(title, sub_title, self.image)
            self.slide = slide_factory(title_card, self.id, ["title_card"])
        else:
            # *rest retrieves every line other than the first one
            (title, *rest) = self.content.splitlines()
            new_content = "\n".join(rest)
            text_card = text_card_factory(title, new_content, self.image)
            self.slide = slide_factory(text_card, self.id, ["text_card"])

    def find_image_links(self):
        """
        Finds the first image link and sets this objects image attribute to it.
        """
        image_pattern = re.compile(r"!\[\]\((.*?)\)")
        image_links = re.findall(image_pattern, self.content)
        if image_links:
            self.content = re.sub(image_pattern, r"", self.content)
            self.image = image_links[0]


def title_card_factory(title: str, sub_title: str, image_link: str = ""):
    """
    For creating title card HTML.

    Args:
        title (str): Title on the title card.
        sub_title (str): The subtitle below the title card.
        image_link (str, optional): The image on the title card. Defaults to "".

    Returns:
        _type_: the Beautifulsoup title card tag.
    """
    soup = BeautifulSoup()
    title_tag = soup.new_tag("h1", **{"class": "center"})
    title_tag.string = title
    tiny_tag = soup.new_tag("h2", **{"class": "center"})
    tiny_tag.string = sub_title

    card_tag = soup.new_tag("div")

    if image_link:
        image_tag = soup.new_tag("img", **{"class": "center_img", "src": image_link, "style": "max-height: 400px;"})
        card_tag.append(image_tag)
    card_tag.append(title_tag)
    card_tag.append(tiny_tag)
    return card_tag


def text_card_factory(title: str, content: str, image_link: str = ""):
    """
    Factory for text cards (the normal cards seen).

    Args:
        title (str): Title for the text card.
        content (str): The text content of the card, the meat of it. Automatically formats lines into a list.
        image_link (str, optional): The image on the slide. Defaults to "".

    Returns:
        _type_: the Beautifulsoup text card tag.
    """
    soup = BeautifulSoup()
    card_tag = soup.new_tag("div")
    title_tag = soup.new_tag("h1")
    title_tag.string = title

    fixed_content = "<ul>"
    for line in content.splitlines():
        fixed_content += "<li>" + line + "</li>"
    fixed_content += "</ul>"
    text_tag = BeautifulSoup(fixed_content, "html.parser")

    card_tag = soup.new_tag("div")

    card_tag.append(title_tag)
    content_table_tag = soup.new_tag("table")
    table_row = soup.new_tag("tr")

    text_table_data = soup.new_tag("td")
    text_table_data.append(text_tag)

    table_row.append(text_table_data)
    if image_link:
        # so that it correctly shares space with the image
        text_table_data["width"] = "50%"
        image_tag = soup.new_tag(
            "img", **{"class": "center", "src": image_link, "width": "50%"}
        )
        img_td = soup.new_tag("td")
        img_td.append(image_tag)
        table_row.append(img_td)

    content_table_tag.append(table_row)

    card_tag.append(content_table_tag)
    return card_tag


def slide_factory(tag, id: int, classes: list = []):
    """
    Factory for creating slides from a given Beautifulsoup tag, id, and list of classes to use for the slide.

    Args:
        tag (_type_): The tag to put into the slide.
        id (int): The id of the slide (used for the Javascript on the page).
        classes (list, optional): What classes should be on the HTML of the slide tag. Defaults to [].

    Returns:
        _type_: The Beautifulsoup slide tag.
    """
    soup = BeautifulSoup()
    slide = soup.new_tag(
        "div", **{"class": "slide " + " ".join(classes), "id": "slide{}".format(id)}
    )
    slide.append(tag)
    return slide


def read_section(fp: TextIOWrapper, id: int) -> Section:
    """
    Parses/Reads a section of the given file pointer, and associates it with a given id.

    Args:
        fp (TextIOWrapper): The file pointer to read the section from.
        id (int): The id of this section.

    Returns:
        Section: An initalized and filled in Section object.
    """
    section_type_pattern = re.compile(r"^%(.*)$")
    section_type = section_type_pattern.findall(fp.readline())
    if len(section_type) == 0:
        return None

    section_type = section_type[0]

    content = ""
    line = fp.readline()
    # checks the line's not empty, or just a space, or just a newline
    while line not in ["\r\n", "\n", " ", ""]:
        content += line
        line = fp.readline()

    return Section(section_type, content, id)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", "-i", default=DEFAULT_INPUT)
    parser.add_argument("--template", "-t", default=DEFAULT_TEMPLATE)
    parser.add_argument("--output", "-o", default=DEFAULT_OUTPUT)
    args = vars(parser.parse_args())
    with open(args["template"], "r") as fp:
        soup = BeautifulSoup(fp, "html.parser")

    with open(args["input"], "r") as fp:
        id = 0
        while new_section := read_section(fp, id):
            soup.find("body").append(new_section.slide)
            id += 1

    with open(args["output"], "w") as fp:
        fp.write(str(soup))
