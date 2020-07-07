



## 树莓派4b 违法行人抓拍系统

> 模拟红绿灯路口的违法行人拍照，当交通灯为红灯时，开始工作，检测到人从马路对面闯红灯过来时，会检测人脸拍摄一张照片并且将人脸显示在大屏幕上（暂时为发送邮件替代，网站没时间搭建）



#### 1.用到的硬件

> 树莓派4b
> 人体红外传感器
> 树莓派官方摄像头
> 蜂鸣器
### 2.代码说明
###### 2.1 人体红外传感器
运行 detect_pelple.py 工作原理，注意GPIO口有BCM和BOARD两种模式
![enter description here](./images/20180130214951056.jpg)

###### 2.2 蜂鸣器
查看 initial_buzzer.py 有蜂鸣器的基本使用方法

###### 2.3 主函数
运行 main.py 需要一些环境配置。新装的树莓派需要挺多的操作
推荐先更换国内镜像源后，然后pip install下来，比较靠谱的教程如下：
[树莓派4B换清华源并更换系统源（Raspbian-buster系统）](https://blog.csdn.net/zqxdsy/article/details/102574239?utm_medium=distribute.pc_relevant.none-task-blog-baidujs-1)
**关于pip下载源：**
自己配置时，pip源没有成功更换，除了~/.pip/pip.conf，另外需要到etc下更改pip的配置文件