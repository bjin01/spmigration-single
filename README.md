# spmigration-single
auto service pack migration for single server

__Usage__:
__dryrun:__
```python spmigration.py -s bjsuma.bo2go.home -u bjin -p suse1234 -newbase dev-sles12-sp4-pool-x86_64 -m zsles12sp3-test.bo2go.home -fromsp sp3 -tosp sp4 --debug```

__execution:__
```python sp-migration.py -s localhost -u bjin -p suse1234 -newbase sles12-sp4-pool-x86_64 -m zsles12sp3-test.bo2go.home -fromsp sp3 -tosp sp4 -d```

__help:__
```
# python sp-migration.py -h
usage: PROG [-h] [-x] -s SERVER -u USERNAME -p [PASSWORD]
            [-newbase NEW_BASE_CHANNEL] [-fromsp MIGRATE_FROM_SERVICEPACK]
            [-tosp MIGRATE_TO_SERVICEPACK] -m MINION [-d]

This scripts runs service pack migration for given base channel. 

Sample command:

    python sp-migration.py -s localhost -u bjin -p suse1234 -newbase sles12-sp4-pool-x86_64 -m zsles12sp3-test.bo2go.home -fromsp sp3 -tosp sp4 -d

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
  
