Automatic lock cleanup is implemented through
a Django custom management command
(clear_expired_locks), intended to run
periodically via a scheduler (cron/Render job).

The command identifies active seat locks
whose expiration time has passed and marks
them as expired automatically, ensuring
timely seat release without manual refresh.