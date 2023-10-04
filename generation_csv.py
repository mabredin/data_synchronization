from csv import writer
from typing import Any

from parser_xml import ParserXML


def write_in_file(employees: dict[str, dict]) -> None:
    with open('daily_report.csv', 'w', newline='') as csvfile:
        spamwriter = writer(csvfile, delimiter=';')
        print(type(spamwriter))
        _writerow(spamwriter, employees)


def _writerow(spamwriter: Any, employees: dict[str, dict]) -> None:
    params = _get_nested_dictionary_keys(employees)
    spamwriter.writerow(['fullname'] + [param for param in params])
    for employee, options in employees.items():
        spamwriter.writerow([employee] + [options[param] for param in params])


def _get_nested_dictionary_keys(employees: dict[str, dict]) -> list[str]:
    return [options for options in list(employees.values())[0]]


if __name__ == '__main__':
    parser = ParserXML()
    parser.get_employees_info()
    if parser.employees_info:
        write_in_file(parser.employees_info)
    else:
        print('Нет информации о сотрудниках')
