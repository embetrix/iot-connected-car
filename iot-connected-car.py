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
import obd 
import json
import time 
import sys
import configuration as cfg
from pubnub.pnconfiguration import PNConfiguration
from pubnub.pubnub import PubNub
from obd import OBDStatus
from obd import OBDCommand

pnconfig = PNConfiguration()
pnconfig.publish_key = cfg.pubkey
pnconfig.subscribe_key = cfg.subkey
pnconfig.ssl = True

obd_data = '{"rpm": "", "speed": "" }'
obd_json= json.loads(obd_data)
 
pubnub = PubNub(pnconfig)

def callback_rpm(r):
    obd_json['rpm'] = r.value.magnitude

def callback_speed(s):
    obd_json['speed'] = s.value.magnitude
  
connection = obd.Async(cfg.obdport)
connection.watch(obd.commands.RPM, callback=callback_rpm)
connection.watch(obd.commands.SPEED, callback=callback_speed)
connection.start()

if not connection.is_connected():
    print 'ODB connection failed!'
    sys.exit(1)

try:
    while(True):
        pubnub.publish().channel(cfg.channel).message(obd_json).sync()
        time.sleep(0.5)

except Exception, e:
    print 'Error :' + str(e)
    sys.exit(0)
