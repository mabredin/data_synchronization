from parser_xml import Employee


transliterate_list = {
    # lowercase
    'а': 'a', 'б': 'b', 'в': 'v',
    'г': 'g', 'д': 'd', 'е': 'e',
    'ё': 'e', 'ж': 'zh', 'з': 'z',
    'и': 'i', 'й': 'i', 'к': 'k',
    'л': 'l', 'м': 'm', 'н': 'n',
    'о': 'o', 'п': 'p', 'р': 'r',
    'с': 's', 'т': 't', 'у': 'u',
    'ф': 'f', 'х': 'kh', 'ц': 'ts',
    'ч': 'ch', 'ш': 'sh', 'щ': 'shch',
    'ъ': 'ie', 'ы': 'y', 'ь': '',
    'э': 'e', 'ю': 'iu', 'я': 'ia',
    # uppercase
    'А': 'A', 'Б': 'B', 'В': 'V',
    'Г': 'G', 'Д': 'D', 'Е': 'E',
    'Ё': 'E', 'Ж': 'Zh', 'З': 'Z',
    'И': 'I', 'Й': 'I', 'К': 'K',
    'Л': 'L', 'М': 'M', 'Н': 'N',
    'О': 'O', 'П': 'P', 'Р': 'R',
    'С': 'S', 'Т': 'T', 'У': 'U',
    'Ф': 'F', 'Х': 'Kh', 'Ц': 'Ts',
    'Ч': 'Ch', 'Ш': 'Sh', 'Щ': 'Shch',
    'Ъ': 'Ie', 'Ы': 'Y', 'Ь': '',
    'Э': 'E', 'Ю': 'Iu', 'Я': 'Ia'
}


class GeneratorNickname:
    def __init__(
            self,
            existing_nicknames: list[str] = [],
            new_employees: list[Employee] = []
        ) -> None:
        self.existing_nicknames = existing_nicknames
        self.new_employees = new_employees

    def generate_original_nicknames(self) -> None:
        if self._check_attributes:
            for employee in self.new_employees:
                login = self._generate_original_nickname(employee)
                employee._set_login(login)

    def _check_attributes(self) -> bool:
        if self.existing_nicknames and self.new_employees:
            return True
        return False
    
    def _generate_original_nickname(self, employee: Employee) -> str:
        user_info = self._split_fullname(employee)
        new_nickname = self._generate_and_check_nickname(user_info)
        return new_nickname

    def _split_fullname(self, employee: Employee) -> dict[str, str]:
        surname, firstname, patronymic = employee.fio.lower().strip().split()
        user_info = {
            'surname': self._transliterate(surname),
            'firstname': self._transliterate(firstname),
            'patronymic': self._transliterate(patronymic)
        }
        return user_info
    
    def _transliterate(self, word: str) -> str:
        for i in word:
            word = word.replace(i, transliterate_list[i])
        return word
    
    def _generate_and_check_nickname(
            self,
            user_info: dict[str, str],
            nickname: str=''
        ) -> str:
        nickname = self._generate_nickname(user_info)
        patronymic_index = 1
        while not self._check_nickname_for_originality(nickname):
            nickname = self._generate_nickname(user_info, patronymic_index)
            patronymic_index += 1
        return nickname
    
    def _generate_nickname(self, user_info: dict[str, str], index: int=0) -> str:
        firstname = user_info['firstname'][:1]
        patronymic = user_info['patronymic'][:index]
        surname = user_info['surname']
        return firstname + patronymic + '_' + surname

    def _check_nickname_for_originality(self, nickname: str) -> bool:
        if nickname not in self._get_list_of_existing_nicknames():
            self.existing_nicknames.append(nickname)
            return True
        return False

    def _get_list_of_existing_nicknames(self) -> list[str]:
        return self.existing_nicknames
    