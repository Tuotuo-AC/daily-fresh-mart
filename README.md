# 天天生鲜购物网站 (Daily Fresh Market)

基于 `Django` 框架开发的完整B2C生鲜电商购物网站。该项目是跟随网课的个人学习实战项目，深入理解和掌握Django框架在大型项目中的应用，包括商品管理、购物车、订单系统等核心电商功能。在该项目的基础上新增了用户认证功能，包括用户注册、登录、登出、忘记密码、个人中心信息管理、收货地址管理等功能。

## ✨ 主要功能

*   **用户模块**
    *   用户注册（邮箱验证码方式:打印到控制台）
    *   用户登录/登出
    *   忘记密码（邮箱验证码重置）
    *   个人中心信息管理（昵称、手机号、性别、生日）
    *   收货地址管理（设置默认地址、增删改查）
*   **商品模块**
    *   商品分类展示
    *   商品列表页（支持排序、筛选、分页）
    *   商品详情页
    *   商品搜索功能
*   **购物车模块**
    *   购物车增删改查
    *   合并登录前后购物车
    *   提交订单
*   **订单模块**
    *   确认订单页面
    *   生成订单
*   **后台管理**
    *   定制化Django Admin
    *   商品、订单、用户等数据管理

## 访问地址

| 功能     | URL                                    |
|--------|----------------------------------------|
| 首页     | `/`                                    |
| 商品列表   | `/goods/`                              |
| 商品分类页面 | 例如海鲜水产（id=2）第三页 `/goods/?cag=2&page=3` |
| 购物车    | `/cart/show_cart`                      |
| 提交订单   | `/cart/place_order/`                   |
| 注册     | `/user/register/`                      |
| 登录     | `/user/login/`                         |
| 个人中心   | `/user/profile/`                       |
| 地址管理   | `/user/address/`                       |
| 后台管理   | `/admin/`                              |

## 🛠️ 技术栈

*   **后端框架**: Python 3.11, Django 4.2
*   **数据库**: MySQL 
*   **前端**: HTML5, CSS3, JavaScript, jQuery, Ajax

## 📦 快速开始

### 环境要求
*   Python 3.11
*   pip 和 virtualenv (推荐)
*   MySQL

### 安装步骤

1.  **克隆仓库**
    ```
    git clone https://github.com/Tuotuo-AC/daily-fresh-mart.git
    cd daily-fresh-mart
    ```

2.  **创建并激活虚拟环境**
    ```
    python -m venv venv
    source venv/bin/activate  # Linux/Mac
    # venv\Scripts\activate  # Windows
    ```

3.  **安装依赖**
    ```
    pip install -r requirements.txt
    ```

4.  **配置数据库**
    *   在MySQL中创建一个数据库，例如 `dailyfresh`。
    *   复制项目中的环境变量示例文件并根据你的配置修改：
        ```
        cp .env.example .env
        # 编辑 .env 文件，填入你的数据库名、用户名、密码、Redis连接等
        ```

5.  **执行数据库迁移**
    ```
    python manage.py makemigrations
    python manage.py migrate
    ```

6.  **创建超级用户**
    ```
    python manage.py createsuperuser
    ```

7.  **收集静态文件**
    ```
    python manage.py collectstatic
    ```

8.  **运行开发服务器**
    
    ```
    python manage.py runserver
    ```
    现在，在浏览器中访问 `http://127.0.0.1:8000` 即可看到网站前台。

## 📁 项目结构

ttsx/
├── cart/                  # 购物车模块
├── goods/                 # 商品模块
├── user/                  # 用户模块
├── ttsx/                  # 项目主配置
│   ├── settings.py        # 配置文件
│   └── urls.py            # 主路由
├── templates/             # 模板文件
│   ├── user/              # 用户相关模板
│   ├── cart.html          # 购物车页面
│   ├── detail.html        # 商品详情页
│   ├── goods.html         # 商品列表页
│   ├── index.html         # 首页
│   └── place_order.html   # 订单确认页
├── static/                # 静态文件
├── manage.py
├── requirements.txt
├── dockerfile
├── docker-compose.yml
└── entrypoint.sh



## 在centos7上用docker部署本项目（适用于未添加用户模块相关功能前的版本）

**在项目根目录ttsx下准备文件dockerfile和docker-compose.yml**

```python
# dockerfile
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

```

```
#在项目根目录下创建 docker-compose.yml 文件，定义两个服务：web（Django）和 db（MySQL）
version: '3.8'

services:
  db:
    image: mysql:8.0
    container_name: ttsx-mysql
    restart: always
    environment:
      MYSQL_ROOT_PASSWORD: rootpass
      MYSQL_DATABASE: ttsxdb
      MYSQL_USER: ttsxuser
      MYSQL_PASSWORD: ttsxpass
    ports:
      - "3308:3306"   # 映射到主机3308，避免与现有MySQL冲突
    volumes:
      - ttsx-mysql-data:/var/lib/mysql   # 持久化数据
    networks:
      - ttsx-network

  web:
    build: .   # 使用当前目录的 Dockerfile 构建镜像
    container_name: ttsx-web
    restart: always
    ports:
      - "8001:8000"   # 映射到主机8001，避免与现有应用冲突
    environment:
      - DB_HOST=db
      - DB_PORT=3306
      - DB_NAME=ttsxdb
      - DB_USER=ttsxuser
      - DB_PASSWORD=ttsxpass
    depends_on:
      - db   # 确保 db 先启动，但 Django 需要等待数据库完全就绪（可能需要额外脚本）
    networks:
      - ttsx-network
    volumes:
      - .:/app   # 挂载代码以便开发时热重载（生产环境不建议）

networks:
  ttsx-network:
    driver: bridge

volumes:
  ttsx-mysql-data:

```

