# Config Updater

A simple tool to update/override cfg (ini) files from build scripts or CI pipelines via parameters: I've participated in a few projects where config files were generated during build steps by third-party components, and sometimes (mainly for testing purposes), we need to update the final version of configs.

### Project limitations:
- Python 3.8 (it's the default version for most versions of popular Linux distros)

---

### Usage:
```text
usage: config-updater [-h] file key=value [key=value ...]

positional arguments:
  file        Config filename
  key=value   List of key-value pairs to override config values

optional arguments:
  -h, --help  show this help message and exit
```

---
