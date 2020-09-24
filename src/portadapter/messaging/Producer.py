from abc import ABC, abstractmethod


class Producer(ABC):
    """Message producer to the message broker

    """

    @abstractmethod
    def simpleProducer(self, obj: object, objMap: callable, schema: str):
        """Send message to the message broker

        Args:
            obj (object): The object model that is needed to be sent
            objMap (callable): A function that will be called by the system in order to get a json representation for
            the data to be sent
            schema (str): The schema that will be used for data validation

        """
        pass

    def transactionalProducer(self, obj: object, objMap: callable, schema: str, transactionalId: str):
        """Send message to the message broker using a transactional id

        Args:
            obj (object): The object model that is needed to be sent
            objMap (callable): A function that will be called by the system in order to get a json representation for
            the data to be sent
            schema (str): The schema that will be used for data validation
            transactionalId (str): This is the transactional id used in message broker transaction

        """
        pass
