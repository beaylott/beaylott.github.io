#!/usr/bin/env python3

import os
import shutil
import datetime

import markdown
from jinja2 import Environment, FileSystemLoader, select_autoescape

header_html = """
<header>
    <nav>
        <ul>
            <li><a href="./index.html">Home</a> <a class="active" href="./about.html">About</a></li>
        </ul>
    </nav>
</header>
"""

footer_html = f'''
<footer>
    <p>©{datetime.datetime.now().strftime("%Y")} Ben Aylott. Last updated: {datetime.datetime.now().strftime("%d/%m/%Y")} | CSS by <a href="https://picocss.com">Pico</a></p>
</footer>
'''


templateLoader = FileSystemLoader(searchpath="./")
env = Environment(loader=templateLoader)
md = markdown.Markdown(extensions = ['meta'])

def generate_posts():

    posts_template = env.get_template("html/post.html")

    posts=[]

    for mdfile in os.listdir("posts"):
        if mdfile.endswith(".md"):
            with open(f"posts/{mdfile}", "r", encoding="utf-8") as input_file:
                body_html = md.convert(input_file.read())
            
            print(md.Meta)
            print(body_html)
            
            if md.Meta['title'][0] == None:
                print("ERROR: No title found in", mdfile)
                continue

            filename = f"{md.Meta['title'][0].replace(' ', '').lower()}.html"
            with open( f"output/{filename}", "w") as f:
                f.write(posts_template.render(footer=footer_html, header=header_html, title=md.Meta['title'][0], body=body_html))

            posts.append({
                'title': md.Meta['title'][0],
                'date': md.Meta['date'][0],
                'url': filename,
            })

    return posts

def generate_index(posts):
    index_template = env.get_template("html/index.html")
    with open("output/index.html", "w") as f:
        f.write(index_template.render(footer=footer_html, header=header_html, posts=posts))

def generate_about():
    about_template = env.get_template("html/about.html")
    with open("output/about.html", "w") as f:
        f.write(about_template.render(footer=footer_html, header=header_html))

if __name__ == "__main__":    
    shutil.rmtree('./output',ignore_errors=True)
    os.mkdir("./output")
    shutil.copyfile('html/pico.classless.min.css','output/pico.classless.min.css')
    generate_about()
    posts=generate_posts()
    generate_index(posts)
    
    