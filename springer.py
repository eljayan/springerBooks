import requests
import bs4
import os
import re
from bookLinks import LINKS
import Tkinter as tk
from tkFileDialog import askdirectory

from pdfminer.high_level import extract_text

headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:68.0) Gecko/20100101 Firefox/68.0'}
PROXIES = {
    "http": "http://r00715649:Huawei%3F3@proxy.huawei.com:8080",
    "https": "http://r00715649:Huawei%3F3@proxy.huawei.com:8080"
}

def main():

    f= select_folder()
    if not f:
        raw_input("No se ha seleccionado ninguna carpeta")
        return

    n=1
    t= len(LINKS)

    for l in LINKS:
        print "Descargando archivo {} de {}".format(n, t)
        donwloadLink(l, f)
        n+=1

    raw_input("Proceso completado.")
    return


def readSrpingerFile(filepath):
    pat = re.compile(r"http://link.springer.com/openurl.*", re.IGNORECASE)
    t= extract_text(filepath)
    links = pat.findall(t)
    return links


def donwloadLink(url, saveDir):

    page = requests.get(url, headers=headers, verify=False)
    soup = bs4.BeautifulSoup(page.text, "html.parser")

    title = soup.find("h1").text
    savepath = os.path.join(saveDir, title+".pdf")

    fileATag = soup.find("a", {"title":"Download this book in PDF format"})
    if not fileATag:
        return

    fileRelativeURL = fileATag["href"]

    fileUrl = "https://link.springer.com" + fileRelativeURL

    print "Descargando: " + title

    return downloadFile(fileUrl, savepath)



def downloadFile(fileUrl, savepath):
    r = requests.get(fileUrl, headers=headers, proxies=PROXIES, verify=False, stream=True)

    if r.status_code == 200:
        with open(savepath, "wb") as f:
            for chunk in r.iter_content(chunk_size=128):
                f.write(chunk)
        return True


def select_folder():
    root = tk.Tk()
    root.withdraw()
    fold= askdirectory(title="Seleccione carpeta de destino:")
    return fold

if __name__ == '__main__':
    #donwloadLink("https://link.springer.com/book/10.1007%2F978-3-642-55309-7", "Books/")
    #print downloadFile("https://link.springer.com/content/pdf/10.1007%2F978-3-642-55309-7.pdf","Books/test.pdf" )
    #print readSrpingerFile("D:/myScripts/SpringerLink/Springer Ebooks.pdf")
    main()