from gdb.scm import BaseScm
import re

#  lldb specifics

class LldbScm(BaseScm):
    def __init__(self, vim, cursor, win):
        super().__init__(vim, cursor, win)

        self.addTrans(self.paused,  re.compile(r'^Process \d+ resuming'),     self.pausedContinue)
        self.addTrans(self.paused,  re.compile(r' at ([^:]+):(\d+)'),     self.pausedJump)
        self.addTrans(self.paused,  re.compile(r'\(lldb\) '),                 self.queryB)
        self.addTrans(self.running, re.compile(r'^Breakpoint \d+:'),          self.queryB)
        self.addTrans(self.running, re.compile(r'^Process \d+ stopped'),      self.queryB)
        self.addTrans(self.running, re.compile(r'\(lldb\) '),                 self.queryB)

        self.state = self.running


def init():
    return { 'initScm': LldbScm,
             'delete_breakpoints': 'breakpoint delete',
             'breakpoint': 'b',
             'until {}': 'thread until {}' }