# DesktopPet

## 1. Problem Statement

想做一个桌宠，成功实现的模块主要以学习其他人的作品为主。自己添加的模块有点失败(x

### Goals

- [x]  显现在桌面上，鼠标点击时绑定能随鼠标移动位置
- [x]  定时随机切换素材库里的gif来切换动作，以及切换相应的对话
- [x]  计时来提醒休息时间
- [x]  可以隐藏到状态栏，有显示、退出等功能。其他的功能模块也可以通过右键添加实现
- [x]  可以打包成exe，得以运行在别人的电脑上

### Non-goals

- [ ]  通过计时来提醒吃饭、睡觉等
- [ ]  接入AI的api来实现聊天交互

## 2. Implementation

### 2.1 Success implementation

1. 主流有使用gif和使用图片两种方法，参考了gif的方法：

[delta1037/DesktopPet: 桌面宠物](https://github.com/delta1037/DesktopPet)

[桌面宠物 ① 通过python制作属于自己的桌面宠物_gif制作桌宠-CSDN博客](https://blog.csdn.net/zujiasheng/article/details/124670676)

用图片的：

[写个桌面挂件 | 手把手带大家做只桌面宠物呗 - 知乎](https://zhuanlan.zhihu.com/p/125693970)

可以切换宠物的：

[DesktopPet/README.md at main · WolfChen1996/DesktopPet](https://github.com/WolfChen1996/DesktopPet/blob/main/README.md)

2. 对于素材的制作

使用的是网络可达鸭素材

对于网络gif素材转化为透明背景的制作，使用了在线ps工具[【在线PS】PS软件网页版，ps在线图片处理工具photopea-稿定设计PS](https://ps.gaoding.com/#/)

3. 各个模块
- 对于主要功能，利用PyQt5实现。
- 对于休息提醒模块，此处参考的是：[llq20133100095/DeskTopPet: 桌面宠物](https://github.com/llq20133100095/DeskTopPet/tree/main)
    
    由于计时用的QTimer()，在提醒休息的时候不影响正常桌宠语料的更换，利用了setText("")来定时清空休息提醒（设的3秒）
    
4. 打包操作

考虑到对Python库的依赖性，使用的是PyInstaller库

- 首先在anaconda prompt中创建虚拟环境
- 在环境中安装需要的库，我这里主要是pyqt5和pyinstaller。（我的电脑会有pathlib的预警，但是忽略了似乎没有影响）
- 利用如下指令把所有的文件打包（这里包括我的素材文件、主要代码文件以及图标文件，bitbug_favicon.ico 就是桌面图标文件，随便利用了在线生成工具把jpg转化了ico格式）
    
    ```bash
    pyinstaller -F -w -i bitbug_favicon.ico [main.py](http://main.py/)
    ```
    
- 打包后会有dist文件夹，需要的exe文件就在里面，由于我设定的是相对路径，因此我需要把exe文件放在才能正常运行，不然会显示找不到路径。我的路径如下
   ``` 
    …\DesktopPet\
    ├── [main.py]
    ├── bitbug_favicon.ico
    ├── resources\
    │   ├── normal\
    │   ├── click\
    │   ├── tigerIcon.jpg
    │   └── dialog.txt
   ``` 
- 但是会发现在把压缩包发给别人的时候出现找不到resources路径的问题，遂修改在打包时生成的spec文件，将datas=[]改为：
    
    ```python
    datas=[('resources', 'resources')]
    ```
    
    接着打包spec文件，即：
    
    ```bash
    pyinstaller main.spec
    ```
    
    新生成的exe文件放到大目录下，再把压缩包发给别人，可以在没有安装python的电脑上运行桌宠。
    

### 2.2 Pending module

1. 想实现吃饭、睡觉的提醒功能，仿照休息提醒利用QTime.currentTime()提取当前时间，利用if、elif语句实现在某个时间段提醒，并设置trigger确保提醒只在指定时间段内触发一次。但程序很快崩溃，只提醒一次就触发“exited with code=3221226505”。推测是与QTimer定时的多线程管理问题，与休息提醒是不同的计时器，但可能存在多线程冲突。
2. 想实现连ai的聊天交互功能。但如果用本地的模型需要在他人电脑上也进行下载，内存占用大过成繁琐。如果使用ai的api，国产的模型使用了豆包，但也需要事先安装sdk，遂搁置此功能。
