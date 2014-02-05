miko
=========
A static blog written by python . 

个人用的静态博客生成器，前身是ShoujoA
实际运行效果请见:http://blog.kochiya.me/

##命令
-------------

初始化
`shoujo.py --init`

提交一篇博文
`shoujo.py --post filename`

提交一个文件夹
`shoujo.py --postDir dirname`

查看已提交的文章
`shoujo.py --show`

删除一篇文章
`shoujo.py --remove index`

本地启动一个测试服务器预览
`shoujo.py --preview`

##书写格式
-----------

```
# Hello world
- archive:documentation
- tags:python,doc

 some texts as abstract.

 content.
 ```python
def hello(name="World"):
    print "Hello %s" % name
 ```
```
  摘要和内容都直接支持markdown格式

##文档
-----------
这是几篇文档。
http://blog.kochiya.me/www/posts/%E5%B7%AB%E5%A5%B3%E7%9A%84%E6%96%B0%E5%B9%B4.html
http://blog.kochiya.me/www/posts/ShoujoA%E7%9A%84%E9%83%A8%E7%BD%B2%E3%80%81%E8%AF%84%E8%AE%BA%E4%BB%A5%E5%8F%8A%E5%85%B6%E5%AE%83.html
http://blog.kochiya.me/www/posts/ShoujoA%E7%9A%84%E4%BD%BF%E7%94%A8%E8%AF%B4%E6%98%8E.html
