# The MIT License (MIT)
#
# Copyright (c) 2021 Ilmari Lauhakangas
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import sys

from supybot.commands import *
import supybot.irclib as irclib
import supybot.ircmsgs as ircmsgs
import supybot.plugins as plugins
import supybot.callbacks as callbacks
from supybot.i18n import PluginInternationalization, internationalizeDocstring
_ = PluginInternationalization('QuitAlert')

class QuitAlert(callbacks.Plugin):
    """This plugin alerts people when certain nicks quit."""
    noIgnore = True
    def __init__(self, irc):
        self.__parent = super(QuitAlert, self)
        self.__parent.__init__(irc)

    def die(self):
        self.__parent.die()

    def __call__(self, irc, msg):
        self.__parent.__call__(irc, msg)

    def _getRealIrc(self, irc):
        if isinstance(irc, irclib.Irc):
            return irc
        else:
            return irc.getRealIrc()

    def doQuit(self, irc, msg):
        quitters = self.registryValue('quitters')
        if not quitters:
            return
        irc = self._getRealIrc(irc)
        if msg.nick in quitters:
            alert = self.registryValue('alertMessage').format(
                quitter = msg.nick,
                alertees = ', '.join(self.registryValue('alertees'))
            )
            m = ircmsgs.privmsg(self.registryValue('alertChannel'), alert)
            irc.queueMsg(m)

Class = QuitAlert

# vim:set shiftwidth=4 softtabstop=4 expandtab textwidth=79:
