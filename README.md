# spmigration-single
auto service pack migration for single server

__Updates from July 2020__
added new argument ```-t``` for type of targets, either traditional or salt. If not salt then target online status will not be checked.

__Usage__:
__dryrun:__
```# python sp-migration.py -s localhost -u bjin -p suse1234 -t traditional -newbase sle-product-sles15-sp2-pool-x86_64 -fromsp sp1 -tosp sp2 -m myhost.test.com -d```

__execution:__
```python sp-migration.py -s localhost -u bjin -p suse1234 -t traditional -x -newbase sle-product-sles15-sp2-pool-x86_64 -fromsp sp1 -tosp sp2 -m myhost.test.com -d```

__help:__
```
# python sp-migration.py -h
usage: PROG [-h] [-x] -s SERVER -u USERNAME -p [PASSWORD] -t SYSTEM_TYPE
            [-newbase NEW_BASE_CHANNEL] [-fromsp MIGRATE_FROM_SERVICEPACK]
            [-tosp MIGRATE_TO_SERVICEPACK] -m MINION [-d]

This scripts runs service pack migration for given base channel. 

Sample command:

    python sp-migration.py -s localhost -u bjin -p suse1234 -t traditional -newbase sles12-sp4-pool-x86_64 -m zsles12sp3-test.bo2go.home -fromsp sp3 -tosp sp4 -d

If -x is not specified the SP Migration is always a dryRun.

optional arguments:
  -h, --help            show this help message and exit
  -x, --execute_migration
  -s SERVER, --server SERVER
                        Enter your suse manager host address e.g.
                        myserver.abd.domain
  -u USERNAME, --username USERNAME
                        Enter your suse manager loginid e.g. admin
  -p [PASSWORD]         Enter your password
  -t SYSTEM_TYPE, --system_type SYSTEM_TYPE
                        Enter type of your target systems, either traditional
                        or salt, default is salt
  -newbase NEW_BASE_CHANNEL, --new_base_channel NEW_BASE_CHANNEL
                        Enter the new base channel label. e.g. sles12-sp4
                        -pool-x86_64
  -fromsp MIGRATE_FROM_SERVICEPACK, --migrate_from_servicepack MIGRATE_FROM_SERVICEPACK
                        Enter the current service pack version e.g. sp3 of
                        course you can jump from sp3 to sp5 as well.
  -tosp MIGRATE_TO_SERVICEPACK, --migrate_to_servicepack MIGRATE_TO_SERVICEPACK
                        Enter the target service pack version e.g. sp4 of
                        course you can jump from sp3 to sp5 as well.
  -m MINION, --minion MINION
                        Enter the target minion id e.g. myhost.richemont.com .
  -d, --debug
  ```
  
