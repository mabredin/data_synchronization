from database_connection import ConnectorToDB
from generator_nickname import GeneratorNickname
from parser_xml import ParserXML


def main():
    parser = ParserXML()
    
    # Получение данных всех пользователей
    # и отдельно данных новых пользователей
    parser.get_employees_info()
    print(parser.employees_info)
    print(parser.new_employees)
    
    # Получение всех никнеймов пользователей из БД
    connector = ConnectorToDB()
    existing_nicknames = connector.get_logins_of_users()
    
    # Генерация логинов для новых пользователей
    generator_nickname = GeneratorNickname(existing_nicknames, parser.new_employees)
    result = generator_nickname.generate_list_original_nicknames()
    if result:
        print(result)


if __name__ == '__main__':
    main()
    