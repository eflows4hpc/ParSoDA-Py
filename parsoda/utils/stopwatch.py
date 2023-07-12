import time


def current_time_millis() -> int:
    """
    Returns the current timestamp, i.e. the number of milliseconds since 1 January 1970 00:00:00
    :return: the current timestamp in milliseconds as an integer
    """
    return int(round(time.time_ns()/1_000_000))


class StopWatch:
    def __init__(self):
        self.__start_time = current_time_millis()
        self.__pause_time = None

    def get_and_reset(self) -> int:
        current_time = self.get()
        self.reset()
        return current_time

    def reset(self) -> None:
        self.__start_time = current_time_millis()
        self.__pause_time = None

    def is_paused(self) -> bool:
        return self.__pause_time is not None

    def pause(self) -> None:
        if self.__pause_time is None:
            self.__pause_time = current_time_millis() - self.__start_time

    def resume(self) -> None:
        if self.__pause_time is not None:
            self.__start_time = current_time_millis() - self.__pause_time
            self.__pause_time = None

    def get(self) -> int:
        if self.__pause_time is not None:
            return self.__pause_time
        else:
            return current_time_millis() - self.__start_time
