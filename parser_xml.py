import datetime
from typing import Optional
import xml.etree.ElementTree as ET

import config


class Employee:
    def __init__(self) -> None:
        self.fio: str = ''
        self.empl_code: Optional[str] = ''
        self.event_state: Optional[str] = ''
        self.department: Optional[str] = ''
        self.job_position: Optional[str] = ''
        self.event_date: Optional[str] = ''
        self.fl: Optional[str] = ''
        self.birthday: Optional[str] = ''

    def __str__(self):
        return self.fio

    def __repr__(self):
        return self.fio

    def _set_fl(self, value: Optional[str]) -> None:
        if value:
            self.fl = value

    def _set_birthday(self, value: Optional[str]) -> None:
        if value:
            self.birthday = value

    def _get_right_param(self, param: str) -> Optional[str]:
        return self.empl_code if param == 'empl_code' else self.fl


class ParserXML:
    def __init__(self) -> None:
        self.root = self.__define_root(config.FILE_NAME)
        self.employees_info: list[Employee] = []
        self.new_employees: list[Employee] = []
        self.transferred_employees: list[Employee] = []
        self.fired_employees: list[Employee] = []
        self.employees_name: list[str] = []

    def __define_root(self, file_name: Optional[str]) -> ET.Element:
        if not file_name:
            raise ValueError("File name must not be empty")
        if type(file_name) is not str:
            raise TypeError("The filename must be a string")
        return ET.parse(file_name).getroot()

    def get_employees_info(self) -> list[Employee]:
        self._parse_employees_info_by_event()
        self._parse_employees_remaining_info()
        self._get_new_employees()
        self._get_transferred_employees()
        self._get_fired_employees()
        return self.employees_info

    def _parse_employees_info_by_event(self) -> None:
        for event in self.root.iter('SostSotr'):
            event_date = self._check_params(event, 'Dat')
            if event_date and self._check_happened_recently(event_date):
                employee = Employee()
                employee.fio = self._get_employee_name_by_param(event, 'Sotr')
                self._set_attrs_by_event(employee, event)
                self.employees_info.append(employee)
                self.employees_name.append(employee.fio)

    def _parse_employees_remaining_info(self) -> None:
        self._parse_fl()
        self._parse_birthdays()

    def _get_new_employees(self) -> None:
        self.new_employees = [
            emp for emp in self.employees_info if self._check_event_state(emp, '1')
        ]

    def _get_transferred_employees(self) -> None:
        self.transferred_employees = [
            emp for emp in self.employees_info if self._check_event_state(emp, '2')
        ]

    def _get_fired_employees(self) -> None:
        self.fired_employees = [
            emp for emp in self.employees_info if self._check_event_state(emp, '3')
        ]

    def _check_params(self, tag: ET.Element, param: str) -> Optional[str]:
        attr = tag.find(param)
        attr_text = attr.text if attr is not None else None
        return attr_text.strip() if attr_text is not None else None

    def _check_happened_recently(self, date: str) -> bool:
        event_date = self._get_right_format_date(date)
        if config.COUNT_DAYS_FOR_SEARCH:
            days = int(config.COUNT_DAYS_FOR_SEARCH)
        return event_date > datetime.datetime.now() - datetime.timedelta(days=days)

    def _get_employee_name_by_param(self, tag: ET.Element, param: str) -> str:
        innertag = self._check_params(tag, param)
        return ' '.join(innertag.split()[:3]) if innertag else ''

    def _set_attrs_by_event(self, employee: Employee, event: ET.Element) -> None:
        employee.empl_code = self._check_params(event, 'SotrKod')
        employee.event_state = self._check_params(event, 'Sost')
        employee.department = self._check_params(event, 'Podr')
        employee.job_position = self._check_params(event, 'Proff')
        employee.event_date = self._check_event_date(event, 'Dat')

    def _parse_fl(self) -> None:
        for sotr in self.root.findall('Sotrs')[0].findall('Sotr'):
            empl_fio = self._get_employee_name_by_param(sotr, 'Naim')
            if self._check_for_compliance(empl_fio, sotr, 'empl_code'):
                fl = self._check_params(sotr, 'Fl')
                employee = self._get_employee_by_fio_from_list(empl_fio)
                employee._set_fl(fl) if employee else None

    def _parse_birthdays(self) -> None:
        for sotr in self.root.iter('Fiz'):
            empl_fio = self._get_employee_name_by_param(sotr, 'FlN')
            if self._check_for_compliance(empl_fio, sotr, 'fl'):
                full_birthday = self._check_params(sotr, 'DatR')
                birthday = self._split_birthday(full_birthday)
                employee = self._get_employee_by_fio_from_list(empl_fio)
                employee._set_birthday(birthday) if employee else None

    def _check_event_state(self, empl: Employee, event_state: str) -> bool:
        if empl.event_state == event_state:
            return True
        return False

    def _get_right_format_date(self, date: str) -> datetime.datetime:
        if type(date) is not str:
            raise TypeError("The date must be a string")
        return datetime.datetime.strptime(date, '%d.%m.%Y %H:%M:%S')

    def _check_event_date(self, event: ET.Element, param: str) -> Optional[str]:
        event_date = event.find(param)
        assert event_date is not None
        assert event_date.text is not None
        return event_date.text.split()[0]

    def _check_for_compliance(self, fio: str, sotr: ET.Element, param: str) -> bool:
        if fio in self.employees_name:
            employee = self._get_employee_by_fio_from_list(fio)
            if not employee:
                return False
            empl_param = employee._get_right_param(param)
            if empl_param == self._check_params(sotr, 'Kod'):
                return True
        return False

    def _get_employee_by_fio_from_list(self, empl_fio: str) -> Optional[Employee]:
        for empl in self.employees_info:
            if empl.fio == empl_fio:
                return empl
        return None

    def _split_birthday(self, param: Optional[str]) -> Optional[str]:
        return param.split()[0] if param else None


if __name__ == '__main__':
    parser = ParserXML()
    parser.get_employees_info()

    for empl in parser.employees_info:
        print(f"{empl.fio}")
        print(f"\t\t\templ_code: {empl.empl_code}")
        print(f"\t\t\tevent_date: {empl.event_date}")
        print(f"\t\t\tevent_state: {empl.event_state}")
        print(f"\t\t\tdepartment: {empl.department}")
        print(f"\t\t\tjob_position: {empl.job_position}")
        print(f"\t\t\tfl: {empl.fl}")
        print(f"\t\t\tbirthday: {empl.birthday}")

    print(f"Все сотрудники:\n\t{parser.employees_info}")
    print(f"Новые сотрудники:\n\t{parser.new_employees}")
    print(f"Переведенные сотрудники:\n\t{parser.transferred_employees}")
    print(f"Уволенные сотрудники:\n\t{parser.fired_employees}")
    