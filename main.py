from tkinter import *
import cryptocompare



# zopytmalizowac potem kod, ladniejsze zmienne, ladniej napisane posegregowane

# dac komunikaty zakupiono iles btc sprzedano iles btc






# dodac mozliwosc wybrania waluty oraz kryptowaluty do trejdowania

# w przuszlosci jakies nwm symulacje w czasie czy cos ale to nie ma sensu troche bo tradowanie dotyczy aktualnych sytuacji tym bardziej tu bez wykresu


class App:
	def __init__(self):
		self.root = Tk()
		self.root.geometry("900x600")
		self.root.title("Bitcoin live trading simulator")
		#self.root.iconbitmap('/Users/michvl/Desktop/SYMULATOR GIELDY BITCOIN/icon.ico')
		self.root.resizable(False, False) 


		self.bgcolor = "#ADD8E6"
		self.root.configure(background=self.bgcolor)

		self.bgimage=PhotoImage(file="/Users/michvl/Desktop/SYMULATOR GIELDY BITCOIN/bg.png")
		self.bg = Label(self.root, image=self.bgimage)
		self.bg.place(x=0, y=0, relwidth=1, relheight=1)


		self.how_much_decimals_btc = 7

		





		# summary
		self.summary = Label(self.root, text='Summary')
		self.summary.place(x=630,y=5)


		try:
			with open('howmuchpaidin.txt', 'r') as f:
				self.howmuchpaidin = float(f.read())
		except:
			self.howmuchpaidin = 0.0


		self.paidin = Label(self.root, text='Paid in on stock: $' + str(self.howmuchpaidin))
		self.paidin.place(x=630,y=40)

		try:
			with open('howmuchbtc.txt', 'r') as f:
				self.howmuchbtconaccount = float(f.read())
		except:
			self.howmuchbtconaccount = 0.0

		self.btcbalance = Label(self.root, text='Account balance: ' + str(self.howmuchbtconaccount) + " BTC", highlightcolor=self.bgcolor, activebackground=self.bgcolor)
		self.btcbalance.place(x=630, y=80)



		self.currentbtcvalue = Label(self.root, text='Current value of BTC: $0')
		self.currentbtcvalue.place(x=630,y=120)


		try:
			with open('howmuchpaidfrom.txt', 'r') as f:
				self.howmuchpaidfrom = float(f.read())
		except:
			self.howmuchpaidfrom = 0.0

		self.paidfrom = Label(self.root, text='Paid from the stock: $' + str(self.howmuchpaidfrom))
		self.paidfrom.place(x=630,y=160)

		self.balance_variable = 0
		self.balance = Label(self.root, text='Balance: $0')
		self.balance.place(x=630, y=210)

		# 'aktualnawartosc + wyplacone - wplacone'
		self.balancelabel = Label(self.root, text='(current BTC value + paid from - paid in)')
		self.balancelabel.place(x=630, y=240)

		self.reset_stats_button = Button(self.root, text='Reset', command=self.reset)
		self.reset_stats_button.place(x=630, y=550)


		#self.minebtcbutton = Button(self.root, text='Mine*')
		#self.minebtcbutton.place(x=5,y=72)


		self.current_btc_price = Label(self.root, text='Current BTC price', font=("Helvetica", 17))
		self.current_btc_price.place(x=265,y=150)

		self.label_current_btc_price = Label(self.root, text="", font=("Helvetica", 20))
		self.label_current_btc_price.place(x=225,y=200)


		self.label_how_much_btc = Label(self.root, text='For how much $ I am buying/selling BTC (must be int, not float)')
		self.label_how_much_btc.place(x=140, y=278)
		self.for_how_much_dollars = Entry(self.root)
		self.for_how_much_dollars.place(x=240, y=300)

		self.buybutton = Button(self.root, text='Buy', command=self.buyBTC, activebackground='black', highlightcolor='black')
		self.buybutton.place(x=240,y=350)

		self.sellbutton = Button(self.root, text='Sell', command=self.sellBTC)
		self.sellbutton.place(x=374,y=350)





		self.btcpriceactual()


		self.root.mainloop()


	def reset(self):
		self.howmuchbtconaccount = 0
		self.howmuchpaidin = 0
		self.howmuchpaidfrom = 0

		with open('howmuchpaidin.txt', 'w') as f:
			f.write(str(self.howmuchpaidin))

		with open('howmuchpaidfrom.txt', 'w') as f:
			f.write(str(self.howmuchpaidfrom))

		with open('howmuchbtc.txt', 'w') as f:
			f.write(str(self.howmuchbtconaccount))


		self.btcbalance.configure(text='Account balance: ' + str(self.howmuchbtconaccount) + " BTC", highlightcolor=self.bgcolor, activebackground=self.bgcolor)
		self.paidfrom.configure(text='Paid from the stock: $' + str(self.howmuchpaidfrom))
		self.paidin.configure(text='Paid in on stock: $' + str(self.howmuchpaidin))



	def buyBTC(self):
		for_how_much_dollars = int(self.for_how_much_dollars.get())



		howmuchboughtbtc = for_how_much_dollars/int(self.priceToShow) 
		howmuchboughtbtc = round(howmuchboughtbtc, self.how_much_decimals_btc)



		self.howmuchbtconaccount+=howmuchboughtbtc

		self.btcbalance.configure(text='Account balance: ' + str(self.howmuchbtconaccount) + " BTC")

		with open('howmuchbtc.txt', 'w') as f:
			f.write(str(self.howmuchbtconaccount))


		self.howmuchpaidin+=for_how_much_dollars
		self.paidin.configure(text= 'Paid in on stock: $' + str(self.howmuchpaidin))

		with open('howmuchpaidin.txt', 'w') as f:
			f.write(str(self.howmuchpaidin))




		self.for_how_much_dollars.delete(0, END)

		print('zakupiono ')

	def sellBTC(self):



		for_how_much_dollars = int(self.for_how_much_dollars.get())

		if for_how_much_dollars<=self.myactualbtcvalue:

			# zatrzymac odswiezanie ceny na moment bo mi sie wwalala w obliczenia
			self.root.after_cancel(self.odswiezanie)
			import time
			time.sleep(1) # zeby zadne poprzednie wywolanie funkcji zmieniajacej kurs sie na pewno nie wywolalo



			howmuchsoldbtc = for_how_much_dollars/int(self.priceToShow)
			howmuchsoldbtc = round(howmuchsoldbtc, self.how_much_decimals_btc)
			#print('sprzedajemy')
			#print(howmuchsoldbtc)

			#print('aktualnie na koncie bylo')
			#print(self.howmuchbtconaccount)




			self.howmuchbtconaccount -= howmuchsoldbtc

			#print('teraz bedzie')
			#print(self.howmuchbtconaccount)

			self.howmuchbtconaccount = round(self.howmuchbtconaccount, self.how_much_decimals_btc)

			#print('teraz bedzie')
			#print(self.howmuchbtconaccount)

			self.howmuchbtconaccount = '{:.7f}'.format(self.howmuchbtconaccount)
			#self.howmuchbtconaccount = float(self.howmuchbtconaccount)
			self.btcbalance.configure(text='Account balance: ' + str(self.howmuchbtconaccount) + " BTC")

			with open('howmuchbtc.txt', 'w') as f:
				f.write(str(self.howmuchbtconaccount))

			self.howmuchpaidfrom+=for_how_much_dollars
			self.paidfrom.configure(text= 'Paid from the stock: $' + str(self.howmuchpaidfrom))

			with open('howmuchpaidfrom.txt', 'w') as f:
				f.write(str(self.howmuchpaidfrom))


			self.for_how_much_dollars.delete(0, END)






			self.howmuchbtconaccount = float(self.howmuchbtconaccount)		


			myactualbtcvalue = self.howmuchbtconaccount*self.priceToShow


			myactualbtcvalue = round(myactualbtcvalue, 2)
			self.currentbtcvalue.configure(text='Current value of BTC: $' + str(myactualbtcvalue))







			self.odswiezanie = self.root.after(1000, self.btcpriceactual)

		else:
			print('nie masz tyle')



	def btcpriceactual(self):
		self.price = cryptocompare.get_price('BTC', currency='USD')
		self.priceToShow = self.price.get("BTC").get("USD")
		#print(self.priceToShow)

		self.label_current_btc_price.configure(text="1 BTC = " + str(self.priceToShow) + " USD")


		# zmieniamy aktualna wartosc moich btc

		self.myactualbtcvalue = self.howmuchbtconaccount*self.priceToShow


		self.myactualbtcvalue = round(self.myactualbtcvalue, 2)
		self.currentbtcvalue.configure(text='Current value of BTC: $' + str(self.myactualbtcvalue))


		# aktualizujemy bilans
		self.balance_variable = self.myactualbtcvalue + self.howmuchpaidfrom - self.howmuchpaidin
		self.balance_variable = round(self.balance_variable, 2)

		self.balance.configure(text='Balance: $' + str(self.balance_variable))



		self.odswiezanie = self.root.after(1000, self.btcpriceactual)





App()