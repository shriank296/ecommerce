class UniqueConstraintViolation(Exception):
    pass

class DbIntegrityError(Exception):
    pass

class DbException(Exception):
    pass

class RecordNotFound(DbException):
    pass