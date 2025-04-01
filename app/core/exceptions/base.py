from enum import IntEnum


class HttpStatusCode(IntEnum):
    NOT_FOUND = 404


class BaseServiceException(Exception):
    message: str
    status_code: HttpStatusCode

    def __init_subclass__(cls, **kwargs):
        for attr in ('message', 'status_code'):
            if not hasattr(cls, attr):
                raise TypeError(
                    f'Class {cls.__name__} must define "{attr}" class attribute.'
                )
        super().__init_subclass__(**kwargs)

    def __new__(cls, *args, **kwargs):
        if cls is BaseServiceException:
            raise TypeError(
                f'BaseServiceException class must not have own instances.'
            )
        return super().__new__(cls)

    def __str__(self):
        return self.message


class EntityMessage:
    def __set_name__(self, owner, name):
        self.name = name

    def __get__(self, obj, owner):
        if obj is None:
            entity = owner.__dict__.get(self.name)
            return f"{entity.capitalize()} not found" if entity else None
        return getattr(obj, self.name)
