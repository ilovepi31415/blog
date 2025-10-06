class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props
    
    def to_html(self):
        raise NotImplementedError
    
    def props_to_html(self):
        prop_string = ''
        if self.props:
            for prop in self.props:
                prop_string += f' {prop}="{self.props[prop]}"'
        return prop_string

    def __repr__(self):
        return f'HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})'
        
class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, None, props)
    
    def to_html(self):
        if self.value is None:
            raise ValueError
        if self.tag is None:
            return self.value
        return f'<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>'
    
    def props_to_html(self):
        return super().props_to_html()

class ParentNode(HTMLNode):
    def __init__(self, tag, children: list[HTMLNode], props=None):
        super().__init__(tag, None, children, props)    

    def to_html(self):
        if self.tag is None:
            raise ValueError('ERROR: Missing tag')
        if self.children is None:
            raise ValueError('ERROR: Missing children')
        html_rep = ''
        html_rep += f'<{self.tag}{self.props_to_html()}>'
        for child in self.children:
            html_rep += child.to_html()
        html_rep += f'</{self.tag}>'
        return html_rep
    
    def props_to_html(self):
        return super().props_to_html()