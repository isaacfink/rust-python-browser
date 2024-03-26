from modules.urls import Url
from modules.html import HTML
from modules.browser import Browser


def main():
    print("Welcome to my browser")
    url_input: str = input("Enter a URL:\n")
    url = Url(url_input)
    body = url.request()
    html = HTML(body)
    browser = Browser(html.get_lines())
    browser.show()
    browser.start()


if __name__ == "__main__":
    main()
