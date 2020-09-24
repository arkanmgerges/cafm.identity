from abc import ABC, abstractmethod


class Consumer(ABC):
    """Message consumer to the message broker

    """
    @abstractmethod
    def produce(self, obj: object, objMap: callable, schema: str):
        """Consume messages from the message broker

        Args:
            obj (object): The object model that is needed to be sent
            objMap (callable): A function that will be called by the system in order to get a json representation for
            the data to be sent
            schema (str): The schema that will be used for data validation

        """
        pass
