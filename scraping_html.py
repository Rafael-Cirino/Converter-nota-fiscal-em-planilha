from bs4 import BeautifulSoup
import regex


def open_html(link):
    from urllib.request import Request, urlopen
    from urllib.error import HTTPError
    from urllib.error import URLError

    req = Request(link, {})
    req.add_header("User-Agent", "Chrome/102.0.5005.63")

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
    options.add_experimental_option("detach", False)
    driver = webdriver.Chrome(
        chrome_options=options, executable_path="Data image\chromedriver.exe"
    )
    # driver = webdriver.Chrome(chrome_options=options, executable_path=r'C:\WebDrivers\chromedriver.exe')
    # driver.close()
    driver.get(link)
    html = driver.page_source

    # print(posts.text)

    res = BeautifulSoup(html, "lxml")
    if res.title is None:
        print("Tag not found")
    else:
        print("\n")  # print(res.title)

    with open("Data image/html.html", "w") as f:
        f.write(str(res))

    # print(tags)
    # Versão melhor, mas não consistente

    list_out = []
    tags = res.find("div", {"id": "conteudo"})
    with open("Data image/html2.txt", "w") as f:
        for tag in tags:
            line = str(tag.text).replace("\t", "").lower()
            f.write(line)
            list_out.append(line.split("\n\n\n"))

    dict_conteudo(list_out[3:])

    # driver = webdriver.Chrome("chromedriver.exe") # Baixe o Chrome WebDriver em https://c


def dict_conteudo(list_conteudo):
    dict_out = {}

    header = list_conteudo[0][0].split("\n\n")
    dict_out["store"] = header[0].replace("\n", "")
    dict_out["CNPJ"] = header[1].replace("\n", " ")
    dict_out["product"] = {}

    # Extraindo os produtos da nota
    amount = 0
    for item in list_conteudo[3]:
        if item != "":
            if regex.search(r"código", item):
                product = item.split("\n(código")
                name = product[0].replace("\n", "", 1)
                dict_out["product"][name] = {}
                dict_out["product"][name]["name"] = name

            elif regex.search(r"qtde", item):
                product = item.split("\n\n")
                qtde = product[0].replace("\n", "", 1).replace("qtde.:", "", 1)
                vl_unit = (
                    product[2]
                    .replace("vl. unit.:\n\xa0\n", "", 1)
                    .replace("vl. unit.:\xa0", "", 1)
                    .replace(",", ".")
                )

                value_product = float(vl_unit) * int(qtde)
                amount += value_product

                dict_out["product"][name]["qtde"] = int(qtde)
                dict_out["product"][name]["vl_unit"] = float(vl_unit)
                dict_out["product"][name]["vl_total"] = value_product

    dict_out["amount"] = amount
    for i, value in enumerate(list_conteudo[5]):
        if value != "":
            if regex.search(r"total de itens", value):
                product = value.split("\n")
                dict_out["qtde_itens"] = int(product[3])

            elif regex.search(r"pagar", value):
                product = value.split("\n")

                dict_out["amount_pay"] = float(product[1].replace(",", "."))
                dict_out["discount"] = amount - float(product[1].replace(",", "."))

            elif regex.search(r"forma de", value):
                product = list_conteudo[5][i + 1].split("\n\n")
                dict_out["payment"] = product[0]
                dict_out["value_payment"] = float(product[1].replace(",", "."))
                # troco
                dict_out["transshipment"] = float(product[1].replace(",", ".")) - dict_out["amount_pay"]

            elif regex.search(r"tributos totais", value):
                product = value.split("\xa0r$\n")
                dict_out["taxation"] = float(
                    product[1].replace("\n\n", "").replace(",", ".")
                )

    print(dict_out)
    return


if __name__ == "__main__":
    link = "http://nfe.sefaz.ba.gov.br/servicos/nfce/qrcode.aspx?p=29200303305734000177650010001716811461514181|2|1|1|3A48CE12C78B38AF6300F6724C8D68113E241569"

    link2 = "https://www.nfce.fazenda.sp.gov.br/qrcode?p=35220461412110045922650210001079881306923988|2|1|1|177fbf696a451eab2a28f146b42e0bfd397c5d15"
    # link = "https://portal.fazenda.sp.gov.br/_api/Web/Lists/getByTitle('Indices')/items?$Select=Title"
    # link = "https://www.python.org/"
    # open_html(link)

    selenium_open(link)
    selenium_open(link2)

    list_teste = [
        [
            "\nDROGARIA SAO PAULO SA\n\nCNPJ:\n61.412.110/0459-22\nAV JOSE MARIA MARQUES DE OLIVEIRA\n,\n538\n,\n\n,\nVILA NORMA\n,\nSalto\n,\nSP\n"
        ],
        ["\n"],
        ["Clear text"],
        [
            "",
            "LENCO PAPEL SOF C 50\n\n(Código :\n80900\n)",
            "\nQtde.:1\n\nUN: UN\n\nVl. Unit.:\n\xa0\n5,19",
            "Vl. Total\n5,19",
            "\nSORO EVER B D 500ML\n\n(Código:\n719587\n)",
            "\nQtde.:1\n\nUN: UN\n\nVl. Unit.:\n\xa0\n7,69",
            "Vl. Total\n7,69\n\n",
        ],
        ["\n"],
        [
            "\n\nQtd. total de itens:\n2",
            "Valor a pagar R$:\n12,88",
            "Forma de pagamento:\nValor pago R$:",
            "\nDinheiro\n\n12,88",
            "Troco \nNaN",
            "Informação dos Tributos Totais Incidentes\n(Lei Federal 12.741/2012)\xa0R$\n5,64\n\n",
        ],
        ["\n"],
    ]

    list_teste2 = [
        [
            "\nmagalhaes araujo medicamentos ltda\n\n    cnpj:\n    03.305.734/0001-77\nrua conde de porto alegre, \n208,\n,\niapi,\nsalvador,\nba\n"
        ],
        ["\n"],
        ["clear text"],
        [
            "",
            "gelo-bio aer 60ml\n(código: 21667)",
            "qtde.:1\n\nun: un\n\nvl. unit.:\xa032,79\n\nvl. total32,79",
            "\nviter c 1gr 10cpr\n(código: 36405)",
            "qtde.:1\n\nun: un\n\nvl. unit.:\xa024,3\n\nvl. total24,30",
            "\nlufbem gts 15ml\n(código: 77658)",
            "qtde.:1\n\nun: un\n\nvl. unit.:\xa024,93\n\nvl. total24,93",
            "\nmaxalgina 500mg/ml gts 10ml\n(código: 11855)",
            "qtde.:1\n\nun: un\n\nvl. unit.:\xa09,66\n\nvl. total9,66\n\n",
        ],
        ["\n"],
        [
            "\n\nqtd. total de itens:\n4",
            "valor total r$:\n91,68",
            "descontos r$:\n71,82",
            "valor a pagar r$:\n19,86",
            "forma de pagamento:\nvalor pago r$:",
            "\n4 - cartão de débito\n\n19,86\n\n",
        ],
        ["\n"],
    ]

    # dict_conteudo(list_teste)
