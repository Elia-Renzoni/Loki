# Loki
Linux Container Runtime for Fun and Profit

## Command Line Arguments
```bash
loki create-image --path=<project path> \
                  --dir=<working dir> \
                  --run=<command> \
                  --run=<command> \
                  ...
                  --cmd=<exec>
```

```bash
loki build
```

```bash
loki run --name=<container-name>
```

```bash
loki stop --name=<container-name>
```
