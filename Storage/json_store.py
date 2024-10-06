from .store import Store
import json
from pathlib import Path
from enum import Enum
from Notifier.console_notifier import ConsoleNotifier

class ActionType(Enum):

    SAVE = "save"
    UPDATE = "update"



class JSONStorage(Store):

    def __init__(self, file_path: str) -> None:
        self.file_path = Path(file_path).resolve()
        self.existing_data = None
        self.notifier = ConsoleNotifier()
        self.load_data()
    

    def load_data(self):
        try:
            if not self.existing_data:
                with open(self.file_path, "r") as f:
                    self.existing_data =  json.load(f)
            return self.existing_data
        except FileNotFoundError:
            raise {"Error": "File not found"}
    
    def compare_data(self, new_data):
        diff = []
        if new_data:
            for product_name, product in new_data.items():
                if product_name not in self.existing_data:
                    diff.append({
                        "product": product,
                        "type": ActionType.SAVE.value
                    })
                elif product_name in self.existing_data and product != self.existing_data[product_name]:
                    diff.append({
                        "product": product,
                        "updated_price": product.get("price"),
                        "action_type": ActionType.UPDATE.value
                    })
        return diff

    def transform_data_and_save(self, data):
        processed_data = {}
        for idx, product in enumerate(data):
            product["idx"] = idx
            processed_data[ product.get("product_title") ] = product
        return processed_data
    
    def generate_report_and_notify(self, newly_scraped_data, processed_data):
        report = self.compare_data(processed_data)
        self.notifier.notify(newly_scraped_data, report)

    async def save_data(self, data):
        if not data:
            print("MSG:: No data Scraped")
            return
        processed_data = self.transform_data_and_save(data)
        self.generate_report_and_notify(data, processed_data)

        with open(self.file_path, "w") as f:
            json.dump(processed_data, f, indent=4)

    
        
        
        