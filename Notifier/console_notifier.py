from .notifier import Notifier, NotifierType

class ConsoleNotifier(Notifier):

    def __init__(self) -> None:
        self.notifier_type = NotifierType.CONSOLE.value
    
    def format_report(self, scraped_data, diff):
        total_scraped_data = len(scraped_data)
        updated_products = 0
        new_products = 0
        for product in diff:
            from Storage.json_store import ActionType
            if product.get("action_type") == ActionType.UPDATE.value:
                updated_products += 1
            else:
                new_products += 1
        message = f"UPDATED PRODUCTS: {updated_products} \nNEW PRODUCTS: {new_products} \nTOTAL SCRAPED PRODUCTS: {total_scraped_data}"
        return message
        
    
    def notify(self, scraped_data, diff):
        msg = self.format_report(scraped_data, diff)
        print(f"{self.notifier_type.upper()} :: ")
        print(msg)
        print()