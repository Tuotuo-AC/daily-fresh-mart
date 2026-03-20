# 使用官方 Python 基础镜像
FROM python:3.11-slim

# 设置工作目录
WORKDIR /app

# 复制依赖文件并安装
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 复制项目代码
COPY . .

# 暴露 Django 默认端口
EXPOSE 8000

# 启动命令（可根据需要调整）
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
