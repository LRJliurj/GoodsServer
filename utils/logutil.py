
#__status__ = "Development"

#__all__ = ['set_logger', 'debug', 'info', 'warning', 'error','critical', 'exception']

import os
import sys
import traceback
import logging
import logging.handlers

class ColoredFormatter(logging.Formatter):
    '''A colorful formatter.'''

    def __init__(self, fmt=None, datefmt=None):
        logging.Formatter.__init__(self, fmt, datefmt)

    def format(self, record):
        # Color escape string
        COLOR_RED = '\033[1;31m'
        COLOR_GREEN = '\033[1;32m'
        COLOR_YELLOW = '\033[1;33m'
        COLOR_BLUE = '\033[1;34m'
        COLOR_PURPLE = '\033[1;35m'
        COLOR_CYAN = '\033[1;36m'
        COLOR_GRAY = '\033[1;37m'
        COLOR_WHITE = '\033[1;38m'
        COLOR_RESET = '\033[1;0m'
        # Define log color
        LOG_COLORS = {
            'DEBUG': '%s',
            'INFO': COLOR_GREEN + '%s' + COLOR_RESET,
            'WARNING': COLOR_YELLOW + '%s' + COLOR_RESET,
            'ERROR': COLOR_RED + '%s' + COLOR_RESET,
            'CRITICAL': COLOR_RED + '%s' + COLOR_RESET,
            'EXCEPTION': COLOR_RED + '%s' + COLOR_RESET,
        }
        level_name = record.levelname
        msg = logging.Formatter.format(self, record)
        return LOG_COLORS.get(level_name, '%s') % msg


