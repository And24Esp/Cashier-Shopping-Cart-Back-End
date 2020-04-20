#1st, I'll import required 1st party (built-in) modules, and define global variables:
import os, time, sys
from datetime import date

transaction_counter = 0

#2nd, I'll write the program's classes, with its respective attributes and methods:
class PointOfSale:

    def __init__(self):     #Inventory will be uploaded using the classe's contructor.

        # This function will help to obtain the point of sale's inventory:
        def delete_punct(text_line):
            """ Returns a list of strings without undesired punctuation"""
            my_substitutions = 'stringtype'.maketrans(":,$", "   ")    
            cleaned_text = text_line.translate(my_substitutions)
            product_info = cleaned_text.split()
            
            return product_info

        # Here, I'll collect all the information from the inventory text file,
		# clean it up using delete_punct(), tranform some data from strings to 
		# integers and floats, and store all these into a python dictionary: 
        cleaned_str = [] 
        inventory_dict = {}
        
        Inventory_file = open("Inventory.txt","r")
        
        counter = 0
        for line in Inventory_file:
            new_line = delete_punct(line)
            new_line[1] = int(new_line[1])
            new_line[2] = float(new_line[2])
            new_line[3] = float(new_line[3])
            cleaned_str.append(new_line)
            inventory_dict.update({cleaned_str[counter][0] : cleaned_str[counter][1:]})
            counter += 1
        
        Inventory_file.close()
        
        self.inventory = inventory_dict


class CustomerShoppingCart:

    def __init__(self, PoS, cust_type):
        """PoS attribute must refer to a PointOfSale object type.
		   cust_type must be either RC (Regular Customer) or RM (Rewards Member)."""
        self.point_of_sale = PoS
        self.customer_type = cust_type
        self.items_cart = {}

    def add_to_cart(self, item_name, req_qty):
        if self.point_of_sale.inventory[item_name][0] >= req_qty:
            self.point_of_sale.inventory[item_name][0] -= req_qty
            self.items_cart.update({item_name : self.point_of_sale.inventory[item_name][0:]})
            self.items_cart[item_name][0] = req_qty
        else:
            print('Error. Required quantity is greater than available inventory.')
            pass

    def rem_from_cart(self, item_name, req_qty):
        if self.items_cart[item_name][0] >= req_qty:
            self.items_cart[item_name][0] -= req_qty
            self.point_of_sale.inventory[item_name][0] += req_qty
        else:
            print('Error. Required quantity is greater than quantity in cart.')
            pass

    def empty_cart(self):
        self.items_cart = {}
        
    def checkout(self, cash):       #Cash paid
        today = date.today()
        t_date = today.strftime("%B %d, %Y")  # t_date refers to today's date        
        
        global transaction_counter
        transaction_counter += 1
        trans_n = transaction_counter # trans_n refers to transaction number
        
        tot_items = 0
        for v in self.items_cart.values():
            tot_items += v[0]
        
        TE_subtotal = 0        #Tax-Exempt sub-total
        for v in self.items_cart.values():
            if self.customer_type == 'RC':
                if v[3] == 'Tax-Exempt':
                    TE_subtotal += round(v[0] * v[1], 2)
                else:
                    continue    
            if self.customer_type == 'RM':
                if v[3] == 'Tax-Exempt':
                    TE_subtotal += round(v[0] * v[2], 2)
                else:
                    continue    

        T_subtotal = 0        #Taxable sub-total
        for v in self.items_cart.values():
            if self.customer_type == 'RC':
                if v[3] == 'Taxable':
                    T_subtotal += round(v[0] * v[1], 2)
                else:
                    continue    
            if self.customer_type == 'RM':
                if v[3] == 'Taxable':
                    T_subtotal += round(v[0] * v[2], 2)
                else:
                    continue

        tax = round(T_subtotal * 0.065, 2)

        total = TE_subtotal + T_subtotal + tax

        if total <= cash:
            change = round(cash - total, 2)
        else:
            change = 'Insufficient payment'

        return t_date, trans_n, tot_items, TE_subtotal, T_subtotal, tax, total, cash, change
    
    def print_receipts(self, checkout_tuple):        
        (t_date, trans_n, tot_items, TE_subtotal, T_subtotal, tax, total, cash, change) = checkout_tuple
        
        #Here, I'll print each required line inside the receipt text file:
        today2 = date.today()
        t_date2 = today2.strftime("%d%m%Y")
        Receipt_file = open('T00000' +str(transaction_counter) + '_' + t_date2 + '.txt','w')
        
        Receipt_file.write(t_date + '\n')
        Receipt_file.write('TRANSACTION: 00000' + str(trans_n) + '\n\n')
        
        Receipt_file.write('ITEM      QTY   UN_PR   TOTAL   \n')
        for k,v in self.items_cart.items():
            if self.customer_type == 'RC':
                Receipt_file.write(k+'\t  '+str(v[0])+'\t$'+str(v[1])+'\t$'+str(v[0]*v[1])+'\t'+'\n')
            elif self.customer_type == 'RM':
                Receipt_file.write(k+'\t  '+str(v[0])+'\t$'+str(v[2])+'\t$'+str(v[0]*v[2])+'\t'+'\n')
        
        Receipt_file.write('******************************\n')
        Receipt_file.write('TOTAL NUMBERS OF ITEMS SOLD: ' + str(tot_items) + '\n')
        Receipt_file.write('SUB-TOTAL: $' + str(TE_subtotal + T_subtotal) + '\n')
        Receipt_file.write('TAX (6.5%): $' + str(tax) + '\n')
        Receipt_file.write('TOTAL: $' + str(total) + '\n')
        Receipt_file.write('CASH: $' + str(cash) + '\n')
        Receipt_file.write('CHANGE: $' + str(change) + '\n')

        Receipt_file.close()

        #And here, I'll proceed to update the inventory text file:
        ud_inv_file = open("Inventory.txt","w")
        
        for k,v in self.point_of_sale.inventory.items():
            ud_inv_file.write(k+': '+str(v[0])+', $'+str(v[1])+', $'+str(v[2])+', '+v[3]+'\n')
        
        ud_inv_file.close()

#3rd, I'll create the add, remove, and checkout screen functions, aswell as the
# program's workflow (WARNING: THIS PART IS INCOMPLETE, IT ONLY A MOCKUP FOR NOW):
def shoppingcart_screen(ShoppingCart):
    #In this screen, the end-user will be able to control the shopping cart:
    os.system('cls')
    print('This is your Shopping Cart. Please, choose an option and press ENTER.\n')
    print('(a) Add a product to my cart.')
    print('(b) Remove a product from my cart (NOT WORKING YET).')
    print('(c) Empty my cart (NOT WORKING YET).')
    print('(d) Go to the checkout screen (NOT WORKING YET).')
    print('(q) Quit program (NOT WORKING YET).')
    choice = input("\nChoice: ")
    if choice.lower()[0] == "a":
        add_product_screen()
    else:
        shoppingcart_screen(ShoppingCart)

def add_product_screen():
    #In this screen, the end-user will be able to control the shopping cart:
    os.system('cls')
    print('Please, type the EXACT name of the product you want, and press ENTER.')
    print('Then, type the quantity of this product you want, and press ENTER.\n')
    print(jerrys_quick_mart.inventory)
    print('\nValue equivalences:')
    print('ITEM: [QUANTITY, REGULAR PRICE ($), REWARDS PRICE ($), TAX STATUS]\n')
    choice1 = input('Please choose product:')
    choice2 = input('Please choose ammount (THIS FILE WILL CLOSE AFTER THIS STEP):')
    andres_espinosa.add_to_cart(choice1, choice2)
    print(andres_espinosa.items_cart)

jerrys_quick_mart = PointOfSale()

os.system('cls')
print('Welcome to Jerrys Quick Mart! Please, choose an option and press ENTER.\n')
print('(a) I am a Regular Customer.')
print('(b) I am a Rewards Member.')
print('Press any other key to quit the program.')
choice = input("\nChoice: ")
if choice.lower()[0] == "a":
    andres_espinosa = CustomerShoppingCart(jerrys_quick_mart, 'RC')
    shoppingcart_screen(andres_espinosa)
elif choice.lower()[0] == "b":
    andres_espinosa = CustomerShoppingCart(jerrys_quick_mart, 'RM')
    shoppingcart_screen(andres_espinosa)
else:
    sys.exit()
