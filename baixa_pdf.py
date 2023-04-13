def highlight(pdf, escopopo, nome):
    import fitz
    pdfIn = fitz.open(pdf)
    
    for page in pdfIn:
        text_instances = page.search_for(escopopo)
        # iterate through each instance for highlighting
        for inst in text_instances:
            annot = page.add_highlight_annot(inst)
            annot.update()
    pdfIn.save(f'{nome}.pdf')


def download_pdf(lnk, nome_arq=None, escopo=None):
    
    from selenium import webdriver
    from time import sleep
    import shutil
    import os
    import fitz

    index = lnk.find('jornal')
    extracted_url = lnk[index:]
    viewer_url = 'https://pesquisa.in.gov.br/imprensa/servlet/INPDFViewer?' + extracted_url + '&captchafield=firstAccess'
    ultimate_url = 'chrome-extension://mhjfbmdgcfjbbpaeojofohoefgiehjai/5719f1b3-e7b6-452b-a421-6a962570f4a5'
    current = 'C:\\Users\\gab36\\OneDrive\\Documentos\\Development\\FetchDOU\\'
    download_folder = "C:\\Users\\gab36\\OneDrive\\Documentos\\Development\\FetchDOU\\PDFs\\"

    options = webdriver.ChromeOptions()
    
    profile = {"plugins.plugins_disabled" : ["Chrome PDF Viewer", "INPDFViewer"],
               "download.default_directory": download_folder,
               "download.extensions_to_open": "",
               "plugins.always_open_pdf_externally": True}
    
    options.add_experimental_option("prefs", profile)
    options.add_argument("--disable-extensions")
    chromedriver = "C:\\webdrivers\\chromedriver.exe"
    driver = webdriver.Chrome(executable_path=chromedriver, options=options)

    print("Downloading file from link: {}".format(lnk))

    driver.get(viewer_url)
    sleep(1)
    driver.get(ultimate_url)
    sleep(3)
    print("Status: Download Complete.")
    

    files = os.listdir(download_folder)
    old_file = 'C:\\Users\\gab36\\OneDrive\\Documentos\\Development\\FetchDOU\\PDFs\\INPDFViewer.pdf'
    new_file = download_folder + (f'{nome_arq}.pdf')

    if len(files) == 1:
        # Rename first file if nome_arq argument is provided
        if nome_arq is not None:
            filename = min([download_folder + f for f in os.listdir(download_folder)],key=os.path.getctime)
            shutil.move(filename,os.path.join(download_folder,r"{}.pdf".format(nome_arq)))
        # Rename all existing files if there is more than one file

    elif len(files) > 1:
        os.rename(old_file,new_file)
    driver.close()

    highlight(new_file, escopo, nome_arq)

    


# pdfzao = "C:\\Users\\gab36\\OneDrive\\Documentos\\Development\\FetchDOU\\PDFs\\NATHALIA STEFANY DE ARAUJO UCHOA.pdf"

# download_pdf(pdfzao, 'jorge', 'NATHALIA STEFANY')
# def highlight(pdf, escopo):
#     import fitz
#     pdfIn = fitz.open(pdf)

#     for page in pdfIn:
#         print(page)
#         text_instances = page.search_for(escopo)
        

#         print(text_instances)  

#         # iterate through each instance for highlighting
#         for inst in text_instances:
#             annot = page.add_highlight_annot(inst)
#             annot.update()
#     pdfIn.save('Nath Barraqueira.pdf')


    ## HIGHLIGHTS ##




