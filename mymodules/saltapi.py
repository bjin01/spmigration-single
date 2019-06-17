#!/usr/bin/python
import salt.config,  sys
import salt.client

def saltping(hostnames):
    master_opts = salt.config.client_config('/etc/salt/master.d/susemanager.conf')
    local = salt.client.LocalClient()
    if hostnames is dict:
        for x in hostnames:
            try:
                ret = local.cmd(x, 'test.ping')
            except:
                print("salt test.ping failed.")
                sys.exit(1)
    else:
        ret = local.cmd(hostnames, 'test.ping')
        
    #print(ret)
    if ret:
        for v,  w in ret.items():
            print("Is server %s online?:" %(v))
            if w == True:
                print("\t Yes. %s" %(w))
            else:
                print("\tVery bad, No. %s" %(w) )
                sys.exit(1)
    else:
        print("Sminion online check failed.")
        sys.exit(1)
    return
