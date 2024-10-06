from abc import ABC, abstractmethod

class Store(ABC):

    @abstractmethod
    def load_data(self):
        pass
    
    @abstractmethod
    def save_data(self):
        pass