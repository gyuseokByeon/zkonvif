# coding: utf-8
import json
import thread, time
import urllib,urllib2,sys
from CardServer import livingS
from RecordingCommand import RecordingCommand

sys.path.append('../')
from common.utils import zkutils

def StartLiving():
    rc = {}
    rc['result'] = 'ok'
    rc['info'] = ''
    try:
        req = urllib2.Request('http://192.168.12.117:50001/repeater/prepublish')
        data = {}
        _utils = zkutils()
        data['mac'] = _utils.mymac()
        data['uid'] = _utils.mymac() + 'Living1'
        data['STATUS'] = '0'
        data = json.dumps(data)

        response = urllib2.urlopen(req,data)
        content = json.load(response)
        url = content['content']['rtmp_repeater']
        print url

        livingS(url)
        time.sleep(1)
        _rcmd = RecordingCommand()
        rc=_rcmd.send_command('BroadCastCmd=StartBroadCast')
        if rc['result'] == 'ok':
            rc['info'] = url
        return rc

    except Exception as err:
        rc['result'] = 'error'
        rc['info'] = str(err)
        return rc

def StopLiving():
    _rcmd = RecordingCommand()
    rc=_rcmd.send_command('BroadCastCmd=StopBroadCast')
    return rc

