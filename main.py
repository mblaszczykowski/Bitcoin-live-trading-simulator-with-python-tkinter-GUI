from tkinter import *
import cryptocompare

class App:
	def __init__(self):
		self.root = Tk()
		self.root.geometry("650x345")
		self.root.title("Bitcoin live trading simulator")
		self.root.resizable(False, False) 

		self.bgcolor = "#323232"
		self.root.configure(background=self.bgcolor)

		self.how_much_decimals_btc = 7

		try:
			with open('howmuchpaidin.txt', 'r') as f:
				self.howmuchpaidin = float(f.read())
		except:
			self.howmuchpaidin = 0.0

		try:
			with open('howmuchbtc.txt', 'r') as f:
				self.howmuchbtconaccount = float(f.read())
		except:
			self.howmuchbtconaccount = 0.0

		try:
			with open('howmuchpaidfrom.txt', 'r') as f:
				self.howmuchpaidfrom = float(f.read())
		except:
			self.howmuchpaidfrom = 0.0


		self.summary = Label(self.root, text='Summary', font=("Poppins", 15, "bold"))
		self.summary.place(x=410,y=30)

		self.paidin = Label(self.root, text='Paid in on stock: $' + str(self.howmuchpaidin), font=("Poppins", 14))
		self.paidin.place(x=410,y=55)

		self.btcbalance = Label(self.root, text='Account balance: ' + str(self.howmuchbtconaccount) + " BTC", highlightcolor=self.bgcolor, activebackground=self.bgcolor, font=("Poppins", 14))
		self.btcbalance.place(x=410, y=80)

		self.currentbtcvalue = Label(self.root, text='Current value of BTC: $0', font=("Poppins", 14))
		self.currentbtcvalue.place(x=410,y=105)

		self.paidfrom = Label(self.root, text='Paid from the stock: $' + str(self.howmuchpaidfrom), font=("Poppins", 14))
		self.paidfrom.place(x=410,y=130)

		self.balance_variable = 0
		self.balance = Label(self.root, text='Balance: $0', font=("Poppins", 14))
		self.balance.place(x=410, y=155)

		self.balancelabel = Label(self.root, text='(current BTC value + paid from - paid in)', font=("Poppins", 11))
		self.balancelabel.place(x=410, y=180)

		self.reset_stats_button = Button(self.root, text='Reset', command=self.reset)
		self.reset_stats_button.place(x=410, y=235)

		self.current_btc_price = Label(self.root, text='Current BTC price', font=("Poppins", 17, "bold"))
		self.current_btc_price.place(x=120,y=65)

		self.label_current_btc_price = Label(self.root, text="", font=("Poppins", 20, "bold"))
		self.label_current_btc_price.place(x=88,y=100)

		self.label_how_much_btc = Label(self.root, text='For how much $ (int)', font=("Poppins", 14))
		self.label_how_much_btc.place(x=120, y=160)
		self.for_how_much_dollars = Entry(self.root, font=("Poppins", 16, "bold"), width=10)
		self.for_how_much_dollars.place(x=128, y=195)

		self.buybutton = Button(self.root, text='Buy', command=self.buyBTC, activebackground='black', highlightcolor='black')
		self.buybutton.place(x=120,y=235)

		self.sellbutton = Button(self.root, text='Sell', command=self.sellBTC)
		self.sellbutton.place(x=202,y=235)

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
		try:
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
		except:
			print("Write value")

	def sellBTC(self):

		try:
			for_how_much_dollars = int(self.for_how_much_dollars.get())

			if for_how_much_dollars<=self.myactualbtcvalue:

				# We are stopping updating BTC price because it disturbs our calculations
				self.root.after_cancel(self.odswiezanie)

				import time
				time.sleep(1) # To be sure that none of previous functions changing btc price will not execute

				howmuchsoldbtc = for_how_much_dollars/int(self.priceToShow)
				howmuchsoldbtc = round(howmuchsoldbtc, self.how_much_decimals_btc)

				self.howmuchbtconaccount -= howmuchsoldbtc

				self.howmuchbtconaccount = round(self.howmuchbtconaccount, self.how_much_decimals_btc)

				self.howmuchbtconaccount = '{:.7f}'.format(self.howmuchbtconaccount)
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
				print('You dont have that amount of BTC')
		except:
			print("Write value")

	def btcpriceactual(self):
		self.price = cryptocompare.get_price('BTC', currency='USD')
		self.priceToShow = self.price.get("BTC").get("USD")

		self.label_current_btc_price.configure(text="1 BTC = " + str(self.priceToShow) + " USD")

		# Changing actual price of our BTC
		self.myactualbtcvalue = self.howmuchbtconaccount*self.priceToShow

		self.myactualbtcvalue = round(self.myactualbtcvalue, 2)
		self.currentbtcvalue.configure(text='Current value of BTC: $' + str(self.myactualbtcvalue))

		# Updating balance
		self.balance_variable = self.myactualbtcvalue + self.howmuchpaidfrom - self.howmuchpaidin
		self.balance_variable = round(self.balance_variable, 2)

		self.balance.configure(text='Balance: $' + str(self.balance_variable))

		self.odswiezanie = self.root.after(1000, self.btcpriceactual)

App()