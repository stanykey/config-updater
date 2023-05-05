# Config Updater

Simple tool to update/override cfg (ini) files from build scripts or CI pipelines via parameters

Project limitations:
  - Python 3.8 (comes with Ubuntu 20.04)
  - Only built-in packages are allowed

---


```text
usage: config-updater [-h] file key=value [key=value ...]

positional arguments:
  file        Config filename
  key=value   List of key-value pairs to override config values

optional arguments:
  -h, --help  show this help message and exit
```

---
