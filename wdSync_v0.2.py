'''
wdSync v0.2 by Klykov Leonid
WatchDog syncronizer - программа для отправки со стендов на сервер файлов с результатами испытаний
Development started 2020/12/30
Спасибо за идею AterCattus`у, его пост от 25 марта 2012 в 14:51 https://habr.com/ru/post/140649/
У event есть 4 свойства src_path, is_directory, event_type («created», «deleted», и т.п.). Для события moved добавляется свойство dest_path.
'''

#0 =========== Imports ================

import time
from shutil import copy2 as copy
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

#1 ========== Classes and functions ===========

def sync(filePath, serverPath):
	try:
		copy(filePath, serverPath)
		print('Синхронизация проведена успешно')
	except IOError:
		print('Копирование не удалось')


class Handler(FileSystemEventHandler):
	def on_created(self, event):
		print(time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime()), event)
		print(event.src_path)
		sync(event.src_path, serverPath)

	def on_deleted(self, event):
		print(event)

	def on_moved(self, event):
		print(event)

#2 ================= Preparing ==================

#2.1 Define stend number and server path
stendNetName = 'arm_0' #os.environ['COMPUTERNAME']

if   stendNetName == 'arm_0': serverPath = 'Saukip/Arm_0'
elif stendNetName == 'arm_1': serverPath = 'Saukip/Arm_1'
elif stendNetName == 'arm_2': serverPath = 'Saukip/Arm_2'
elif stendNetName == 'arm_3': serverPath = 'Saukip/Arm_3'
elif stendNetName == 'arm_5': serverPath = 'Saukip/Arm_5'
else: print('Сетевое имя компьютера не соответствует стандарту имен или отсутствет. Проверьте настройки имени компьютера, должно быть "arm0", "arm1", "arm2", "arm3" или "arm5".')


#3 Launching program
observer = Observer()
observer.schedule(Handler(), path=r'D:\code\python\folders', recursive=True)
observer.start()


try:
	while True:
		time.sleep(0.1)
except KeyboardInterrupt:
	observer.stop()

observer.join()

print('finished')
input()