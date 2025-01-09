import os
import sys
import random
import time
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
#from talk_show import Client
#from transformers.dependency_versions_check import pkgs_to_check_at_runtime

def resource_path(relative_path):
    """
    获取资源文件的路径，处理打包后的路径和开发模式下的路径差异
    """
    if getattr(sys, "frozen", False):
        # 处理 PyInstaller 打包后的路径
        base_path = sys._MEIPASS
    else:
        # 使用当前目录作为基准路径
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

class DesktopPet(QWidget):
    def __init__(self, parent=None, **kwargs):
        super(DesktopPet, self).__init__(parent)
        # 窗体初始化
        self.init()
        # 托盘化初始
        self.initPall()
        # 宠物静态gif图加载
        self.initPetImage()
        # 宠物正常待机，实现随机切换动作
        self.petNormalAction()

    def init(self):
        """
        初始化窗口属性，设置为无标题栏并固定在最前面
        """
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.SubWindow)
        self.setAutoFillBackground(False)
        self.setAttribute(Qt.WA_TranslucentBackground, True)
        self.repaint()
        '''
        # 启动定时器检查时间
        self.checkTimeTimer = QTimer(self)  # 创建定时器
        self.checkTimeTimer.timeout.connect(self.checkTime)  # 连接到checkTime方法
        self.checkTimeTimer.start(5000) 
        '''

    def initPall(self):
        """
        初始化托盘图标并设置托盘右键菜单
        """
        icons = resource_path('resources/tigerIcon.jpg')  # 使用 resource_path 获取资源路径
        quit_action = QAction('退出', self, triggered=self.quit)
        quit_action.setIcon(QIcon(icons))
        showing = QAction(u'显示', self, triggered=self.showwin)
        self.tray_icon_menu = QMenu(self)
        self.tray_icon_menu.addAction(quit_action)
        self.tray_icon_menu.addAction(showing)
        self.tray_icon = QSystemTrayIcon(self)
        self.tray_icon.setIcon(QIcon(icons))
        self.tray_icon.setContextMenu(self.tray_icon_menu)
        self.tray_icon.show()

    def initPetImage(self):
        """
        加载宠物静态gif图像，并初始化宠物的状态
        """
        self.talkLabel = QLabel(self)
        self.talkLabel.setStyleSheet("font:15pt '楷体';border-width: 1px;color:blue;")
        self.image = QLabel(self)
        self.movie = QMovie(resource_path("resources/psyduck/psyduck1.gif"))  # 使用 resource_path 获取资源路径
        self.movie.setScaledSize(QSize(200, 200))
        self.image.setMovie(self.movie)
        self.movie.start()
        self.resize(300, 300)
        #self.randomPosition()
        #self.show()
        
        # "休息一下"时间显示
        self.show_time_rest = QLabel(self)
        # 对话框样式设计
        self.show_time_rest.setStyleSheet("font:15pt '楷体';border-width: 1px;color:blue;")

        # 调用自定义的randomPosition，会使得宠物出现位置随机
        self.randomPosition()

        # 布局设置
        vbox = QVBoxLayout()
        vbox.addWidget(self.talkLabel)
        vbox.addWidget(self.image)
        vbox.addWidget(self.show_time_rest)

        #加载布局：前面设置好的垂直布局
        self.setLayout(vbox)

        # 展示
        self.show()
        
        # 将宠物正常待机状态的动图放入pet1中        
        self.pet1 = []
        for i in os.listdir("resources/psyduck"):
            self.pet1.append(resource_path("resources/psyduck/" + i))  # 使用 resource_path 获取资源路径
        
        self.dialog = []
        # 使用 utf-8 编码读取 dialog.txt 文件
        with open(resource_path("resources/dialog.txt"), "r", encoding="utf-8") as f:  # 使用 resource_path 获取资源路径
            text = f.read()
            self.dialog = text.split("\n")

    def petNormalAction(self):
        """
        宠物正常待机动作
        设置宠物的定时随机动作和对话显示
        """
        self.timer = QTimer()
        self.timer.timeout.connect(self.randomAct)
        self.timer.start(4000)  # 动作时间切换设置
        # 宠物状态设置为正常
        self.condition = 0
        # 每隔一段时间切换对话
        self.talkTimer = QTimer()
        self.talkTimer.timeout.connect(self.talk)
        self.talkTimer.start(4000)
        # 对话状态设置为常态
        self.talk_condition = 0
        self.talk()

        # 休息一下
        self.timer_rest = QTimer()
        self.timer_rest.timeout.connect(self.haveRest)
        #self.timer_rest.start(3600000) 
        #self.timer_rest.start(10000)
        # self.timer_rest_movie = QTimer()
        # self.timer_rest_movie.timeout.connect(self.haveRestMovie)
        # self.timer_rest_movie.start(10000)     
        # 
        self.rest_open = 1   # 休息状态开关

    def randomAct(self):
        """
        随机选择宠物的动作并显示
        """
        if not self.condition:
            self.movie = QMovie(random.choice(self.pet1))
            self.movie.setScaledSize(QSize(200, 200)) # 宠物大小
            self.image.setMovie(self.movie)
            self.movie.start()
        # condition不为0，转为切换特有的动作，实现宠物的点击反馈
        # 这里可以通过else-if语句往下拓展做更多的交互功能
        elif self.condition == 1:
            self.movie = QMovie(resource_path("resources/click/click.gif"))  # 使用 resource_path 获取资源路径
            self.movie.setScaledSize(QSize(200, 200))
            self.image.setMovie(self.movie)
            self.movie.start()
            # 宠物状态设置为正常待机
            self.condition = 0
            self.talk_condition = 0
        elif self.condition == 2:
            # 把表情设定为固定的动作
            self.movie = QMovie(resource_path("resources/click/rest.gif"))
            self.movie.setScaledSize(QSize(200, 200))
            self.image.setMovie(self.movie)
            self.movie.start()
            # 宠物状态设置为正常待机
            self.condition = 0
            self.talk_condition = 0

    def talk(self):
        """
        随机选择宠物的对话内容进行显示
        """
        if not self.talk_condition:
            # talk_condition为0则选取加载在dialog中的语句
            self.talkLabel.setText(random.choice(self.dialog))
            self.talkLabel.setStyleSheet(
                "font: bold 15pt 'Pacifico';"
                "color:white;"
                "background-color: transparent"
            )
            self.talkLabel.adjustSize()
        elif self.talk_condition == 1:
            self.talkLabel.setText("别点我!")
            self.talkLabel.setStyleSheet(
                "font: bold 15pt 'Pacifico';"
                "color:white;"
                "background-color: transparent"
            )
            self.talkLabel.adjustSize()
            self.talk_condition = 0

    def quit(self):
        """
        退出程序
        """
        self.close()
        sys.exit()

    def showwin(self):
        """
        显示宠物窗口
        """
        self.setWindowOpacity(1)

    def randomPosition(self):
        """
        随机位置显示宠物
        """
        # screenGeometry（）函数提供有关可用屏幕几何的信息
        screen_geo = QDesktopWidget().screenGeometry()
        # 获取窗口坐标系
        pet_geo = self.geometry()
        width = int((screen_geo.width() - pet_geo.width()) * random.random())
        height = int((screen_geo.height() - pet_geo.height()) * random.random())
        self.move(width, height)
    
    def mousePressEvent(self, event):
        """
        鼠标点击事件处理
        鼠标左键按下时, 宠物将和鼠标位置绑定
        """
        # 宠物状态设置为点击
        self.condition = 1
        self.talk_condition = 1
        self.talk()
        self.randomAct()
        if event.button() == Qt.LeftButton:
            self.is_follow_mouse = True
        # globalPos() 事件触发点相对于桌面的位置
        # pos() 程序相对于桌面左上角的位置，实际是窗口的左上角坐标
        self.mouse_drag_pos = event.globalPos() - self.pos()
        event.accept()
        # 拖动时鼠标图形的设置
        self.setCursor(QCursor(Qt.OpenHandCursor))

    def mouseMoveEvent(self, event):
        """
        鼠标移动事件处理
        鼠标移动时调用，实现宠物随鼠标移动
        """
        if Qt.LeftButton and self.is_follow_mouse:
            self.move(event.globalPos() - self.mouse_drag_pos)
        event.accept()

    def mouseReleaseEvent(self, event):
        """
        鼠标释放事件处理
        鼠标释放调用，取消绑定
        """
        self.is_follow_mouse = False
        # 鼠标图形设置为箭头
        self.setCursor(QCursor(Qt.ArrowCursor))

    def enterEvent(self, event):
        """
        鼠标进入事件处理
        鼠标移进时调用
        """
        # 设置鼠标形状 Qt.ClosedHandCursor   非指向手
        self.setCursor(Qt.ClosedHandCursor)

    def contextMenuEvent(self, event):
        """
        右键菜单事件处理
        """
        # 定义菜单
        menu = QMenu(self)
        # 定义菜单项
        quitAction = menu.addAction("退出")
        hide = menu.addAction("隐藏")
        #question_answer = menu.addAction("聊天")
        if self.rest_open == 1:
            rest_anhour = menu.addAction("打开休息提醒")
        elif self.rest_open == 2:
            rest_anhour = menu.addAction("关闭休息提醒")
        menu.addSeparator()

        # 使用exec_()方法显示菜单。从鼠标右键事件对象中获得当前坐标
        action = menu.exec_(self.mapToGlobal(event.pos()))
        if action == quitAction:
            qApp.quit()
        if action == hide:
            self.setWindowOpacity(0)
        '''
        if action == question_answer:
            self.client = Client()
            self.client.show()
        '''
        if action == rest_anhour:
            if self.rest_open == 1:            
                if not self.timer_rest.isActive():  # 如果定时器没有启动
                    #self.timer_rest.start(10000)
                    self.timer_rest.start(3600000)
                #self.timer_rest.stop()
                self.rest_open = 2
            elif self.rest_open == 2:
                self.timer_rest.stop()
                self.rest_open = 1

    def haveRest(self):
        """
        休息时间
        """
        self.show_time_rest.setText("休息一下!")
        self.show_time_rest.setStyleSheet(
                "font: bold 15pt 'Pacifico';"
                "color:white;"
                "background-color: transparent"
            )
        self.condition = 2
        self.randomAct()
        # 设置一个定时器，休息 3 秒后清空文字
        self.rest_clear_timer = QTimer()
        self.rest_clear_timer.timeout.connect(self.clearRestMessage)
        self.rest_clear_timer.start(3000)  # 3秒后清除“休息一下!”文字

    def clearRestMessage(self):
        """
        清除休息时间的文字
        """
        self.show_time_rest.setText("")  # 清空文字
        self.rest_clear_timer.stop()  # 停止定时器
    
    '''
    def checkTime(self):
        """
        检查当前时间并显示对应的消息
        """
        current_time = QTime.currentTime()
        hour = current_time.hour()
        minute = current_time.minute()

        # 午餐时间段：12:00 到 12:10
        if hour == 12 and 0 <= minute <= 10:
            if not hasattr(self, 'lunch_triggered_today') or not self.lunch_triggered_today:
                self.show_message("吃午饭了！")
                self.lunch_triggered_today = True  # 设置午餐已触发标志

        # 晚餐时间段：18:00 到 18:10
        elif hour == 18 and 0 <= minute <= 10:
            if not hasattr(self, 'dinner_triggered_today') or not self.dinner_triggered_today:
                self.show_message("晚餐时间到了！")
                self.dinner_triggered_today = True  # 设置晚餐已触发标志

        # 休息时间段：23:30 到 23:40
        elif hour == 22 and 51 <= minute <= 53:
            if not hasattr(self, 'rest_triggered_today') or not self.rest_triggered_today:
                self.show_message("记得早点休息！")
                self.rest_triggered_today = True  # 设置休息已触发标志

        else:
            # 清除所有的标志，允许下次触发
            if hasattr(self, 'lunch_triggered_today'):
                del self.lunch_triggered_today
            if hasattr(self, 'dinner_triggered_today'):
                del self.dinner_triggered_today
            if hasattr(self, 'rest_triggered_today'):
                del self.rest_triggered_today

    def show_message(self, message):
        """
        显示消息并设置定时器在3秒后清除
        """
        self.show_time_rest.setText(message)
        self.show_time_rest.setStyleSheet(
            "font: bold 15pt 'Pacifico';"
            "color:white;"
            "background-color: transparent"
        )
        self.condition = 0
        self.randomAct()

        # 设置定时器，3秒后清除消息
        self.clear_message_timer = QTimer(self)
        self.clear_message_timer.timeout.connect(self.clearRestMessage)
        self.clear_message_timer.start(3000)  # 3秒后清除文字
    '''

if __name__ == '__main__':
    """
    主程序入口，启动应用并显示宠物窗口
    """
    app = QApplication(sys.argv)
    pet = DesktopPet()
    sys.exit(app.exec_())
