import contextlib
from abc import ABC

class DbAdapterException(Exception):
    pass

class DbAdapter(ABC):
    @contextlib.contextmanager
    def transaction(self):
        raise NotImplementedError
    
    @contextlib.contextmanager
    def nested_transaction(self):
        raise NotImplementedError
    
    @contextlib.contextmanager
    def destroy_db(self):
        raise NotImplementedError
    
    @contextlib.contextmanager
    def init_db(self):
        NotImplementedError

    @contextlib.contextmanager
    def rollback(self):
        NotImplementedError    