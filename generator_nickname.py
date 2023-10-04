from typing import Iterable, Optional


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

# test list of nicknames
existing_nicknames = [
    'm_bredin', 's_abdullov', 's_rudikov',
    'v_pankin', 'i_abaturov', 'k_abaturov',
    'd_ivanov', 'alv_ivanov', 'iu_ivanov',
    'av_ivanov', 'ivanovvv', 'iv_ivanov',
    'i_ivanov', 'ivanovlv', 'o_ivanov'
]

# test tuple of new employees
new_employees = (
    'Бредин Максим Андреевич', 'Абатуров Кирилл Леонидович',
    'Иванов Андрей Владимирович', 'Иванов Алексей Алексеевич',
    'Шутько Константин Иванович', 'Иванов Алексей Алексеевич',
    'Бредин Игорь Андреевич', 'Бредина Ангелина Борисовна'
)


class GeneratorNickname:
    def __init__(
            self,
            existing_nicknames: list[str] = [],
            new_employees: Iterable[str] = []
        ) -> None:
        self.existing_nicknames = existing_nicknames
        self.new_employees = new_employees

    def generate_list_original_nicknames(self) -> Optional[list[str]]:
        if self._check_attributes:
            return [self._generate_original_nickname(emp) for emp in self.new_employees]
        return None

    def _check_attributes(self) -> bool:
        if self.existing_nicknames and self.new_employees:
            return True
        return False
    
    def _generate_original_nickname(self, name: str) -> str:
        user_info = self._split_fullname(name)
        new_nickname = self._generate_and_check_nickname(user_info)
        return new_nickname

    def _split_fullname(self, name: str) -> dict[str, str]:
        surname, firstname, patronymic = name.lower().strip().split()
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


if __name__ == '__main__':
    example = GeneratorNickname(existing_nicknames, new_employees)
    print(example.generate_list_original_nicknames())
    