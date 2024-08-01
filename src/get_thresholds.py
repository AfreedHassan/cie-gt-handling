from src.pdf_downloader import download_pdf_files
from src.pdf_extractor import extract_thresholds

def get_thresholds(arg_v:list[str])->list[list[str]]:
    """
    Download PDFs to local directory
    Extract the thresholds from each PDF of the given combination of components and append to the list
    Delete the downloaded pdfs.
    Return a list[list[str]] of the thresholds

    :param arg_v: a list with structure [code, combo, max_weighted_mark, latest_year, number_of_years=10]
                  where code <- subject code, combo <- combination of components, max_weighted_mark is as it says, 
                  latest_year <- most recent year from which thresholds should be downloaded from.
                  number_of_years=10 <- number of years to go back and download from. 
    :return:  list of lists of strings representing the thresholds.
    """
    code = arg_v[1]
    combo = arg_v[2]
    max_weighted_mark = int(arg_v[3])
    latest_year = arg_v[4]
    number_of_years = 10
    if len(arg_v) == 6:
        number_of_years = arg_v[5]

    years = []
    for y in range(0,number_of_years):
        if latest_year-y != 20: years.append(latest_year-y)

    thresholds:list[list[str]] = [["Si. No", "Session", "Full Mark", 'A*', 'A', 'B', 'C', 'D', 'E']]
    for year in years:
        pdfs = download_pdf_files(code,year) #returns the list of pdfs downloaded
        for pdf in pdfs: 
            thresholds.append(extract_thresholds(pdf,combo,max_weighted_mark))
    return thresholds
