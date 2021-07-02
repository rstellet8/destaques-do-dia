from selenium import webdriver
from time import sleep
import pandas as pd


WEBDRIVER_PATH = "D:/Python/webdriver/chromedriver.exe"
URL = "https://www.infomoney.com.br/ferramentas/altas-e-baixas/"


def getDestaques(URL=URL, WEBDRIVER_PATH=WEBDRIVER_PATH):
    driver = webdriver.Chrome(WEBDRIVER_PATH)
    driver.get(URL)


    raw_header1 = driver.find_element_by_css_selector("#altas_e_baixas > thead").text.split(" ")

    raw_header2 = [
        raw_header1[0], 
        raw_header1[1],
        " ".join(raw_header1[2:4]),     
        " ".join(raw_header1[4:7]),     
        " ".join(raw_header1[7:10]),     
        " ".join(raw_header1[10:13]),     
        " ".join(raw_header1[13:16]),     
        " ".join(raw_header1[16:19]),     
        " ".join(raw_header1[19:21]),     
        " ".join(raw_header1[21:23]),     
        raw_header1[23]     
    ]


    counter = 0
    while True:
        counter += 1
        txt = driver.find_element_by_css_selector("#altas_e_baixas > tbody").text.split("\n")
        if txt[0] != 'Carregando...':
            break

        if counter >= 10:
            raise TimeoutError(f"Incapaz de carregar os dados, consulte a disponibilidade de: {URL}")

        sleep(1)


    def cleanElement(driver):
        ftxt = []
        for i in txt:
            i = i.split(" ")
            i[-2] = i[-2] + " " + i[-1]
            i.pop()
            ftxt.append(i)

        return ftxt

    def add_line(dataFrame, line):
        return dataFrame.append(pd.Series(line, index=dataFrame.columns), ignore_index=True)


    df = pd.DataFrame(columns=raw_header2)

    for i in cleanElement(txt):
        df = add_line(df, i)

    for col in df.iloc[:, 2:-1].columns:
        df[col] = df[col].apply(lambda x: x.replace(",", "."))
        df[col] = pd.to_numeric(df[col], errors="coerce")

    df = df.sort_values(by="VAR. DIA (%)", ascending=False)


    df = df.head().append(df.tail())
    df.to_excel("DestaquesDoDia.xlsx", index=False)

if __name__ == "__main__":
    getDestaques()
