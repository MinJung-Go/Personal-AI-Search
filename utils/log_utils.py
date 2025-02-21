# -*- Power By FocusAIM -*-


import os
import sys
import logging
from concurrent_log_handler import ConcurrentRotatingFileHandler

LOGDIR = "log" # 日志文件目录

server_error_msg = "**NETWORK ERROR DUE TO HIGH TRAFFIC. PLEASE REGENERATE OR REFRESH THIS PAGE.**" # 服务器错误消息
moderation_msg = "YOUR INPUT VIOLATES OUR CONTENT MODERATION GUIDELINES. PLEASE TRY AGAIN." # 内容审核消息

def build_logger(logger_name, logger_filename):
    """
    创建一个日志记录器，支持并发写入日志文件，并将标准输出和标准错误重定向到日志记录器。
    
    Args:
        logger_name (str): 日志记录器的名称。
        logger_filename (str): 日志文件的名称（不包括路径）。
    
    Returns:
        logging.Logger: 创建的日志记录器对象。
    
    """
    formatter = logging.Formatter(
        fmt="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    # 设置根记录器的格式
    if not logging.getLogger().handlers:
        logging.basicConfig(level=logging.INFO)
    logging.getLogger().handlers[0].setFormatter(formatter)

    # 重定向stdout和stderr到记录器
    stdout_logger = logging.getLogger("stdout")
    stdout_logger.setLevel(logging.INFO)
    sys.stdout = StreamToLogger(stdout_logger, logging.INFO)

    stderr_logger = logging.getLogger("stderr")
    stderr_logger.setLevel(logging.ERROR)
    sys.stderr = StreamToLogger(stderr_logger, logging.ERROR)

    # 获取记录器
    logger = logging.getLogger(logger_name)
    logger.setLevel(logging.INFO)

    # 添加并发文件处理程序
    os.makedirs(LOGDIR, exist_ok=True)
    filename = os.path.join(LOGDIR, logger_filename)
    file_handler = ConcurrentRotatingFileHandler(
        filename, maxBytes=1024 * 1024 * 10,  # 10MB per file
        backupCount=10,  # Keep 10 log files
        encoding='UTF-8'
    )
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    return logger

class StreamToLogger(object):
    def __init__(self, logger, log_level=logging.INFO):
        """
        初始化对象。
        
        Args:
            logger (logging.Logger): 日志记录器对象。
            log_level (int, optional): 日志级别。默认为 logging.INFO。
        
        Returns:
            None
        """
        self.logger = logger
        self.log_level = log_level

    def write(self, buf):
        """
        将输入内容写入日志。
        
        Args:
            buf (str): 要写入日志的内容，以字符串形式传入。
        
        Returns:
            None
        
        将输入的内容逐行写入日志，每行去除前后多余的空白字符后记录。
        """
        for line in buf.rstrip().splitlines():
            self.logger.log(self.log_level, line.rstrip())

    def flush(self):
        pass 