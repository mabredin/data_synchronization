import datetime
from typing import Optional
import xml.etree.ElementTree as ET

import config


class Employee:
    def __init__(self) -> None:
        self.fio: str = ''
        
    def _set_attributes_by_event(self, event: ET.Element) -> None:
        self.empl_code = self._check_params(event, 'SotrKod')
        self.event_state = self._check_params(event, 'Sost')
        self.department = self._check_params(event, 'Podr')
        self.job_position = self._check_params(event, 'Proff')
        self.event_date = self._check_event_date(event, 'Dat')

    def _check_params(self, event: ET.Element, param: str) -> Optional[str]:
        attr = event.find(param)
        attr_text = attr.text if attr is not None else None
        return attr_text.strip() if attr_text is not None else None
    
    def _check_event_date(self, event: ET.Element, param: str) -> Optional[str]:
        event_date = event.find('Dat')
        assert event_date is not None
        assert event_date.text is not None
        return event_date.text.split()[0]


class ParserXML:
    def __init__(self) -> None:
        self.root = self.__define_root(config.FILE_NAME)
        self.employees_info: dict[str, dict] = {}
        self.new_employees: list[str] = []

    def __define_root(self, file_name: Optional[str]) -> ET.Element:
        if not file_name:
            raise ValueError("File name must not be empty")
        if type(file_name) is not str:
            raise TypeError("The filename must be a string")
        return ET.parse(file_name).getroot()

    def get_employees_info(self) -> dict[str, dict]:
        self._parse_employees_info_by_event()
        self._parse_employees_remaining_info()
        self.get_new_employees()
        return self.employees_info

    def _parse_employees_info_by_event(self) -> None:
        for event in self.root.iter('SostSotr'):
            event_date = self._check_params(event, 'Dat')
            if event_date and self._check_happened_recently(event_date):
                employee = Employee()
                employee.fio = self._get_employee_name_by_param(event, 'Sotr')
                employee._set_attributes_by_event(event)
                self._set_employees_info(employee)

    def _parse_employees_remaining_info(self) -> None:
        self._parse_fl()
        self._parse_birthdays()
        
    def get_new_employees(self) -> None:
        self.new_employees = [
            emp for emp in self.employees_info if self._check_event_state(emp, '1')
        ]
    
    def _check_params(self, tag: ET.Element, param: str) -> Optional[str]:
        attr = tag.find(param)
        attr_text = attr.text if attr is not None else None
        return attr_text.strip() if attr_text is not None else None
    
    def _check_happened_recently(self, date: str) -> bool:
        event_date = self._get_right_format_date(date)
        return event_date > datetime.datetime.now() - datetime.timedelta(days=90)

    def _get_employee_name_by_param(self, tag: ET.Element, param: str) -> str:
        innertag = self._check_params(tag, param)
        return ' '.join(innertag.split()[:3]) if innertag else ''

    def _set_employees_info(self, employee: Employee) -> None:
        self.employees_info[employee.fio] = {
            'empl_code': employee.empl_code,
            'event_date': employee.event_date,
            'event_state': employee.event_state,
            'department': employee.department,
            'job_position': employee.job_position
        }

    def _parse_fl(self) -> None:
        for sotr in self.root.findall('Sotrs')[0].findall('Sotr'):
            empl_fio = self._get_employee_name_by_param(sotr, 'Naim')
            if self._check_for_compliance(empl_fio, sotr, 'empl_code'):
                fl = self._check_params(sotr, 'Fl')
                self.employees_info[empl_fio]['fl'] = fl

    def _parse_birthdays(self) -> None:
        for sotr in self.root.iter('Fiz'):
            empl_fio = self._get_employee_name_by_param(sotr, 'FlN')
            if self._check_for_compliance(empl_fio, sotr, 'fl'):
                full_birthday = self._check_params(sotr, 'DatR')
                birthday = self.split_birthday(full_birthday)
                self.employees_info[empl_fio]['birthday'] = birthday
    
    def split_birthday(self, param: Optional[str]) -> Optional[str]:
        return param.split()[0] if param else None
    
    def _check_event_state(self, empl: str, event_state: str) -> bool:
        if self.employees_info[empl]['event_state'] == event_state:
            return True
        return False
    
    def _get_right_format_date(self, date: str) -> datetime.datetime:
        if type(date) is not str:
            raise TypeError("The date must be a string")
        return datetime.datetime.strptime(date, '%d.%m.%Y %H:%M:%S')
    
    def _check_for_compliance(self, fio: str, sotr: ET.Element, param: str) -> bool:
        if fio in self.employees_info.keys():
            employee = self.employees_info[fio]
            if employee[param] == self._check_params(sotr, 'Kod'):
                return True
        return False


if __name__ == '__main__':
    parser = ParserXML()
    parser.get_employees_info()
    for fio, info in parser.employees_info.items():
        print(f"{fio}")
        for k, v in info.items():
            print(f"\t\t\t{k}: {v}")
    
    print(parser.new_employees)
    