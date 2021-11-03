class UnauthorizedError(Exception):
    pass


class AccountIsBannedError(Exception):
    pass


class EAlreadyExist(Exception):
    pass


class GoneError(Exception):
    pass


class UnknownError(Exception):
    pass


class NotFoundError(Exception):
    pass
