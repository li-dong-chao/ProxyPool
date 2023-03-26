FROM python:3.11.2-slim-bullseye

LABEL maintainer="LiDongchao <1148238139@qq.com>"

# 工作路径
WORKDIR /ProxyPool

# 环境变量
ENV TZ=Asia/Shanghai HOST=127.0.0.1 PORT=6379 USERNAME="" PASSWORD=""

# 复制requirements到容器内
COPY ./requirements.txt /

# 配置pip源和apt源，并安装python第三方依赖，修改时区
RUN pip install -i https://pypi.tuna.tsinghua.edu.cn/simple pip -U \
&& pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple \
&& pip install --no-cache-dir -r /requirements.txt \
&& sed -i "s@http://security.debian.org@https://repo.huaweicloud.com@g" /etc/apt/sources.list \
&& sed -i 's/deb.debian.org/mirrors.ustc.edu.cn/g' /etc/apt/sources.list \
&& apt-get update \
&& echo "${TZ}" > /etc/timezone \
&& ln -sf /usr/share/zoneinfo/${TZ} /etc/localtime

# 暴露端口
EXPOSE 8000

# 启动命令
CMD ["/bin/sh", "/ProxyPool/app/start.sh"]
