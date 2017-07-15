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
import settings as s
from pubnub.pnconfiguration import PNConfiguration
from pubnub.pubnub import PubNub
from obd import OBDStatus
from obd import OBDCommand

pnconfig = PNConfiguration()
pnconfig.publish_key = s.pubkey
pnconfig.subscribe_key = s.subkey
pnconfig.ssl = True

obd_data = '{"rpm": "na", "speed": "na" }'
obd_json= json.loads(obd_data)
 
pubnub = PubNub(pnconfig)

connection = obd.OBD(s.obdport)

if connection.status() != OBDStatus.CAR_CONNECTED:
    sys.exit()

while True:
    rpm   = connection.query(obd.commands.RPM)
    speed = connection.query(obd.commands.SPEED)
 
    if not rpm.is_null() and not speed.is_null():
        obd_json['rpm'] = rpm.value.magnitude
        obd_json['speed'] = speed.value.magnitude
        print obd_json
        pubnub.publish().channel(s.channel).message(obd_json).sync()
 
    time.sleep(1)
