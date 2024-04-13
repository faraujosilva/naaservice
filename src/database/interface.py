from abc import ABC, abstractmethod


class IDatabase(ABC):
    """Abstract class for all databases."""
    @abstractmethod
    def get(self):
        """Get method to retrieve data from the database."""

    @abstractmethod
    def create(self):
        """Create method to insert data into the database."""

    @abstractmethod
    def update(self):
        """Update method to update data in the database."""

    @abstractmethod
    def delete(self):
        """Delete method to delete data from the database."""
