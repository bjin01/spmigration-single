import fnmatch
import json
import salt.config
import salt.utils.event,  salt.utils.json,  salt.output
import pprint

#def parse_jobresults(data):
#    y = json.loads(data)
#    print(json.dumps(data, indent = 4, sort_keys=True))
#    return
    
opts = salt.config.client_config('/etc/salt/master.d/susemanager.conf')

sevent = salt.utils.event.get_event(
        'master',
        sock_dir=opts['sock_dir'],
        transport=opts['transport'],
        opts=opts)

while True:
    ret = sevent.get_event(full=True)
    #salt.output.pprint_out(ret)
    if ret is None:
        continue

    if fnmatch.fnmatch(ret['tag'], 'salt/job/*/ret/*'):
        pydata = pprint.pformat(json.loads(json.dumps(ret['data'])))
        print(pydata)
        for x in pydata:
            print(x[0]['id'])
