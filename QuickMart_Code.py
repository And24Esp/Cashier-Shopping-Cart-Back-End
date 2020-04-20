#1st: I'll import required 1st party (built-in) modules, and define global variables:
import os, time, sys
from datetime import date

transaction_counter = 0

#2nd: I'll write the program's classes, with its respective attributes and methods:
class PointOfSale:

    def __init__(self):   #Inventory will be uploaded using the classe's contructor.

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

        print('The receipt has been printed and the inventory updated. Check your files.')

#3rd: I'll demostrate how to run the code from an IDE that can interpretate python:
# This is how you create a point of sale, no parameters are needed:
jerrys_quick_mart = PointOfSale()     

# This is how you visualize (inside the IDE's terminal) the uploaded inventory:
print(jerrys_quick_mart.inventory)

#This is how you create a Customer, the parameter must be either
# the string RC (Regular Customer) or RM (Rewards Member).
andres_espinosa = CustomerShoppingCart(jerrys_quick_mart, 'RC') 

#This is how you add products to the cart, the 2 required parameters
# are the exact product name (consider uppercases) and the required quantity:
andres_espinosa.add_to_cart('Milk',4)
andres_espinosa.add_to_cart('RedBull',6)
andres_espinosa.add_to_cart('Flour',10)
andres_espinosa.add_to_cart('Sugar',3)
print(andres_espinosa.items_cart)   #Print to visualize the actual products in the cart.

#If the quiantity required is greater than the one available in the inventory,
# a noticication will be printed in the terminal, and the item won't be added to the cart:
andres_espinosa.add_to_cart('Sugar',3000)

#This is how you remove products to the cart, like when adding, the 2 required parameters
# are the exact product name (consider uppercases) and the required quantity:
andres_espinosa.rem_from_cart('Milk',2)
andres_espinosa.rem_from_cart('RedBull',3)
andres_espinosa.add_to_cart('Sugar',1)
print(andres_espinosa.items_cart)   #Print to visualize the actual products in the cart.

#This is how you empty the cart, no parameters are needed:
andres_espinosa.empty_cart()
print(andres_espinosa.items_cart)   #Print to visualize that the cart is empty.

#Finally, this is how you checkout and print the transaction receipt, the required 
# parameter is the amount of cash to be paid (first, we add some items to the cart):
andres_espinosa.add_to_cart('Milk',4)
andres_espinosa.add_to_cart('RedBull',6)
andres_espinosa.add_to_cart('Flour',10)
andres_espinosa.add_to_cart('Sugar',3)
print(andres_espinosa.items_cart)   #Print to visualize that the cart is empty.
andres_espinosa.print_receipts(andres_espinosa.checkout(60))

#It's done! The transaction receipt was created in the same directory where QuickMart_Code.py 
# is located, and the Inventory.txt file was automatically updated with the new inventory.