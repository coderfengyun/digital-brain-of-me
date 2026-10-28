from html.parser import HTMLParser
from pathlib import Path


class ArticleText(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.in_article = False
        self.depth = 0
        self.skip = 0
        self.out = []

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == "article" and "content" in attrs.get("class", "").split():
            self.in_article = True
            self.depth = 1
            return
        if not self.in_article:
            return
        self.depth += 1
        if tag in {"script", "style", "button"}:
            self.skip += 1
        if self.skip:
            return
        if tag == "h2": self.out.append("\n## ")
        elif tag == "h3": self.out.append("\n### ")
        elif tag in {"p", "figure", "table", "pre"}: self.out.append("\n")
        elif tag == "li": self.out.append("\n- ")
        elif tag == "br": self.out.append("\n")
        elif tag in {"td", "th"}: self.out.append(" | ")

    def handle_endtag(self, tag):
        if not self.in_article:
            return
        if tag in {"script", "style", "button"} and self.skip:
            self.skip -= 1
        if not self.skip and tag in {"h2", "h3", "p", "figure", "table", "pre", "li"}:
            self.out.append("\n")
        self.depth -= 1
        if tag == "article" and self.depth == 0:
            self.in_article = False

    def handle_data(self, data):
        if self.in_article and not self.skip:
            text = " ".join(data.split())
            if text:
                self.out.append(text + " ")


src = Path("knowledge/ai/20261028-on-policy-distillation/paper.html")
dst = Path("knowledge/ai/20261028-on-policy-distillation/source.md")
p = ArticleText()
p.feed(src.read_text())
text = "".join(p.out)
while "  " in text:
    text = text.replace("  ", " ")
while "\n\n\n" in text:
    text = text.replace("\n\n\n", "\n\n")
header = "# On-Policy Distillation\n\nAuthor: Kevin Lu with Thinking Machines Lab\n\nPublished: 2025-10-27\n\nSource: https://thinkingmachines.ai/blog/on-policy-distillation/\n\n"
dst.write_text(header + text.strip() + "\n")