class Log():
    def __init__(self, filename=None, mode='a',uuid=None,log_address=None,modelname=None,
                 cmdlevel='DEBUG',
                 filelevel='INFO',
                 cmdfmt='[%(asctime)s] %(filename)s line:%(lineno)d %(levelname)-8s%(message)s',
                 filefmt='[%(asctime)s] %(levelname)-8s%(message)s',
                 cmddatefmt='%H:%M:%S',
                 filedatefmt='%Y-%m-%d %H:%M:%S',
                 backup_count=7, limit=20480, when="D", colorful=False):
        self.filename = filename
        if self.filename is None:
            self.filename = getattr(sys.modules['__main__'], '__file__', 'log.py')
            self.filename = os.path.basename(self.filename.replace('.py', '.log'))
            # self.filename = os.path.join('/tmp', self.filename)
        # self.uuid=uuid
        self.log_address=log_address
        self.modelname=modelname
        self.mode = mode
        self.cmdlevel = cmdlevel
        self.filelevel = filelevel
        if isinstance(self.cmdlevel, str):
            self.cmdlevel = getattr(logging, self.cmdlevel.upper(), logging.DEBUG)
        if isinstance(self.filelevel, str):
            self.filelevel = getattr(logging, self.filelevel.upper(), logging.DEBUG)
        self.filefmt = filefmt
        self.cmdfmt = cmdfmt
        self.filedatefmt = filedatefmt
        self.cmddatefmt = cmddatefmt
        self.backup_count = backup_count
        self.limit = limit
        self.when = when
        self.colorful = colorful
        self.logger = None
        self.streamhandler = None
        self.filehandler = None
        if self.cmdlevel > 10:
            self.filefmt = '[%(asctime)s] %(levelname)-8s%(message)s'
            self.cmdfmt = '[%(asctime)s] %(levelname)-8s%(message)s'
            self.cmddatefmt = '%Y-%m-%d %H:%M:%S'
        # self.set_logger(cmdlevel=self.cmdlevel)

    def init_logger(self):
        '''Reload the logger.'''
        if self.logger is None:
            self.logger = logging.getLogger()
        else:
            logging.shutdown()
            self.logger.handlers = []
        self.streamhandler = None
        self.filehandler = None
        self.logger.setLevel(logging.DEBUG)

    def add_streamhandler(self):
        '''Add a stream handler to the logger.'''
        self.streamhandler = logging.StreamHandler()
        self.streamhandler.setLevel(self.cmdlevel)
        if self.colorful:
            formatter = ColoredFormatter(self.cmdfmt, self.cmddatefmt)
        else:
            formatter = logging.Formatter(self.cmdfmt, self.cmddatefmt, )
        self.streamhandler.setFormatter(formatter)
        self.logger.addHandler(self.streamhandler)

    def add_filehandler(self):
        '''Add a file handler to the logger.'''
        # Choose the filehandler based on the passed arguments
        if self.backup_count == 0:  # Use FileHandler
            self.filehandler = logging.FileHandler(self.filename, self.mode)
        elif self.when is None:  # Use RotatingFileHandler
            self.filehandler = logging.handlers.RotatingFileHandler(self.filename,
                                                                    self.mode, self.limit, self.backup_count)
        else:  # Use TimedRotatingFileHandler
            self.filehandler = logging.handlers.TimedRotatingFileHandler(self.filename,
                                                                         self.when, 1, self.backup_count)
            self.filehandler.suffix="%Y-%m-%d.log"
        self.filehandler.setLevel(self.filelevel)
        formatter = logging.Formatter(self.filefmt, self.filedatefmt, )
        self.filehandler.setFormatter(formatter)
        self.logger.addHandler(self.filehandler)

    def set_logger(self, **kwargs):
        '''Configure the logger.'''
        keys = ['mode', 'cmdlevel', 'filelevel', 'filefmt', 'cmdfmt',\
                'filedatefmt', 'cmddatefmt', 'backup_count', 'limit',\
                'when', 'colorful','log_address','modelname']
        for (key, value) in kwargs.items():
            if not (key in keys):
                return False
            setattr(self, key, value)
        self.filename=str(getattr(self,'log_address'))+'modelProject.log_'+str(getattr(self,'modelname'))+'.log'
        if isinstance(self.cmdlevel, str):
            self.cmdlevel = getattr(logging, self.cmdlevel.upper(), logging.DEBUG)
        if isinstance(self.filelevel, str):
            self.filelevel = getattr(logging, self.filelevel.upper(), logging.DEBUG)
        if not "cmdfmt" in kwargs:
            self.filefmt = '[%(asctime)s] %(filename)s line:%(lineno)d %(levelname)-8s%(message)s'
            self.filedatefmt = '%Y-%m-%d %H:%M:%S'
            self.cmdfmt = '[%(asctime)s] %(filename)s line:%(lineno)d %(levelname)-8s%(message)s'
            self.cmddatefmt = '%H:%M:%S'
            if self.cmdlevel > 10:
                self.filefmt = '[%(asctime)s] %(levelname)-8s%(message)s'
                self.cmdfmt = '[%(asctime)s] %(levelname)-8s%(message)s'
                self.cmddatefmt = '%Y-%m-%d %H:%M:%S'
        self.init_logger()
        self.add_streamhandler()
        self.add_filehandler()
        # Import the common log functions for convenient
        self.import_log_funcs()
        return True

    def import_log_funcs(self):
        '''Import the common log functions from the logger to the class'''
        log_funcs = ['debug', 'info', 'warning', 'error', 'critical',
                     'exception']
        for func_name in log_funcs:
            func = getattr(self.logger, func_name)
            setattr(self, func_name, func)

    def trace(self):
        info = sys.exc_info()
        for file, lineno, function, text in traceback.extract_tb(info[2]):
            self.error('%s line:%s in %s:%s' % (file, lineno, function, text))
        self.error('%s: %s' % info[:2])


# if __name__ == '__main__':
#     log = Log(cmdlevel='info')
#     # log = Log(cmdlevel='debug')
#     log.set_logger(cmdlevel='debug')
#     log.debug('debug')
#     log.info('debug%s' % 'haha')
#     log.error((1, 2))
#     log.error('debug')
#     log.info({'a': 1, 'b': 2})
#     os.system("pause")
#
#
#     class A():
#         def __init__(self, log):
#             self.log = log
#
#         def a(self, a):
#             self.log.info(a)
#
#
#     class B():
#         def __init__(self, log):
#             self.log = log
#
#         def b(self, a):
#             self.log.info(a)
#     a = A(log)
#     a.a("test a")
#     b = B(log)
#     b.b(5)
#     def fun(a):
#         return 10 / a
#     try:
#         a = fun(0)
#     except:
#         log.trace()