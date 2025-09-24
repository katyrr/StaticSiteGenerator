from textnode import TextNode, TextType
from htmlnode import HTMLNode, ParentNode, LeafNode


def main():

    
    '''test = TextNode("This is some anchor text", TextType.LINK, "https://www.boot.dev")
    alt = TextNode("a different example", TextType.BOLD)
    extra = TextNode("This is some anchor text", TextType.LINK, "https:boot.dev")
    print(test)
    print(f"test and alt are equal: {test==alt}")
    print(f"test and extra are equal: {test==extra}")'''

    test = LeafNode("the tag", "the value", {"href": "alink.com"})

    print(test)


if __name__ == "__main__":
    main()