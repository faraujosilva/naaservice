from abc import ABC, abstractmethod

class IDatabase(ABC):
    @abstractmethod
    def get(self):
        pass
    
    @abstractmethod
    def create(self):
        pass
    
    @abstractmethod
    def update(self):
        pass
    
    @abstractmethod
    def delete(self):
        pass