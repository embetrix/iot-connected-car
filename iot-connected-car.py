# (C) Copyright 2017
#
# Embexus Embedded Systems Solutions, ayoub.zaki@embexus.com
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License as
# published by the Free Software Foundation; either version 2 of
# the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.	 See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston,
# MA 02111-1307 USA
#
from pubnub.pnconfiguration import PNConfiguration
from pubnub.pubnub import PubNub
from obd import OBDStatus
import obd
import time
import settings as s

pnconfig = PNConfiguration()

pnconfig.publish_key = s.pubkey
pnconfig.subscribe_key = s.subkey

Data = [{'a': 1828292992, 'b': 727277272}]
 
pubnub = PubNub(pnconfig)

#obd.logger.setLevel(obd.logging.DEBUG)
 
connection = obd.OBD(s.obdport) 


while True:
        cmd = obd.commands.RPM # select an OBD command (sensor)
 
        response = connection.query(cmd, force=True) # send the command
 
        print(response)

        pubnub.publish().channel(s.channel).message(Data).sync()
 
        time.sleep(1)
