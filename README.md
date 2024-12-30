# Config Updater

A simple tool to update/override cfg (ini) files from build scripts or CI pipelines via parameters: I've participated in
a few projects where config files were generated during build steps by third-party components, and sometimes (mainly for
testing purposes), we need to update the final version of configs.


---

### Usage:

```text
Usage: config-updater FILE COMMAND [ARGS]...

  A simple tool to update/override cfg (ini) files.

Options:
  --help  Show this message and exit.

Commands:
  remove  Remove config fields if existed.
  update  Update (override) or add config fields.
```

---
