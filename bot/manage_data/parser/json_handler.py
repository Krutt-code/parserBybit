import json

class JsonHandler:

    def __init__(self, filename: str) -> None:
        self.filename = filename

    def write_json(self, data: dict | list) -> None:
        '''Перезапись файла новыми данными
        :param data: [{'id': 1, 'name': 'kook'}, {'id': 2, 'name': 'lool'}] | {'id': 1, 'name': 'kook'}]
        '''
        with open(self.filename, 'w', encoding='utf-8') as file:
            json.dump(data, file, indent=4, ensure_ascii=False)

    def write_to_json(self, data: dict) -> None:
        '''Добавление данных в файл json
        :param data: {'id': 1, 'name': 'kook'}
        '''
        try: 
            with open(self.filename, 'r', encoding='utf-8') as file:
                f = json.load(file)
        except:
            print("Ошибка: Файл для чтения не найден.")
            return
        
        try:
            f.update(data)
        except:
            f.append(data)

        with open(self.filename, 'w', encoding='utf-8') as file:
            json.dump(f, file, indent=4, ensure_ascii=False)
        
    def writes_to_json(self, data: list | dict) -> None:
        '''Добавление множества данных в файл
        :param data: [{'id': 1, 'name': 'kook'}, {'id': 2, 'name': 'lool'}] | {'id': 1, 'name': 'kook'}]
        '''

        try: 
            with open(self.filename, 'r', encoding='utf-8') as file:
                f = json.load(file)
        except:
            print("Ошибка: Файл для чтения не найден.")
            return
        
        try:
            for item in data.items():
                f.append({item[0]: item[1]})
        except:
            for item in data.items():
                f.update({item[0]: item[1]})

        with open(self.filename, 'w', encoding='utf-8') as file:
            json.dump(f, file, indent=4, ensure_ascii=False)


    def read_json(self) -> None | dict:
        '''Чтение файлов json'''
        try:
            with open(self.filename, 'r', encoding='utf-8') as file:
                return json.load(file)
        except:
            print("Ошибка: Файл для чтения не найден.")