from textnode import TextNode, TextType
from htmlnode import HTMLNode


def main():

    
    test = TextNode("This is some anchor text", TextType.LINK, "https://www.boot.dev")
    alt = TextNode("a different example", TextType.BOLD)
    extra = TextNode("This is some anchor text", TextType.LINK, "https:boot.dev")
    print(test)
    print(f"test and alt are equal: {test==alt}")
    print(f"test and extra are equal: {test==extra}")

    test = HTMLNode("the tag", "the value", None, {"href": "alink.com"})

    print(test)


if __name__ == "__main__":
    main()