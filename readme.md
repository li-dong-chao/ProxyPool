# ProxyPool

一个简单的代理池项目，主要用于从自动抓取网上的免费代理，对代理质量进行验证，并入库储存。

具体实现的功能点如下：

* 通过`Fetcher`类实现对免费代理网站的爬取，包含一个简单的可插拔设计，方便扩展免费代理网站。
* 通过`Validator`类实现对代理的活性验证。
* 借用`pydantic`模块实现对代理类型的校验。
* 使用`fastapi`进行功能封装，提供API接口方便直接调用。

## 部署方式

* 下载源码到本地

```shell
git clone git@github.com:li-dong-chao/ProxyPool.git
```

* 启动项目
```shell
cd ProxyPool
docker-compose up -d
```

* 检查项目是否正常启动
```shell
docker logs --tail 100 proxypool
```

出现下面的内容，说明服务正常启动了
```text
INFO:     Started server process [12]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
2023-03-27 12:33:32.914 | INFO     | app.fetcher.fetcher:get:27 - 开始抓取代理
2023-03-27 12:33:32.915 | INFO     | app.fetcher.fetcher:get:30 - <class 'app.fetcher.geonode.Geonode'> start
2023-03-27 12:33:38.874 | INFO     | app.fetcher.fetcher:get:30 - <class 'app.fetcher.ip66.IP66'> start
2023-03-27 12:34:26.006 | INFO     | app.fetcher.fetcher:get:30 - <class 'app.fetcher.ip89.IP89'> start
```

## 使用方式

本项目提供了4个API接口，方便在爬虫时直接调用。

* 获取一个代理
  * 地址：http://<ip>:<port>/get
  * 请求方式：get
  * 请求参数示例：
    * 无需参数
  * 返回结果示例：
    * http://127.0.0.1/7777 （有代理则返回该结果）
    * No proxy in pool.  （代理池中无代理，返回该结果）
* 删除一个代理
  * 地址：http://<ip>:<port>/get
  * 请求方式：delete
  * 请求参数示例：
    * http://127.0.0.1/7777 （传get返回的结果即可）
  * 返回结果示例：
    * OK
* 查看所有代理数量
    * 地址：http://<ip>:<port>/quantity/all
    * 请求方式：get
    * 请求参数示例：
        * 无需参数
    * 返回结果示例：
        * 100
* 查看验证通过代理数量
    * 地址：http://<ip>:<port>/quantity/valid
    * 请求方式：get
    * 请求参数示例：
        * 无需参数
    * 返回结果示例：
        * 100

## 扩展免费代理网站

在`app/fetcher`目录下新增脚本 `your_file_name.py`，
该脚本中生成一个类，类目无限制，但是该类需要继承自`app/fetcher/base.py`中的`BaseFetcher`类，
并实现`fetch`方法，`fetch`方法即为爬虫代码，它通过`yield`返回一个代理类型（即`app/schemas/proxy.py`中的`Proxy`）。
脚本完成后，如果需要启动该方法，在`app/fetcher/__init__.py`中引入一下该类即可。


> 该项目是对以下两个开源项目的拙略模仿，仅作自己学习练手，
> 有类似在学习代理池搭建的同学，建议了解下这两个项目：
> 
> * https://github.com/Python3WebSpider/ProxyPool
> * https://github.com/jhao104/proxy_pool