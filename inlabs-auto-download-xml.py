import datetime
import requests
import zipfile
import os
import warnings
import config as cf

login = cf.login
senha = cf.senha

tipo_dou = "DO2"  # Seções separadas por espaço
# Opções DO1 DO2 DO3 DO1E DO2E DO3E

url_login = "https://inlabs.in.gov.br/logar.php"
url_download = "https://inlabs.in.gov.br/index.php?p="
warnings.filterwarnings(
    "ignore", category=requests.packages.urllib3.exceptions.InsecureRequestWarning
)

directory_FETCH = "C:\\Users\\gab36\\OneDrive\\Documentos\\Development\\FetchDOU\\"

payload = {"email": login, "password": senha}
headers = {
    "Content-Type": "application/x-www-form-urlencoded",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
}

s = requests.Session()


def download():
    if s.cookies.get("inlabs_session_cookie"):
        cookie = s.cookies.get("inlabs_session_cookie")
    else:
        print("Falha ao obter cookie. Verifique suas credenciais")
        exit(37)

    # Montagem da URL:
    ano = datetime.datetime.today().strftime("%Y")
    mes = datetime.datetime.today().strftime("%m")
    dia = datetime.datetime.today().strftime("%d")
    data_completa = ano + "-" + mes + "-" + dia

    # data_completa = '2023-05-02'

    for dou_secao in tipo_dou.split(" "):
        print("Aguarde Download...")
        url_arquivo = (
            url_download
            + data_completa
            + "&dl="
            + data_completa
            + "-"
            + dou_secao
            + ".zip"
        )
        cabecalho_arquivo = {
            "Cookie": "inlabs_session_cookie=" + cookie,
            "origem": "736372697074",
        }
        response_arquivo = s.request("GET", url_arquivo, headers=cabecalho_arquivo)
        caminho = directory_FETCH + "DOUS\\" + data_completa + "-" + dou_secao
        arq = data_completa + "-" + dou_secao + ".zip"
        if response_arquivo.status_code == 200:
            with open(arq, "wb") as f:
                f.write(response_arquivo.content)
                print("Arquivo %s salvo." % (arq))
                f.close()
                with zipfile.ZipFile(arq, "r") as zip_ref:
                    if not os.path.exists(caminho):
                        os.makedirs(caminho)
                    else:
                        print("Erro! Pasta Já existe!")
                    zip_ref.extractall(caminho)
                    print("Pasta Extraída")
            del response_arquivo
            del f
            os.remove(directory_FETCH + arq)
            print("Arquivo ZIP em duplicata excluído com Sucesso!")
        elif response_arquivo.status_code == 404:
            print("Arquivo não encontrado:")

    print("Aplicação encerrada")
    exit(0)


def login():
    if datetime.datetime.today().weekday() not in [5, 6]:
        try:
            response = s.request(
                "POST",
                url_login,
                data=payload,
                headers=headers,
                timeout=7,
                verify=False,
            )

            download()
        except requests.exceptions.ConnectionError:
            login()
    else:
        print("Não há edição do DOU disponivel em finais de semana!")


login()


# python -W ignore inlabs-auto-download-xml.py
