### How to run

``` bash
sudo nano /etc/systemd/system/ai_parody_store.service
```

```
[Unit]
Description=ai_parody_store

[Service]
WorkingDirectory=%DIR%
ExecStart=%DIR%/env/bin/python store_messages.py
Restart=always

[Install]
WantedBy=multi-user.target
```

``` bash
sudo systemctl start ai_parody_store
sudo systemctl status ai_parody_store
sudo systemctl enable ai_parody_store
```
