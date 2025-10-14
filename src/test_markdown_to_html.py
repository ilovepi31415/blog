import unittest
from markdown_to_html import *

class test_markdown_to_html(unittest.TestCase):
    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_codeblock(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )

    def test_quote(self):
        md = """
>This is text that _should_ remain
>the **same** even with inline stuff
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><blockquote>This is text that <i>should</i> remain\nthe <b>same</b> even with inline stuff</blockquote></div>",
        )
    
    def test_ol(self):
        md = """
- This is text that _should_ remain
- the **same** even with inline stuff
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ol><li>This is text that <i>should</i> remain</li><li>the <b>same</b> even with inline stuff</li></ol></div>",
        )
    
    def test_heading(self):
        md = """
### This is text that _should_ remain
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h3>This is text that <i>should</i> remain</h3></div>",
        )
    
