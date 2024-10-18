import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

# Указываем URL сайта
base_url = 'http://heta.dan.tatar/'

# Функция для создания директорий
def create_directory(path):
    if not os.path.exists(path):
        os.makedirs(path)

# Функция для скачивания файла
def download_file(url, destination):
    response = requests.get(url)
    if response.status_code == 200:
        with open(destination, 'wb') as file:
            file.write(response.content)
        print(f'Downloaded: {destination}')
    else:
        print(f'Failed to download: {url}')

# Функция для парсинга и скачивания файлов
def parse_and_download(url, local_path):
    response = requests.get(url)
    if response.status_code != 200:
        print(f'Failed to access: {url}')
        return

    soup = BeautifulSoup(response.text, 'html.parser')

    # Ищем все ссылки на файлы
    for link in soup.find_all('a'):
        file_url = urljoin(url, link.get('href'))
        file_name = os.path.basename(file_url)

        if link.get('href') and not link.get('href').endswith('/'):
            # Путь для сохранения файла
            file_path = os.path.join(local_path, file_name)

            # Скачиваем файл
            download_file(file_url, file_path)

        elif link.get('href') and link.get('href').endswith('/'):
            # Рекурсивный вызов для директории
            dir_name = os.path.basename(link.get('href').rstrip('/'))
            new_local_path = os.path.join(local_path, dir_name)
            create_directory(new_local_path)
            parse_and_download(file_url, new_local_path)

# Создаем основную директорию для скачивания
target_directory = 'downloaded_files'
create_directory(target_directory)

# Запускаем парсер
parse_and_download(base_url, target_directory)
