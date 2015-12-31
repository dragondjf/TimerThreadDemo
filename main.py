#!/usr/bin/python
# -*- coding: utf-8 -*-


from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *


class SignalManager(QObject):

    startTimer1Worker = pyqtSignal()
    startTimer2Worker = pyqtSignal()

    timer1Signal = pyqtSignal()
    timer2Signal = pyqtSignal()


    def __init__(self, parent=None):
        super(SignalManager, self).__init__(parent)


signalManger = SignalManager()


class Timer1Worker(QObject):

    def __init__(self, parent=None):
        super(Timer1Worker, self).__init__(parent)
        self.initWorker()
        self.initConnect()

    def initWorker(self):
        self.timer = QTimer(self)
        self.timer.setInterval(100)
        self.timer.timeout.connect(signalManger.timer1Signal)

    def initConnect(self):
        signalManger.startTimer1Worker.connect(self.timer.start)


class Timer2Worker(QObject):

    def __init__(self, parent=None):
        super(Timer2Worker, self).__init__(parent)
        self.initWorker()
        self.initConnect()

    def initWorker(self):
        self.timer = QTimer(self)
        self.timer.setInterval(200)
        self.timer.timeout.connect(signalManger.timer2Signal)

    def initConnect(self):
        signalManger.startTimer2Worker.connect(self.timer.start)


class TaskController(QObject):
    """docstring for FileController"""
    def __init__(self, parent=None):
        super(TaskController, self).__init__(parent)
        self.initTask1()
        self.initTask2()

    def initTask1(self):
        self.worker1 = Timer1Worker()
        self.thread1 = QThread()
        self.worker1.moveToThread(self.thread1)
        self.thread1.start()

    def initTask2(self):
        self.worker2 = Timer2Worker()
        self.thread2 = QThread()
        self.worker2.moveToThread(self.thread2)
        self.thread2.start()

    def startTask(self):
        signalManger.startTimer1Worker.emit()
        signalManger.startTimer2Worker.emit()


class MainWindow(QFrame):
    """docstring for MainWindow"""
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(None)
        self.parent = parent
        self.initData()
        self.initUI()
        self.initConnect()

    def initData(self):
        self.count1 = 0
        self.count2 = 0

    def initUI(self):
        self.resize(400, 300)
        self.label1 = QLabel("thread1", self)
        self.timerlabel1 = QLabel("0", self)
        self.label2 = QLabel("thread2", self)
        self.timerlabel2 = QLabel("0", self)

        mainLayout = QGridLayout()
        mainLayout.addWidget(self.label1, 0, 0)
        mainLayout.addWidget(self.timerlabel1, 0, 1)
        mainLayout.addWidget(self.label2, 1, 0)
        mainLayout.addWidget(self.timerlabel2, 1 , 1)
        
        self.setLayout(mainLayout)

    def initConnect(self):
        signalManger.timer1Signal.connect(self.updateTimerLabel1)
        signalManger.timer2Signal.connect(self.updateTimerLabel2)

    def updateTimerLabel1(self):
        self.count1 += 1
        self.timerlabel1.setText("%d" % self.count1)

    def updateTimerLabel2(self):
        self.count2 += 1
        self.timerlabel2.setText("%d" % self.count2)


if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    main = MainWindow()
    main.show()
    taskController = TaskController()
    taskController.startTask()
    sys.exit(app.exec_())
