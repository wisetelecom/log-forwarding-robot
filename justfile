default: dev-server

app := "src.main:app"

alias i := install
alias l := lint

set positional-arguments

# 安装依赖
install:
    uv sync
    pre-commit install --install-hooks

# 统一代码风格
lint:
    ruff check --fix .
    ruff format .

# 运行开发服务器
dev-server:
    python set_webhook.py
    uvicorn --reload --reload-dir ./src {{app}} --host 0.0.0.0 --port 8000

# 运行生产服务器
prod-server: check-prod-server
    gunicorn -k uvicorn.workers.UvicornWorker {{app}}

# 检查生产服务器配置
check-prod-server:
    gunicorn --print-config {{app}}
