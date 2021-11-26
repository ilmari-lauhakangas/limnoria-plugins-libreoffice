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
_ = PluginInternationalization('QuitAlert')

def configure(advanced):
    # This will be called by supybot to configure this module.  advanced is
    # a bool that specifies whether the user identified themself as an advanced
    # user or not.  You should effect your configuration by manipulating the
    # registry as appropriate.
    from supybot.questions import expect, anything, something, yn
    QuitAlert = conf.registerPlugin('QuitAlert', True)
    quitters = anything("Space-separated list of nicks we should monitor")
    alertees = anything("Space-separated list of nicks we should alert")
    alertMessage = something("Alert message", default="{alertees}: alert, {quitter} has disconnected!")
    alertChannel = anything("Channel for receiving the alert")
    conf.supybot.plugins.QuitAlert.quitters.set(quitters)
    conf.supybot.plugins.QuitAlert.alertees.set(alertees)
    conf.supybot.plugins.QuitAlert.alertMessage.set(alertMessage)
    conf.supybot.plugins.QuitAlert.alertChannel.set(alertChannel)

QuitAlert = conf.registerPlugin('QuitAlert')
# This is where your configuration variables (if any) should go.  For example:
# conf.registerGlobalValue(QuitAlert, 'someConfigVariableName',
#     registry.Boolean(False, _("""Help for someConfigVariableName.""")))
conf.registerGlobalValue(QuitAlert, 'quitters',
    registry.SpaceSeparatedListOfStrings('', _("Monitor quits of these nicks.")))
conf.registerGlobalValue(QuitAlert, 'alertees',
    registry.SpaceSeparatedListOfStrings('', _("People to alert.")))
conf.registerGlobalValue(QuitAlert, 'alertMessage',
    registry.String("{alertees}: alert, {quitter} has disconnected!", _("The alert message.")))
conf.registerGlobalValue(QuitAlert, 'alertChannel',
    registry.String('', _("Channel to send the alert to.")))

# vim:set shiftwidth=4 softtabstop=4 expandtab textwidth=79:
