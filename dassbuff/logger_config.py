import logging
import os
from logging.handlers import TimedRotatingFileHandler

class LevelFilter(logging.Filter):
    """
    只允许特定level的日志通过
    """
    def __init__(self, level):
        super().__init__()
        self.level = level

    def filter(self, record):
        return record.levelno == self.level

def setup_loggers():
    # 确保日志目录存在
    base_dir = os.path.dirname(os.path.abspath(__file__))
    log_dir = os.path.join(base_dir, "log")
    os.makedirs(log_dir, exist_ok=True)

    # 创建一个格式化器，包含详细的日志信息
    # '%(asctime)s - %(name)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s'

    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

    # 定义日志文件的命名格式和处理器配置
    log_configs = [
        {
            'level': logging.DEBUG,
            'filename': 'debug.log',
            'when': 'midnight',  # 在午夜滚动日志
            'interval': 1,       # 每天滚动一次
            'backupCount': 30    # 保留30天的日志
        },
        {
            'level': logging.INFO,
            'filename': 'info.log',
            'when': 'midnight',  # 在午夜滚动日志
            'interval': 1,       # 每天滚动一次
            'backupCount': 30    # 保留30天的日志
        },
        {
            'level': logging.WARNING,
            'filename': 'warn.log',
            'when': 'midnight',
            'interval': 1,
            'backupCount': 30
        },
        {
            'level': logging.ERROR,
            'filename': 'error.log',
            'when': 'midnight',
            'interval': 1,
            'backupCount': 30
        }
    ]

    # 配置根日志
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.DEBUG)  # 修复：设置为DEBUG，保证debug日志能被处理

    # 先移除所有旧的handler，防止重复添加
    if root_logger.hasHandlers():
        root_logger.handlers.clear()

    # 为每个级别创建处理器
    for config in log_configs:
        # 构建日志文件路径，格式为：log/级别.log
        log_file = os.path.join(log_dir, config['filename'])

        # 创建定时滚动日志处理器
        handler = TimedRotatingFileHandler(
            log_file,
            when=config['when'],
            interval=config['interval'],
            backupCount=config['backupCount'],
            encoding='utf-8',
            utc=False
        )

        # 设置处理器的日志级别
        handler.setLevel(logging.DEBUG)  # 必须设置为DEBUG，否则高于此级别的日志不会被处理

        # 设置日志格式
        handler.setFormatter(formatter)

        # 添加过滤器，确保只处理指定级别的日志
        handler.addFilter(LevelFilter(config['level']))

        # 将处理器添加到根日志
        root_logger.addHandler(handler)

    # 可选：添加控制台输出处理器
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)
    root_logger.addHandler(console_handler)

    return root_logger

if __name__ == "__main__":
    # 初始化日志配置
    logger = setup_loggers()

    logger.debug("调试日志 - 不会在文件和CMD中显示")
    # 测试不同级别的日志
    logger.info("这是一条信息日志")
    logger.warning("这是一条警告日志")
    logger.error("这是一条错误日志")

    # 测试异常日志（会被归类到error级别）
    try:
        1 / 0
    except Exception as e:
        logger.error("捕获到异常: %s", e, exc_info=True)

    print("日志测试完成，查看log目录下的日志文件")
