from injector import Module, Injector


class AppDi(Module):
    """
    Dependency injection module of the app

    """


instance = Injector([AppDi])
