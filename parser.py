import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse

urls = [
    "https://heta.dan.tatar/AmoreForever/amoremods/",
    "https://heta.dan.tatar/CakesTwix/Hikka-Modules/",
    "https://heta.dan.tatar/Codwizer/ReModules/",
    "https://heta.dan.tatar/D4n13l3k00/FTG-Modules/",
    "https://heta.dan.tatar/DarkModules/hikkamods/",
    "https://heta.dan.tatar/Den4ikSuperOstryyPer4ik/Astro-modules/",
    "https://heta.dan.tatar/DziruModules/hikkamods/",
    "https://heta.dan.tatar/Fl1yd/FTG-Modules/",
    "https://heta.dan.tatar/GD-alt/mm-hikka-mods/",
    "https://heta.dan.tatar/GeekTG/FTG-Modules/",
    "https://heta.dan.tatar/HitaloSama/FTG-modules-repo/",
    "https://heta.dan.tatar/Ijidishurka/catmod/",
    "https://heta.dan.tatar/Ijidishurka/modules/",
    "https://heta.dan.tatar/KeyZenD/modules/",
    "https://heta.dan.tatar/MoriSummerz/ftg-mods/",
    "https://heta.dan.tatar/N3rcy/modules/",
    "https://heta.dan.tatar/Sad0ff/modules-ftg/",
    "https://heta.dan.tatar/SekaiYoneya/Friendly-telegram/",
    "https://heta.dan.tatar/SkillsAngels/Modules/",
    "https://heta.dan.tatar/Yahikoro/Modules-for-FTG/",
    "https://heta.dan.tatar/anon97945/hikka-mods/",
    "https://heta.dan.tatar/blazedzn/ftg-modules/",
    "https://heta.dan.tatar/dorotorothequickend/DorotoroModules/",
    "https://heta.dan.tatar/hikariatama/ftg/",
    "https://heta.dan.tatar/iamnalinor/FTG-modules/",
    "https://heta.dan.tatar/kamolgks/Hikkamods/",
    "https://heta.dan.tatar/m4xx1m/FTG/",
    "https://heta.dan.tatar/shadowhikka/sh.modules/",
    "https://heta.dan.tatar/skillzmeow/skillzmods_hikka/",
    "https://heta.dan.tatar/sqlmerr/hikka_mods/",
    "https://heta.dan.tatar/thomasmod/hikkamods/",
    "https://heta.dan.tatar/trololo65/Modules/",
    "https://heta.dan.tatar/vsecoder/hikka_modules/"
]

base_local_path = os.path.join(os.getcwd(), "hikka", "modules")

def create_local_directory(path):
    if not os.path.exists(path):
        os.makedirs(path)
        print(f"Создана директория: {path}")

def get_py_files(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        py_files = []
        for link in soup.find_all('a'):
            href = link.get('href')
            if href and href.endswith('.py'):
                full_url = urljoin(url, href)
                py_files.append(full_url)
        return py_files
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP ошибка для {url}: {http_err}")
    except Exception as err:
        print(f"Ошибка для {url}: {err}")
    return []

def download_file(file_url, local_path):
    try:
        response = requests.get(file_url)
        response.raise_for_status()
        with open(local_path, 'wb') as f:
            f.write(response.content)
        print(f"Скачано: {file_url} -> {local_path}")
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP ошибка при скачивании {file_url}: {http_err}")
    except Exception as err:
        print(f"Ошибка при скачивании {file_url}: {err}")

def main():
    for url in urls:
        parsed_url = urlparse(url)
        path_parts = parsed_url.path.strip('/').split('/')
        if len(path_parts) >= 2:
            main_folder = path_parts[-2]
            sub_folder = path_parts[-1]
            local_dir = os.path.join(base_local_path, main_folder, sub_folder)
            create_local_directory(local_dir)
            py_files = get_py_files(url)
            if py_files:
                for file_url in py_files:
                    filename = os.path.basename(urlparse(file_url).path)
                    local_file_path = os.path.join(local_dir, filename)
                    download_file(file_url, local_file_path)
            else:
                print(f"No .py files found in {url}")
        else:
            print(f"Некорректный URL или структура пути: {url}")

if __name__ == "__main__":
    main()
