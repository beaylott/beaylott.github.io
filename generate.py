#!/usr/bin/env python3

import os
import shutil
import datetime
import xml.etree.ElementTree as ET
import markdown
from jinja2 import Environment, FileSystemLoader

header_html = """
<header>
    <nav>
        <ul>
            <li><a href="./index.html">Home</a></li>
            <li><a href="./about.html">About</a></li>
            <li><a href="./atom.xml">Feed</a></li>
        </ul>
    </nav>
</header>
"""

footer_html = f"""
<footer>
    <p>©{datetime.datetime.now().strftime("%Y")} Ben Aylott. Last updated: {datetime.datetime.now().strftime("%d/%m/%Y")} | CSS by <a href="https://picocss.com">Pico</a></p>
</footer>
"""

templateLoader = FileSystemLoader(searchpath="./")
env = Environment(loader=templateLoader)
md = markdown.Markdown(extensions=["meta"])


def generate_posts():
    posts_template = env.get_template("html/post.html")

    posts = []

    for mdfile in os.listdir("posts"):
        if mdfile.endswith(".md"):
            with open(f"posts/{mdfile}", "r", encoding="utf-8") as input_file:
                body_html = md.convert(input_file.read())

            if md.Meta["title"][0] is None:
                print("ERROR: No title found in", mdfile)
                continue

            filename = f"{md.Meta['title'][0].replace(' ', '').lower()}.html"
            with open(f"output/{filename}", "w") as f:
                f.write(
                    posts_template.render(
                        footer=footer_html,
                        header=header_html,
                        title=md.Meta["title"][0],
                        body=body_html,
                    )
                )

            posts.append(
                {
                    "title": md.Meta["title"][0],
                    "date": md.Meta["date"][0],
                    "url": filename,
                }
            )

    return posts


def generate_index(posts):
    index_template = env.get_template("html/index.html")
    with open("output/index.html", "w") as f:
        f.write(
            index_template.render(footer=footer_html, header=header_html, posts=posts)
        )


def generate_about():
    about_template = env.get_template("html/about.html")
    with open("output/about.html", "w") as f:
        f.write(about_template.render(footer=footer_html, header=header_html))


atom_topmatter = """
<?xml version="1.0" encoding="utf-8"?>
"""


def generate_posts_feed_atom(posts):
    xml = ET.Element("feed")
    xml.set("xmlns", "http://www.w3.org/2005/Atom")
    title = ET.SubElement(xml, "title")
    title.text = "1d2f0.info"
    link = ET.SubElement(xml, "link")
    link.set("href", "https://1d2f0.info/atom.xml")
    link.set("rel", "self")
    updated = ET.SubElement(xml, "updated")
    updated.text = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")
    author = ET.SubElement(xml, "author")
    name = ET.SubElement(author, "name")
    name.text = "Ben Aylott"
    id = ET.SubElement(xml, "id")
    id.text = "https://1d2f0.info/"

    for post in posts:
        entry = ET.SubElement(xml, "entry")
        title = ET.SubElement(entry, "title")
        title.text = post["title"]
        link = ET.SubElement(entry, "link")
        link.set("href", "https://1d2f0.info/" + post["url"])
        updated = ET.SubElement(entry, "updated")
        updated.text = datetime.datetime.strptime(post["date"], "%Y-%m-%d").strftime(
            "%Y-%m-%dT%H:%M:%SZ"
        )
        id = ET.SubElement(entry, "id")
        id.text = "https://1d2f0.info/" + post["url"] + "/"
    print(ET.tostring(xml))
    et = ET.ElementTree()
    et._setroot(xml)
    ET.indent(et, space="\t", level=0)
    et.write("output/atom.xml", encoding="utf-8", xml_declaration=True)


if __name__ == "__main__":
    shutil.rmtree("./output", ignore_errors=True)
    os.mkdir("./output")
    shutil.copyfile(
        "third-party/pico.classless.min.css", "output/pico.classless.min.css"
    )
    shutil.copyfile("habits.png", "output/habits.png")
    generate_about()
    posts = generate_posts()
    generate_posts_feed_atom(posts)
    generate_index(posts)
