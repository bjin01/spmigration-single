#!/usr/bin/python

import xmlrpclib,  argparse,  getpass,  textwrap,  sys,  time,  os
from datetime import datetime
from mymodules import newoptchannels,  saltapi

class Password(argparse.Action):
    def __call__(self, parser, namespace, values, option_string):
        if values is None:
            values = getpass.getpass()

        setattr(namespace, self.dest, values)

child_channels = []
directory = '/var/log/spmigration/'

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
    
        python sp-migration.py -s localhost -u bjin -p suse1234 -newbase sles12-sp4-pool-x86_64 -m zsles12sp3-test.bo2go.home -fromsp sp3 -tosp sp4 -d\n \
    
    If -x is not specified the SP Migration is always a dryRun.
     ''')) 
    parser.add_argument("-x", "--execute_migration", action="store_true")
    parser.add_argument("-s", "--server", help="Enter your suse manager host address e.g. myserver.abd.domain",  default='localhost',  required=True)
    parser.add_argument("-u", "--username", help="Enter your suse manager loginid e.g. admin ", default='admin',  required=True)
    parser.add_argument('-p', action=Password, nargs='?', dest='password', help='Enter your password',  required=True)
    parser.add_argument("-t", "--system_type", help="Enter type of your target systems, either traditional or salt, default is salt", default='salt', required=True)
    parser.add_argument("-newbase", "--new_base_channel", help="Enter the new base channel label. e.g. sles12-sp4-pool-x86_64 ",  required=False)
    parser.add_argument("-fromsp", "--migrate_from_servicepack", help="Enter the current service pack version e.g. sp3\n of course you can jump from sp3 to sp5 as well.",  required=False)
    parser.add_argument("-tosp", "--migrate_to_servicepack", help="Enter the target service pack version e.g. sp4\n of course you can jump from sp3 to sp5 as well.",  required=False)
    parser.add_argument("-m", "--minion", help="Enter the target minion id e.g. myhost.richemont.com\n.",  required=True)
    parser.add_argument("-d", "--debug", dest='debug', default=False, action='store_true')
    args = parser.parse_args()
    
    DEBUG = args.debug
    MANAGER_URL = "http://"+ args.server+"/rpc/api"
    MANAGER_LOGIN = args.username
    MANAGER_PASSWORD = args.password
    client = xmlrpclib.Server(MANAGER_URL, verbose=0)
    key = client.auth.login(MANAGER_LOGIN, MANAGER_PASSWORD)
    today = datetime.today()
    earliest_occurrence = xmlrpclib.DateTime(today)
    
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
    
    serverid = client.system.getId(key,  target_minion)
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
    except AssertionError as error:
        log(error)
    if "salt" in args.system_type:
        saltapi.saltping(target_minion)
        
    try:
        spjob = client.system.scheduleSPMigration(key, sid,  new_base_channel,  optionalChannels,  dryRun,  earliest_occurrence)
    except AssertionError as error:
        log(error)
    
    z = 0
    while True:
        time.sleep(5)
        if spjob != 0:
            listprogresssystems = client.schedule.listInProgressSystems(key, spjob)
            if listprogresssystems:
                for k in listprogresssystems:
                    if k['server_id'] == sid:
                        log("Job %s is pending." %str(spjob))
                        z = 1
            else:
                z = 0
        if z == 0:
            listfailedsystems = client.schedule.listFailedSystems(key, spjob)
            if listfailedsystems:
                for n in listfailedsystems:
                    if n['server_id'] == sid:
                        print("Job on %s failed with message: \n" %(target_minion))
                        logmessage = target_minion + ': failed with message' + n['message']
                        output_file = writedata_to_file(target_minion,  logmessage)
                        log(n['message'])
                        log("The output message can be found in: " + output_file)
                        sys.exit(3)
            else:
                z = 4
                    
        if z == 4:
            listsuccesssystems = client.schedule.listCompletedSystems(key, spjob)
            if listsuccesssystems:
                log(listsuccesssystems)
                for m in listsuccesssystems:
                    if m['server_id'] == sid:
                        print("Job %s finished successfully." %str(spjob))
                        logmessage = "Job " + str(spjob) + " for " + s['name'] + " finished successfully.\n\n" + m['message']
                        output_file = writedata_to_file(target_minion,  logmessage)
                        log("The output message can be found in: " + output_file)
                        sys.exit(0)
            else:
                print("Job %s is not done yet, but resulted an unknown reason." %str(spjob))
                logmessage = "Job is not done yet, but resulted an unknown reason! " + str(spjob)
                output_file = writedata_to_file(target_minion,  logmessage)
                log("The output message can be found in: " + output_file)
                sys.exit(1)
                
    client.auth.logout(key)

if __name__ == "__main__":
    main()