**调整数据库配置** 

```
# settings.py
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': os.environ.get('DB_NAME', 'ttsxdb'),
        'USER': os.environ.get('DB_USER', 'ttsxuser'),
        'PASSWORD': os.environ.get('DB_PASSWORD', 'ttsxpass'),
        'HOST': os.environ.get('DB_HOST', 'localhost'),
        'PORT': os.environ.get('DB_PORT', '3306'),
        'OPTIONS': {
        	'charset': 'utf8mb4',
            'ssl': {'disabled': True} # 禁用 SSL
        }
    }
}

ALLOWED_HOSTS = ['*']  # 生产环境应指定域名或IP
```

#### 使用 Docker Compose 启动

**进入正确的项目目录**

```
cd /root/ttsx
```

**在项目根目录执行**：

```python
docker-compose up -d 
```

- `-d` 表示后台运行。
- 首次执行会构建 Django 镜像，并拉取 MySQL 镜像，然后启动容器。

**查看运行状态**：

```
docker-compose ps或docker ps -a
```

应该看到两个服务状态均为 `**Up**`。

------

#### 执行数据库迁移和创建超级用户

容器启动后，Django 数据库尚未创建表，需要执行迁移命令：

```
# 进入 web 容器执行迁移
docker-compose exec web python manage.py migrate

# 创建超级用户（可选）
docker-compose exec web python manage.py createsuperuser
```

如果项目有静态文件，还需收集：

```
docker-compose exec web python manage.py collectstatic --noinput
```

#### 防火墙放行8001端口

```
sudo firewall-cmd --add-port=8001/tcp --permanent
sudo firewall-cmd --reload # 重新加载防火墙配置
sudo firewall-cmd --list-ports # sudo firewall-cmd --list-ports
```

#### 导入数据库文件

**在项目根目录**ttsx下

**将 SQL 文件复制到 MySQL 容器中**

```
docker cp categories.sql ttsx-mysql:/tmp/
docker cp goodsinfo.sql ttsx-mysql:/tmp/
```

**进入 MySQL 容器执行导入**

```
docker-compose exec db bash
```

**然后在容器内执行**：

```
mysql -uroot -p ttsxdb < /tmp/categories.sql
mysql -uroot -p ttsxdb < /tmp/goodsinfo.sql
```

输入密码 `rootpass`。

**验证数据**

在 MySQL 容器内（或通过 `docker-compose exec db mysql -uroot -p` 进入）执行：

```sql
USE ttsxdb;
SELECT COUNT(*) FROM goods_goodsinfo;
```

#### 访问网站

打开浏览器，访问 `http://ip地址:8001/index`

**常用命令**

```
systemctl start docker 启动docker容器
docker images 查看镜像
docker ps -a 查看容器状态
docker stop 容器
docker restart 容器
docker-compose logs web 查看 web 容器的日志
```



在虚拟机重启后，Django 容器再次出现 `Connection refused` 错误，根本原因是 **Django 容器启动时 MySQL 尚未完全就绪**。虽然 `docker-compose.yml` 中设置了 `depends_on: - db`，但这只确保 MySQL **容器已启动**（即 `docker container start` 完成），并不能保证 MySQL 服务已经初始化完成并可以接受连接。MySQL 容器启动后通常需要几秒到几十秒来初始化数据、执行恢复等，这段时间内如果 Django 尝试连接，就会得到 `Connection refused`，导致 Django 退出，然后被 `restart: always` 策略反复重启。

------

#### 解决方案：为 Django 添加数据库等待脚本

您需要修改项目，让 Django 在启动前等待 MySQL 就绪。以下是最简便的方法

#### 1. 在项目根目录创建 `entrypoint.sh`

```
vi entrypoint.sh
```

内容如下：

```
#!/bin/sh
echo "Waiting for database..."
while ! nc -z db 3306; do
  sleep 1
done
echo "Database is ready."
python manage.py migrate --noinput   # 可选的，自动运行迁移
exec python manage.py runserver 0.0.0.0:8000
```

保存并退出（`:wq`）。

#### 2. 赋予执行权限

```
chmod +x entrypoint.sh
```

#### 3. 修改 dockerfile

在 `dockerfile` 末尾添加：

```
COPY entrypoint.sh .
RUN chmod +x entrypoint.sh
CMD ["./entrypoint.sh"]

完整的 Dockerfile 看起来应该是这样
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

# 新添加的部分
RUN apt-get update && apt-get install -y netcat-openbsd
COPY entrypoint.sh .
RUN chmod +x entrypoint.sh

CMD ["./entrypoint.sh"]
```

#### 4. 重新构建并启动容器

```
docker-compose down
docker-compose up -d --build
```

#### 验证启动

查看日志，确认 web 容器已等待并成功连接：

```
docker-compose logs web --tail=20
```

应该看到类似：

```
Waiting for database...
Database is ready.
Operations to perform...
```

然后访问 `http://服务器ip:8001` 检查网站是否正常。
