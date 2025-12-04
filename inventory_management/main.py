# Candy Inventory Management System

class CandyInventory:
    def __init__(self):
        # Initialize inventory as a dictionary with dates as keys
        self.inventory = {}

    def add_candy(self, date, candy_type, quantity):
        """
        Add candy to the inventory.
        :param date: Date in 'YYYY-MM-DD' format
        :param candy_type: Type of candy (e.g., 'chocolate', 'gummy')
        :param quantity: Quantity of candy to add
        """
        if date not in self.inventory:
            self.inventory[date] = {}
        if candy_type not in self.inventory[date]:
            self.inventory[date][candy_type] = 0
        self.inventory[date][candy_type] += quantity

    def remove_candy(self, date, candy_type, quantity):
        """
        Remove candy from the inventory.
        :param date: Date in 'YYYY-MM-DD' format
        :param candy_type: Type of candy
        :param quantity: Quantity of candy to remove
        """
        if date in self.inventory and candy_type in self.inventory[date]:
            self.inventory[date][candy_type] -= quantity
            if self.inventory[date][candy_type] <= 0:
                del self.inventory[date][candy_type]
            if not self.inventory[date]:
                del self.inventory[date]

    def get_inventory(self, date):
        """
        Get the inventory for a specific date.
        :param date: Date in 'YYYY-MM-DD' format
        :return: Dictionary of candy types and their quantities
        """
        return self.inventory.get(date, {})

    def display_inventory(self):
        """
        Display the entire inventory.
        """
        for date, candies in self.inventory.items():
            print(f"Date: {date}")
            for candy_type, quantity in candies.items():
                print(f"  {candy_type}: {quantity}")

if __name__ == "__main__":
    inventory = CandyInventory()

    # Example usage
    inventory.add_candy("2025-12-03", "chocolate", 10)
    inventory.add_candy("2025-12-03", "gummy", 5)
    inventory.remove_candy("2025-12-03", "chocolate", 3)

    print("Inventory for 2025-12-03:")
    print(inventory.get_inventory("2025-12-03"))

    print("\nFull Inventory:")
    inventory.display_inventory()