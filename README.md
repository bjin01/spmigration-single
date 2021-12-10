# spmigration-single - updated for SUMA 4.2.x with python3
auto service pack migration for single server

__Updates from July 2021__
The updated script works with python3 and SUSE Manager 4.x
Additionally I made an improvement for input parameters. Instead of providing hostname, user and password in commandline we use a config file written in yaml.
The yaml config file provides the host, user and password for login to SUSE Manager API. This way if you setup crontab jobs the password is not exposed in crontab.

__Updates from July 2020__
added new argument ```-t``` for type of targets, either traditional or salt. If not salt then target online status will not be checked.

__Usage__:
__dryrun:__
```# python3 sp-migration.py -c /root/suma_config.yaml -t traditional -newbase sle-product-sles15-sp2-pool-x86_64 -fromsp sp1 -tosp sp2 -m myhost.test.com -d```

__execution:__
```python3 sp-migration.py -c /root/suma_config.yaml -t traditional -x -newbase sle-product-sles15-sp2-pool-x86_64 -fromsp sp1 -tosp sp2 -m myhost.test.com -d```

__help:__
```
# python sp-migration.py -h
usage: PROG [-h] [--config CONFIG] [-x] -t SYSTEM_TYPE
            [-newbase NEW_BASE_CHANNEL] [-fromsp MIGRATE_FROM_SERVICEPACK]
            [-tosp MIGRATE_TO_SERVICEPACK] -m MINION [-d]

This scripts runs service pack migration for given base channel. 

Sample command:

    python3 sp-migration.py -c /root/suma_config.yaml -t traditional -newbase sles12-sp4-pool-x86_64 -m zsles12sp3-test.bo2go.home -fromsp sp3 -tosp sp4 -d

If -x is not specified the SP Migration is always a dryRun.

This scripts runs service pack migration for given base channel. 

Sample command:

    # python3 sp-migration.py -s localhost -u bjin -p suse1234 -t traditional 
    -newbase  sle-product-sles15-sp2-pool-x86_64 -fromsp sp1 -tosp sp2 -m caasp02.bo2go.home -dn     
If -x is not specified the SP Migration is always a dryRun.

optional arguments:
  -h, --help            show this help message and exit
  --config CONFIG       Enter the config file name that contains login and
                        channel information e.g. /root/suma_config.yaml
  -x, --execute_migration
  -t SYSTEM_TYPE, --system_type SYSTEM_TYPE
                        Enter type of your target systems, either traditional
                        or salt, default is salt
  -newbase NEW_BASE_CHANNEL, --new_base_channel NEW_BASE_CHANNEL
                        Enter the new base channel label. e.g.
                        sles12-sp4-pool-x86_64
  -fromsp MIGRATE_FROM_SERVICEPACK, --migrate_from_servicepack MIGRATE_FROM_SERVICEPACK
                        Enter the current service pack version e.g. sp3 of
                        course you can jump from sp3 to sp5 as well.
  -tosp MIGRATE_TO_SERVICEPACK, --migrate_to_servicepack MIGRATE_TO_SERVICEPACK
                        Enter the target service pack version e.g. sp4 of
                        course you can jump from sp3 to sp5 as well.
  -m MINION, --minion MINION
                        Enter the target minion id e.g. myhost.test.com .
  -d, --debug
  ```
  
