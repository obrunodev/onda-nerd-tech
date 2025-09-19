from datetime import datetime

MONTHS_MAPPING = {
    "1": "Janeiro", "2": "Fevereiro", "3": "Março", "4": "Abril",
    "5": "Maio", "6": "Junho", "7": "Julho", "8": "Agosto",
    "9": "Setembro", "10": "Outubro", "11": "Novembro", "12": "Dezembro",
}

actual_year = datetime.today().year
YEARS = range(actual_year - 10, actual_year + 50)
