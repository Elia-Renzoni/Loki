# Loki
Linux Container Runtime for Fun and Profit

## Command Line Arguments
* container image:
```bash
loki build --name=pyapp \
  --run="pip install flask" \
  --copy=./src:/app \
  --workdir=/app \
  --expose=5000 \
  --cmd="python main.py"
```

* run a container:
```bash
loki run --d \
  --name=myapp \
  --env=DB_HOST=localhost \
  --env=DB_PORT=5432 \
  --mount=/data:/app/data \
  --port=8080:80 \
```

* simple management:
```bash
loki ps
loki start myapp
loki stop myapp
loki rm myapp
loki images
```

