from bs4 import BeautifulSoup


def open_html(link):
    from urllib.request import Request, urlopen
    from urllib.error import HTTPError
    from urllib.error import URLError

    req = Request(link, {})
    req.add_header('User-Agent', 'Chrome/102.0.5005.63')

    try:
        html = urlopen(req)
    except HTTPError as e:
        print(e)
    except URLError:
        print("Server down or incorrect domain")
    else:
        res = BeautifulSoup(html.read(), "html5lib")
        if res.title is None:
            print("Tag not found")
        else:
            print(res.title)

        with open("Data image/html.html", "w") as f:
            f.write(str(res))

        tags = res.find_all("div", class_="txtCenter")
        print(tags)
        for tag in tags:
            print(tag.getText())

def selenium_open(link):
    from selenium import webdriver

    options = webdriver.ChromeOptions()
    driver = webdriver.Chrome(executable_path="Data image\chromedriver.exe")
    #driver.close()
    driver.get(link)
    posts = driver.find_element_by_id("avisos")

    print(posts)
    with open("Data image/html.txt", "w") as f:
        f.write(str(posts.text))

    #driver = webdriver.Chrome("chromedriver.exe") # Baixe o Chrome WebDriver em https://c


if __name__ == "__main__":
    link = "http://nfe.sefaz.ba.gov.br/servicos/nfce/qrcode.aspx?p=29200303305734000177650010001716811461514181|2|1|1|3A48CE12C78B38AF6300F6724C8D68113E241569"
    #link = "http://nfe.sefaz.ba.gov.br/servicos/nfce/qrcode.aspx?p=29200303305734000177650010001716811461514181|2|1|1|3A48CE12C78B38AF6300F6724C8D68113E241569"
    link = "https://www.nfce.fazenda.sp.gov.br/qrcode?p=35220461412110045922650210001079881306923988|2|1|1|177fbf696a451eab2a28f146b42e0bfd397c5d15"
    #link = "https://portal.fazenda.sp.gov.br/_api/Web/Lists/getByTitle('Indices')/items?$Select=Title"
    #link = "https://www.python.org/"
    #open_html(link)

    selenium_open(link)
