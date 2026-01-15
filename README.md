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
loki run -d \
  --name=myapp \
  -e=DB_HOST=localhost \
  -e=DB_PORT=5432 \
  -v=/data:/app/data \
  -p=8080:80 \
  -w=/app \
  webapp:v1
```

* simple management:
```bash
loki ps
loki start myapp
loki stop myapp
loki rm myapp
loki images
```

