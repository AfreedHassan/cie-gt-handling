import pdfplumber 
from sys import argv

def extract_thresholds(pdf:str,combo:str, max_weighted_mark:int) -> str:
    """
    Extract the thresholds from each PDF of the given combination of components and append to the list
    Delete the downloaded pdfs.
    Return a list[[list[str]] of the thresholds

    :param pdf: name of pdf file.
    :param combo: combination of components.
    :param max_weighted_mark: as it says.
    :return: a list of lists of strings representing the thresholds.
    """
    extract_thresholds.counter += 1 
    variant:chr = pdf[5] #pdf has format #CCCC_vYY_gt.pdf where v is variant
    year:str = pdf[6:8]  #and YY is year

    #first three cells of row.
    threshold = [str(extract_thresholds.counter), f"{variant}{year}",str(max_weighted_mark)]

    with pdfplumber.open(pdf) as f:
        for page in f.pages:
            tables = page.extract_tables()
            for table in tables:
                for row in table:
                    if combo in row: # row has format [option, (maxRawMark), comboOfComponents, A*, A, B, C, D, E], where the grades represent the threshold for each mark.
                        for e in row: 
                            if e.isnumeric():
                                threshold.append(e)
                        if (threshold[2] == threshold[3]): threshold.pop(2) #to account for the case when the max_weighted_mark is part of the table, so max_weighted_mark is repeated.
                        return (threshold)
        return []
extract_thresholds.counter = 0
