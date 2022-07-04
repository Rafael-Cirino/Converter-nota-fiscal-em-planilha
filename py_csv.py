import csv

import os
from dotenv import load_dotenv

load_dotenv()

PATH_TESSERACT = os.getenv("PATH_TESSERACT")
PAST_DATA = os.getenv("PAST_DATA")


def isNumber(n):
    try:
        float(n)
    except ValueError:
        return False

    try:
        int(n)
    except ValueError:
        return False

    return True


def write_csv(data):
    # with open(PAST_DATA + "sheet/test.csv", mode="w") as csv_file:
    #   writer = csv.writer(csv_file)

    with open(
        PAST_DATA + "sheet/test.csv", newline="", encoding="utf-8", mode="w"
    ) as csv_file:
        csv_config = csv.writer(
            csv_file, delimiter=",", quotechar='"', quoting=csv.QUOTE_MINIMAL
        )

        for key in data.keys():

            if key == "product":
                csv_config.writerow([""])
                csv_config.writerow(
                    ["Product", "quantity", "unitary value", "total product value"]
                )

                for key_product in data["product"].keys():
                    list_write = []
                    for key_name in data["product"][key_product].keys():
                        value = data["product"][key_product][key_name]
                        if isNumber(value):
                            list_write.append(value)
                        else:
                            list_write.append(value.replace("\n", " "))

                    csv_config.writerow(list_write)

                csv_config.writerow([""])
            else:
                value = data[key]
                if isNumber(value):
                    csv_config.writerow([key, data[key]])
                else:
                    csv_config.writerow([key, data[key].replace("\n", " ")])
                


if __name__ == "__main__":
    t1 = {
        "store": "drogaria sao paulo sa",
        "CNPJ": "cnpj: 61.412.110/0459-22 av jose maria marques de oliveira , 538 ,",
        "product": {
            "lenco papel sof c 50": {
                "name": "lenco papel sof c 50",
                "qtde": 1,
                "vl_unit": 5.19,
                "vl_total": 5.19,
            },
            "soro ever b d 500ml\n": {
                "name": "soro ever b d 500ml\n",
                "qtde": 1,
                "vl_unit": 7.69,
                "vl_total": 7.69,
            },
        },
        "amount": 12.88,
        "qtde_itens": 2,
        "amount_pay": 12.88,
        "discount": 0.0,
        "payment": "\ndinheiro",
        "value_payment": 12.88,
        "transshipment": 0.0,
        "taxation": 5.64,
    }

    write_csv(t1)