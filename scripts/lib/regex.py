import re


# regex for headline between span tags
HEADLINE_SPAN = re.compile(r'<span class="article-title">(.*?)</span>|<img alt=.*?/>')
# regex for headline between header tags
HEADLINE_HEADER = re.compile(r'<header>(.*?)<header>')
# regex for headline with h1-h9 tags
HEADLINE_H1 = re.compile(r'<h[0-9].*?>(.*?)</h[0-9]>')
# regex for headline between div tags
HEADLINE_DIV = re.compile(r'<div.*?>(.*?)</div>')
# regex for headline between a tags
HEADLINE_A = re.compile(r'<a .*?>(.*?)</a>')

# regex to remove scripts, all tags and all duplicate empty spaces
ALL_HTML = re.compile(r'<script.+?</script>|<.*?>|</.*?>|[ ]{2,5}', flags=re.DOTALL)
# regex for all escape characters if they are duplicate
ESCAPE = re.compile(r'\n{2,10}|\r{2,10}|\t')