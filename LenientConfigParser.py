__author__ = 'mariusmetzger'

from ConfigParser import RawConfigParser

class LenientConfigParser(RawConfigParser):

    def add_section(self, section):
        if not self.has_section(section):
            RawConfigParser.add_section(self, section)

    def get(self, section, option, add_if_failed = True):
        try:
            return RawConfigParser.get(self, section, option)
        except:
            if add_if_failed:
                self.set(section, option, None)
            return None

    def set(self, section, option, value=None):
        if not self.has_section(section):
            RawConfigParser.add_section(self, section)
        RawConfigParser.set(self, section, option, value)