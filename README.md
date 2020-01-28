# xjobs



#### 介绍
一个基于 Python 3 开发的定时任务调度平台。

**开发者：雪山凌狐**

x取雪的第一个字母。

开发的初衷是给自己的云服务器整一个自己写的定时任务调度平台，用来完成一些需要定时调度的任务，比如python，bat，存储过程或者其他等等。同时感谢我的领导对我的指导帮助。

比较适合放到自己的服务器上使用。

因为我是在win平台开发和在win server平台使用的，目前仅保证win平台的正常运转，其他平台请自行尝试。



#### 必要环境安装

1. Python 3已安装到电脑上，我目前开发环境的python示例版本为3.8.1



#### 使用方法

1. 将发行版download到本地并解压到某个单独的文件夹。

2. 安装DB Browser或者SQLite Studio等数据库软件，打开xjobs.db数据库文件进行编辑。（当然，我已配置了一个测试任务，你也可以先跳过这一步，直接到下一步也可以的）

   内含好几张预设表，他们的作用分别如下：

   - **sqlite_sequence：sqlite**表序列存储表，自动生成，自动填写，你无需理会。

   - **xjobs_dictionary：xjobs**数据字典表，对数据库的各个表和字段做了充分详尽的解释，你可以把它看做一个字典，可以不维护，也可以自行按照里面的规范进行维护。

   - **xjobs_task**：我们**最重要**的需要进行配置的表，里面包含许多的字段，某些字段是必填项，你可以根据字典里面的指引或者参考我给你的测试任务的填写范例进行填写。

     其中，**is_pause**字段控制该行的定时任务是否启用，为0则启用，为1则暂停，如果你不需要测试任务了，可以设置为1。

     **update_time**字段为更新时间，我设置了一个触发器，会自动进行时间的更新，你无须自行填写。

     **cron_exp**字段为配置时需要特别关注的点，它为cron定时表达式。它的填写指引如下：

     ```python
     '''
     顺序单位：   秒     分     时     日     月     周      年(年一般省略不写)
     【cron表达式介绍】
     *：触发所有值
     */a：a从最小值开始，触发每个值
     a-b：触发a-b范围内的任何值（必须小于b）
     a-b/c：触发在a-b之间的每个c值
     xth y：第y个工作日中第x天发触发
     last x：在一个月中第x个工作日中的最后一天触发
     last：在月末的最后一天触发
     x,y,z：触发任何匹配的表达式; 可以组合任意数量的任何上述表达式。
     注意：xth y,last x,last这3个是用在day（即日）参数中，其它所有参数都可以使用。
     '''
     ```

    配置好数据库后，保存数据库。

3. 双击“启动xjobs定时调度平台.bat”这个文件启动xjobs调度平台。

4. 启动后会自动先加载一遍数据库中配置好的定时任务，并且每过一段时间也会重新加载一下。你可以根据打开的程序中的提醒，输入对应的命令并回车来执行。

5. 祝您使用愉快！



#### 更新日志
V 1.0 版本 20200128：

1. 完成xjobs定时任务调度框架的绝大部分功能和测试，达到上线水平，即将部署到生产环境。

   欢迎大家尝试使用，如有问题，可以向我反馈或发起Pull Requests。



