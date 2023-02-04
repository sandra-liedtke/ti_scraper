import re


# regex for headline between span tags
HEADLINE_SPAN = re.compile(r'<span class="article-title">(.*?)</span>')
#headline for headline between div tags
HEADLINE_HEADER = re.compile(r'<header>(.*?)<header>')
#headline for headline with h1-h9 tags
HEADLINE_H1 = re.compile(r'<h[0-9].*?>(.*?)</h[0-9]>')
#headline for headline between div tags
HEADLINE_DIV = re.compile(r'<div.*?>(.*?)</div>')