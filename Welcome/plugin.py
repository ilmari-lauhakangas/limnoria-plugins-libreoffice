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

import re
import os
import sys
import time
import sqlite3
import threading
from string import Template

import supybot.conf as conf
import supybot.utils as utils
import supybot.ircdb as ircdb
import supybot.ircmsgs as ircmsgs
from supybot.commands import *
import supybot.plugins as plugins
import supybot.ircutils as ircutils
import supybot.callbacks as callbacks
from supybot.i18n import PluginInternationalization
_ = PluginInternationalization('Welcome')

class WelcomeDB(object):
    __slots__ = ('engine', 'filename', 'dbs',)
    def __init__(self, filename):
        self.filename = filename
        self.engine = None

    def close(self):
        self.dbs.clear()

    def makeDbName(self, filename):
        filename = os.path.basename(filename)
        dirname = conf.supybot.directories.data.dirize('global')
        if not os.path.exists(dirname):
            os.makedirs(dirname)
        return os.path.join(dirname, filename)

    def get_db(self):
        if self.engine:
            engine = self.engine
        else:
            filename = self.makeDbName(self.filename)
            exists = os.path.exists(filename)
            engine = sqlite3.connect(filename, check_same_thread=False)
            if not exists:
                cursor = engine.cursor()
                cursor.execute("""CREATE TABLE nicks (
                        id INTEGER PRIMARY KEY,
                        name TEXT UNIQUE ON CONFLICT REPLACE)""")
                engine.commit()
            self.engine = engine
        assert engine.execute("select 1").fetchone() == (1,)
        return engine

    def has_nick(self, name):
        db = self.get_db()
        return self.get_db().cursor() \
                .execute("""SELECT COUNT() as count
                            FROM nicks WHERE name = ?;""", (name,)) \
                .fetchone()[0]

    def add_nick(self, name):
        if self.has_nick(name):
            return False
        db = self.get_db()
        cursor = db.cursor()
        cursor.execute("""INSERT INTO nicks VALUES (
            NULL, ?);""", (name,))
        db.commit()

class Welcome(callbacks.Plugin):
    """
    This plugin welcomes newcomers.
    """
    threaded = True

    def __init__(self, irc):
        self.__parent = super(Welcome, self)
        self.__parent.__init__(irc)
        filename = conf.supybot.directories.data.dirize('Welcome.sqlite3.db')
        self._db = WelcomeDB(filename)

    def clean_nick(self, nick):
        """ Cleans a nickname of decorators/identifiers. """
        status = re.search(r'_(afk|away|brb|off)$|\[m.*$', nick)
        if status:
            stat_len = len(status.group(0))
            nick = nick[:-stat_len]

        nick = nick.rstrip('_1234567890')
        """Returns same nick if '|' is absent"""
        nick = nick.split('|', 1)[0]
        nick = nick.lower()
        return nick

    def historyDiff(self, history, time):
        """Returns the history from the wait period."""
        return [h for h in history if h.time and h.time > time]

    def nickDiff(self, history, nick):
        """Returns the current nick in case it was changed during
        the wait period."""
        for i, h in enumerate(history):
            if h.command == 'NICK' and h.nick == nick:
                return self.nickDiff(history[i+1:], h.args[0])
        return nick

    def processNewcomer(self, irc, msg):
        """Taking potential nick changes during wait period into account
        requires cleaning the nick both before and after waiting.
        We store the clean nick, but welcome and query the state of the
        unclean nick."""
        silent = False
        lastTime = irc.state.history[-1].time
        ownNick = conf.supybot.nick()
        greeters = self.registryValue('greeters', msg.channel)
        bots = self.registryValue('bots')
        clean_nick = self.clean_nick(msg.nick)
        if self._db.has_nick(clean_nick):
            return False        
        time.sleep(self.registryValue('waitPeriod'))
        history = irc.state.history
        newMessages = self.historyDiff(history, lastTime)
        nick = self.nickDiff(newMessages, msg.nick)
        clean_nick = self.clean_nick(nick)
        """Don't welcome or add to db, if disconnected"""
        if not nick in irc.state.channels[msg.channel].users:
            return
        """Add to db, but don't welcome, if there were non-bot messages
        during the wait period."""
        speech = [m for m in newMessages if m.channel == msg.channel and m.command == "PRIVMSG" and m.nick not in bots + [nick, msg.nick, ownNick]]
        if speech:
            silent = True
        """If there are no greeters assigned to the channel, add to db, but don't welcome."""
        if self._add_nick(clean_nick) and greeters and not silent:
            welcomeMessage = Template(self.registryValue('welcomeMessage')).substitute(
                newcomer=nick,
                greeter_string=utils.str.commaAndify(greeters)
            )
            m = ircmsgs.privmsg(msg.channel, welcomeMessage)
            irc.queueMsg(m)

    def doJoin(self, irc, msg):
        """Have to start a thread as bot is paused until doJoin finishes."""
        t = threading.Thread(target = self.processNewcomer, args = (irc, msg))
        t.start()

    def _add_nick(self, nick):
        if self._db.has_nick(nick):
            return False
        self._db.add_nick(nick)
        return True

Class = Welcome

# vim:set shiftwidth=4 softtabstop=4 expandtab textwidth=79:
