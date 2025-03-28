

class ClothingStore:
    def _init_(self, inventory_file="inventory.json", sales_file="sales.json"):
        self.inventory_file=inventory_file
        self.sales_file=sales_file
        self.inventory=self.load_inventory()
        self.sales=self.load_sales()
    
    def load_inventory(self):
        try:
            with open(self.inventory_file,"r") as file:
                return json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            return{}
    
    def load_sales(self):
        try:
            with open(self.sales_file,"r") as file:
                return json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            return []
    
    def save_inventory(self):
        with open(self.inventory_file,"w") as file:
            json.dump(self.inventory, file, indent=4)
    
    def save_sales(self):
        with open(self.sales_file,"w") as file:
            json.dump(self.sales,file,indent=4)
    
    def add_item(self):
        item_id=input("Enter Item ID: ")
        name=input("Enter Item Name: ")
        category=input("Enter Category: ")
        price=float(input("Enter Price: "))
        quantity=int(input("Enter Quantity: "))
        if item_id in self.inventory:
            print(f"Item ID {item_id} already exists. Updating quantity instead.")
            self.inventory[item_id]['quantity'] += quantity
        else:
            self.inventory[item_id]={'name':name,'category':category,'price': price,'quantity': quantity}
        self.save_inventory()
        print(f"Added/Updated {quantity} {name}(s) to inventory.")
    
    def sell_item(self):
        item_id=input("Enter Item ID to sell: ")
        quantity=int(input("Enter Quantity: "))
        customer_name=input("Enter Customer Name: ")
        
        if item_id not in self.inventory:
            print(f"Item ID {item_id} not found in inventory.")
            return False
        
        if self.inventory[item_id]['quantity'] < quantity:
            print(f"Not enough stock. Only {self.inventory[item_id]['quantity']} available.")
            return False
        
        self.inventory[item_id]['quantity'] -= quantity
        self.save_inventory()
        
        total_price = self.inventory[item_id]['price'] * quantity
        self.sales.append({'item_id':item_id,'item_name':self.inventory[item_id]['name'],'quantity':quantity,'total_price':total_price,'customer_name':customer_name})
        self.save_sales()
        print(f"Sold {quantity} {self.inventory[item_id]['name']}(s) to {customer_name} for ${total_price:.2f}")
        return True
    
    def check_stock(self):
        print("\nCurrent Inventory:")
        print("{:<5} {:<20} {:<15} {:<10} {:<5}".format("ID", "Name", "Category", "Price", "Qty"))
        print("-"*60)
        for item_id, item in self.inventory.items():
            print("{:<5} {:<20} {:<15} ${:<9.2f} {:<5}".format(item_id, item['name'], item['category'], item['price'], item['quantity']))
    
    def view_sales(self):
        print("\nSales History:")
        print("{:<20} {:<20} {:<5} {:<10}".format("Customer", "Item", "Qty", "Total Price"))
        print("-"*60)
        for sale in self.sales:
            print("{:<20} {:<20} {:<5} ${:<9.2f}".format(sale['customer_name'], sale['item_name'], sale['quantity'], sale['total_price']))
        total_sales = sum(sale['total_price'] for sale in self.sales)
        print(f"\nTotal Sales: ${total_sales:.2f}")

def main():
    store = ClothingStore()
    while True:
        print("\n1. Add Item")
        print("2. Sell Item")
        print("3. Check Stock")
        print("4. View Sales")
        print("5. Exit")
        choice = input("Enter your choice: ")
        if choice == '1':
            store.add_item()
        elif choice == '2':
            store.sell_item()
        elif choice == '3':
            store.check_stock()
        elif choice == '4':
            store.view_sales()
        elif choice == '5':
            break
        else:
            print("Invalid choice. Please try again.")

if _name_ == "_main_":
    main()
