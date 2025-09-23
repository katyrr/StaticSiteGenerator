from textnode import TextNode, TextType


def main():

    test = TextNode("This is some anchor text", TextType.LINK, "https://www.boot.dev")
    alt = TextNode("a different example", TextType.BOLD)
    extra = TextNode("This is some anchor text", TextType.IMAGE, "https://www.boot.dev")
    print(test)
    print(f"test and alt are equal: {test==alt}")
    print(f"test and extra are equal: {test==extra}")


if __name__ == "__main__":
    main()