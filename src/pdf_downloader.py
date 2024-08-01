import os
import requests
import json
from sys import argv


def download_pdf_files(code:str, year:str) -> list[str]:
    """Download PDF from given URL to local directory.

    :param url: The url of the PDF file to be downloaded
    :return: True if PDF file was successfully downloaded, otherwise False.
    """
    with open("subjectInfo.json", 'r') as f:
        sub_info = json.load(f)

    variants = ['w', 's', 'm']

    pdfs = []

    for variant in variants:
        url = f'https://bestexamhelp.com/exam/cambridge-{sub_info[code]["qual"]}/{sub_info[code]["name"]}-{code}/20{year}/{code}_{variant}{year}_gt.pdf'

        # Request URL and get response object
        response = requests.get(url, stream=True)

        # isolate PDF filename from URL
        pdf_file_name = os.path.basename(url)
        if response.status_code == 200:
            # Save in current working directory
            filepath = os.path.join(os.getcwd(), pdf_file_name)
            with open(filepath, 'wb') as pdf_object:
                pdf_object.write(response.content)
                print(f'{pdf_file_name} was successfully saved!')
                pdfs.append(pdf_file_name)
        else:
            print(f'Uh oh! Could not download {pdf_file_name},')
            print(f'HTTP response status code: {response.status_code}')

    os.system('del *.pdf')
    return pdfs

if __name__ == '__main__':
    code = argv[1]
    year = argv[2]
    download_pdf_files(code,year)
