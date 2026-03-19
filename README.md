# 天天生鲜购物网站 (Daily Fresh Market)

基于 `Django` 框架开发的完整B2C生鲜电商购物网站。该项目是跟随B站课程《Python实战：Django实现大型购物网站》的实战练习项目，旨在通过构建一个功能完善的在线生鲜商城，深入理解和掌握Django框架在大型项目中的应用，包括用户认证、商品管理、购物车、订单系统等核心电商功能。

## ✨ 主要功能

*   **用户模块**
    *   用户注册/登录/登出
    *   邮箱/手机号激活验证
    *   个人中心信息管理
    *   收货地址管理
*   **商品模块**
    *   商品分类展示（支持多级分类）
    *   商品列表页（支持排序、筛选、分页）
    *   商品详情页
    *   商品搜索功能
*   **购物车模块**
    *   购物车增删改查
    *   合并登录前后购物车
    *   使用`Redis`缓存购物车数据
*   **订单模块**
    *   确认订单页面
    *   生成订单（使用事务保证数据一致性）
    *   订单列表/详情查看
    *   模拟支付流程（集成第三方支付接口示例）
*   **后台管理**
    *   定制化Django Admin
    *   商品、订单、用户等数据管理

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
    现在，在浏览器中访问 `http://127.0.0.1:8000/index` 即可看到网站前台。

## 📁 项目结构

```
tiantian-fresh/
├── apps/                 # 所有Django应用
│   ├── users/            # 用户模块
│   ├── goods/            # 商品模块
│   ├── cart/             # 购物车模块
│   ├── order/            # 订单模块
│   └── ...
├── db/                   # 数据库相关
├── logs/                 # 日志文件
├── media/                # 用户上传文件
├── static/               # 静态文件 (CSS, JS, Images)
├── templates/            # 项目模板文件
├── utils/                # 工具函数/类
├── dailyfresh/           # 项目主配置目录
│   ├── settings.py       # 配置文件
│   ├── urls.py           # 主路由
│   └── wsgi.py
├── .env.example          # 环境变量示例
├── .gitignore
├── manage.py
└── requirements.txt      # 项目依赖
```

