import os
import sys
from datetime import datetime


_LOGGER_INITIALIZED = False


class _TimestampTee:
    def __init__(self, original_stream, log_file_handle):
        self._original_stream = original_stream
        self._log_file_handle = log_file_handle
        self._buffer = ""

    def write(self, data):
        try:
            self._original_stream.write(data)
        except Exception:
            pass

        self._buffer += data
        while "\n" in self._buffer:
            line, self._buffer = self._buffer.split("\n", 1)
            if line.strip() == "":
                timestamped = f"{_now_str()} \n"
            else:
                timestamped = f"{_now_str()} {line}\n"
            try:
                self._log_file_handle.write(timestamped)
                self._log_file_handle.flush()
            except Exception:
                pass

    def flush(self):
        try:
            self._original_stream.flush()
        except Exception:
            pass
        if self._buffer:
            line = self._buffer
            self._buffer = ""
            timestamped = f"{_now_str()} {line}"
            try:
                self._log_file_handle.write(timestamped)
                self._log_file_handle.flush()
            except Exception:
                pass

    def isatty(self):
        try:
            return self._original_stream.isatty()
        except Exception:
            return False


def _now_str():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def init_logger(log_filename: str | None = None):
    global _LOGGER_INITIALIZED
    if _LOGGER_INITIALIZED:
        return

    base_dir = os.path.dirname(os.path.abspath(__file__))
    log_dir = os.path.join(base_dir, "log")
    try:
        os.makedirs(log_dir, exist_ok=True)
    except Exception:
        pass

    if not log_filename:
        log_filename = "app"

    logfile_path = os.path.join(log_dir, f"{log_filename}.log")

    try:
        log_fh = open(logfile_path, "a", encoding="utf-8")
    except Exception:
        # 回退到当前工作目录
        log_fh = open(os.path.join(os.getcwd(), f"{log_filename}.log"), "a", encoding="utf-8")

    sys.stdout = _TimestampTee(sys.stdout, log_fh)
    sys.stderr = _TimestampTee(sys.stderr, log_fh)

    _LOGGER_INITIALIZED = True


