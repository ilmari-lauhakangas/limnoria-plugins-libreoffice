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

import supybot.conf as conf
import supybot.registry as registry
from supybot.i18n import PluginInternationalization, internationalizeDocstring
_ = PluginInternationalization('Welcome')

def configure(advanced):
    # This will be called by supybot to configure this module.  advanced is
    # a bool that specifies whether the user identified themself as an advanced
    # user or not.  You should effect your configuration by manipulating the
    # registry as appropriate.
    from supybot.questions import expect, anything, something, yn
    Welcome = conf.registerPlugin('Welcome', True)
    bots = anything("Space-separated list of bots we should ignore")
    welcomeMessage = something("Welcome message", default="Welcome $newcomer! I thought I'd say hello, and ping some people so they know you're here (like $greeter_string). I'm a bot! If no one responds for a while, relax and stay in the channel. Please look at the channel topic for helpful advice.")
    waitPeriod = something("Seconds we should wait until welcoming a newcomer", default=60)
    conf.supybot.plugins.Welcome.bots.set(bots)
    conf.supybot.plugins.Welcome.welcomeMessage.set(welcomeMessage)
    conf.supybot.plugins.Welcome.waitPeriod.set(waitPeriod)

Welcome = conf.registerPlugin('Welcome')
# This is where your configuration variables (if any) should go.  For example:
# conf.registerGlobalValue(Welcome, 'someConfigVariableName',
#     registry.Boolean(False, _("""Help for someConfigVariableName.""")))
conf.registerChannelValue(Welcome, 'greeters',
    registry.SpaceSeparatedListOfStrings('', _("People to notify of a newcomer in the welcome message.")))
conf.registerGlobalValue(Welcome, 'bots',
    registry.SpaceSeparatedListOfStrings('', _("Ignore these bots when determining, if the channel is quiet.")))
conf.registerGlobalValue(Welcome, 'welcomeMessage',
    registry.String("Welcome $newcomer! I thought I'd say hello, and ping some people so they know you're here (like $greeter_string). I'm a bot! If no one responds for a while, relax and stay in the channel. Please look at the channel topic for helpful advice.", _("Welcome message.")))
conf.registerGlobalValue(Welcome, 'waitPeriod',
    registry.PositiveInteger(60, _("Indicates how many seconds the bot will wait until welcoming a new nick.")))

# vim:set shiftwidth=4 softtabstop=4 expandtab textwidth=79:
