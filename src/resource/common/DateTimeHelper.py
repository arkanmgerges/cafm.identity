"""
@author: Arkan M. Gerges<arkan.m.gerges@gmail.com>
"""


class DateTimeHelper:
    @classmethod
    def utcNow(cls) -> int:
        """Return current utc time in milliseconds

        Returns:
             int: Current UTC time in milliseconds
        """
        import datetime
        epoch = datetime.datetime(1970, 1, 1, 0, 0, 0)
        now = datetime.datetime.utcnow()
        return round((now - epoch).total_seconds() * 1000)
