#!/usr/bin/python

import argparse, getpass, textwrap, sys, time, os, yaml
from datetime import datetime
from mymodules import newoptchannels, saltapi
from xmlrpc.client import ServerProxy, Error, DateTime

class Password(argparse.Action):
    def __call__(self, parser, namespace, values, option_string):
        if values is None:
            values = getpass.getpass()

        setattr(namespace, self.dest, values)

child_channels = []
directory = '/var/log/spmigration/'

def get_login(path):
    
    if path == "":
        path = os.path.join(os.environ["HOME"], "suma_config.yaml")
    with open(path) as f:
        login = yaml.load_all(f, Loader=yaml.FullLoader)
        for a in login:
            login = a

    return login

def login_suma(login):
    MANAGER_URL = "https://"+ login['suma_host'] +"/rpc/api"
    MANAGER_LOGIN = login['suma_user']
    MANAGER_PASSWORD = login['suma_password']
    SUMA = "http://" + login['suma_user'] + ":" + login['suma_password'] + "@" + login['suma_host'] + "/rpc/api"
    with ServerProxy(SUMA) as session_client:

    #session_client = xmlrpclib.Server(MANAGER_URL, verbose=0)
        session_key = session_client.auth.login(MANAGER_LOGIN, MANAGER_PASSWORD)
    return session_client, session_key

def suma_logout(session, key):
    session.auth.logout(key)
    return

def checktarget_channel(client,  key,  sid,  new_base_channel):
    valid = False
    try:
        subscribablechannels = client.channel.listAllChannels(key)
    except AssertionError as error:
        print('An error happened while getting channels list')
        print(error)
    #print("Subscribable channels are: ")
    if subscribablechannels:
        for s in subscribablechannels:
            #print("\t" + s['label'])
            if s['label'] == new_base_channel:
                valid = True
    else:
        print("The new base channel has not been found. Exiting...")
        sys.exit(1)
    return valid

def create_dirs():
    if not os.path.exists(directory):
        os.makedirs(directory)
    return directory
    
def writedata_to_file(minion_name,  logmessage):
    try:
        dirname = create_dirs()
    except AssertionError as e:
        print(e)
    filename = dirname + minion_name
    try:
        f = open(filename, "w")
        f.write(logmessage)
        f.close()
    except AssertionError as e:
        print(e)
    return filename
    

def main():
    parser = argparse.ArgumentParser()
    #parser.add_argument("-v", "--verbosity", action="count", default=0)
    parser = argparse.ArgumentParser(prog='PROG', formatter_class=argparse.RawDescriptionHelpFormatter, description=textwrap.dedent('''\
    This scripts runs service pack migration for given base channel. 
    
    Sample command:
    
        # python sp-migration.py -s localhost -u bjin -p suse1234 -t traditional 
        -newbase  sle-product-sles15-sp2-pool-x86_64 -fromsp sp1 -tosp sp2 -m caasp02.bo2go.home -dn \
    
    If -x is not specified the SP Migration is always a dryRun.
     '''))
    parser.add_argument("--config", help="Enter the config file name that contains login and channel information e.g. /root/suma_config.yaml",  required=False)
    parser.add_argument("-x", "--execute_migration", action="store_true")
    
    parser.add_argument("-t", "--system_type", help="Enter type of your target systems, either traditional or salt, default is salt", default='salt', required=False)
    parser.add_argument("-newbase", "--new_base_channel", help="Enter the new base channel label. e.g. sles12-sp4-pool-x86_64 ",  required=False)
    parser.add_argument("-fromsp", "--migrate_from_servicepack", help="Enter the current service pack version e.g. sp3\n of course you can jump from sp3 to sp5 as well.",  required=False)
    parser.add_argument("-tosp", "--migrate_to_servicepack", help="Enter the target service pack version e.g. sp4\n of course you can jump from sp3 to sp5 as well.",  required=False)
    parser.add_argument("-m", "--minion", help="Enter the target minion id e.g. myhost.test.com\n.",  required=True)
    parser.add_argument("-d", "--debug", dest='debug', default=False, action='store_true')
    args = parser.parse_args()
    
    DEBUG = args.debug
    """ MANAGER_URL = "http://"+ args.server+"/rpc/api"
    MANAGER_LOGIN = args.username
    MANAGER_PASSWORD = args.password
    client = xmlrpclib.Server(MANAGER_URL, verbose=0)
    key = client.auth.login(MANAGER_LOGIN, MANAGER_PASSWORD) """
    """ today = datetime.today()
    earliest_occurrence = xmlrpclib.DateTime(today) """
    
    nowlater = datetime.now()
    earliest_occurrence = DateTime(nowlater)
    if args.config:
        suma_data = get_login(args.config)
        client, key = login_suma(suma_data)
    else:
        conf_file = "/root/suma_config.yaml"
        suma_data = get_login(conf_file)
        client, key = login_suma(suma_data)

    def log(s):
        if DEBUG:
            print(s)
    
    if args.execute_migration:
        dryRun = 0
    else:
        dryRun = 1

    target_minion = args.minion    
    new_base_channel = args.new_base_channel
    
    previous_sp = args.migrate_from_servicepack
    new_sp = args.migrate_to_servicepack
    
    serverid = client.system.getId(key, target_minion)
    if not serverid:
        print("target host %s not found in suse manager." %(target_minion))
        sys.exit(1)
        
    for s in serverid:
        sid = s['id']
        no_packages = str(s['outdated_pkg_count'])
        log("The server ID is: %s" % (str(sid)) + "   " + s['name'])
        
        if s['outdated_pkg_count'] > 10000:
            print('BUT the system has too many outdated packages: %s' %(no_packages))
            sys.exit(1)
        else:
            print('the system has outdated packages: %s' %(no_packages))
            try:
                basechannel = client.system.getSubscribedBaseChannel(key,  sid)
            except AssertionError as error:
                print(error)
            log('Current Base Channel is: ' + basechannel['label'])
            childchannels = client.system.listSubscribedChildChannels(key,  sid)
            log('Current Child Channels are:')
            for c in childchannels:
                log("\t" +  c['label'])
                
            valid = checktarget_channel(client,  key,  sid, new_base_channel  )
            log("The given target base channel is valid: " + str(valid))

    try:
        getoptchannels = newoptchannels.getnew_optionalChannels(client, key, sid)
        
    except AssertionError as error:
        log(error)
    try:
        optionalChannels = getoptchannels.find_replace(previous_sp, new_sp)
        for c in optionalChannels:
                log("\t childs: " +  c)
    except AssertionError as error:
        log(error)
    if "salt" in args.system_type:
        saltapi.saltping(target_minion)
        
    try:
        spjob = client.system.scheduleSPMigration(key, sid,  new_base_channel,  optionalChannels,  dryRun,  earliest_occurrence)

    except AssertionError as error:
        log(error)
    
    if spjob != 0:
        listprogresssystems = client.schedule.listInProgressSystems(key, spjob)
        if listprogresssystems:
            for k in listprogresssystems:
                if k['server_id'] == sid:
                    print("Job %s is pending." %str(spjob))
                    log("Job %s is pending." %str(spjob))
                
    suma_logout(client, key)

if __name__ == "__main__":
    main()
