from PySide6.QtWidgets import *
from PySide6.QtCore import QTimer, QTime,Qt,QThread,Signal,QTime
from PySide6.QtGui import *
import sys
import ast
# import time
namelist={}
print(namelist)
class timethread(QThread):
        timesignal = Signal(str)
        def run(self):
           while True:
            current_time = QTime.currentTime().toString("hh:mm AP")
            print(current_time)
            self.timesignal.emit(current_time)
            self.msleep(1000)
            # time.sleep(1)
class data(QThread):
    datasignal=Signal(dict)
    mainwindowdata=Signal(dict)
    buyinglist=Signal(dict)
    def run(self):
        with open("gamesdata.txt","r") as file:
            g=file.read()
            self.datasignal.emit(ast.literal_eval(g))
            self.mainwindowdata.emit(ast.literal_eval(g))
            self.buyinglist.emit(namelist)
            # self.msleep(1000)
class timeapp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.toolbar_created = False
        self.setWindowTitle("Timer")
        # self.showFullScreen()
        self.setGeometry(400,100,600,500)
        self.initUI()
        
    def result(self):
        self.datathread=data()
        # self.results()
        self.datathread.start()
        self.datathread.datasignal.connect(self.results)
        # self.datathread.data.connect(self.testing)
        
    def results(self,g):
        widgetresult=QWidget()
        resultlayout=QVBoxLayout(widgetresult)
        l=[]
        for i in g.keys():
            btn=QPushButton()
            btn.setFixedHeight(40)
            if self.text.text().lower()==i.lower():
                btn.setText(self.text.text())
                btn.clicked.connect(lambda checked,name=i,data=g: self.testing(name,data))
                resultlayout.addWidget(btn)
                resultlayout.addStretch()  
        self.stacked.addWidget(widgetresult)
        self.stacked.setCurrentWidget(widgetresult)
    def testing(self,name,data):
        datais=data[name]
        widgetresult=QWidget()
        resultlayout=QVBoxLayout(widgetresult)
        label=QLabel("Name: "+name)
        label.setStyleSheet("font-size:20px;")
        price=QLabel("Price: "+str(datais['price']))
        price.setStyleSheet("font-size:20px;")
        buyingbtn=QPushButton("Buy")
        buyingbtn.clicked.connect(lambda checked,key=name:self.boughtit(key))
        font=QFont()
        font.setPointSize(13)
        description=QTextEdit(str(datais['description']))
        description.setReadOnly(True)
        description.setFont(font)
        resultlayout.addWidget(label)
        resultlayout.addWidget(price)
        resultlayout.addWidget(buyingbtn)
        resultlayout.addWidget(description)
        self.stacked.addWidget(widgetresult)
        self.stacked.setCurrentWidget(widgetresult)
    def testing2(self,i,data):
        widgetresult=QWidget()
        resultlayout=QVBoxLayout(widgetresult)
        label=QLabel("Name: "+str(i))
        label.setStyleSheet("font-size:20px;")
        price=QLabel("Price: "+str(data['price']))
        price.setStyleSheet("font-size:20px;")
        buyingbtn=QPushButton("Buy")
        buyingbtn.clicked.connect(lambda checked,key=str(i),data=data:self.boughtit(key,data))
        buyingbtn.setStyleSheet("font-size:20px; font-style:bold;")
        font=QFont()
        font.setPointSize(13)
        description=QTextEdit(str(data['description']))
        description.setFixedHeight(250)
        description.setReadOnly(True)
        description.setFont(font)
        resultlayout.addWidget(label)
        resultlayout.addWidget(price)
        resultlayout.addWidget(buyingbtn)
        resultlayout.addWidget(description)
        resultlayout.addStretch()
        self.stacked.addWidget(widgetresult)
        self.stacked.setCurrentWidget(widgetresult)
    def exit(self):
        self.close()
    def send_data_to_bought(self):
        self.datathread=data()
        self.datathread.start()
        self.datathread.buyinglist.connect(self.bought)
    def boughtit(self,name,data):
        if name not in namelist.keys():
           namelist[name]=data['price']
           print(namelist)
        self.send_data_to_bought()
    def bought(self,name):
        print(name)
        widget=QWidget()
        layout=QVBoxLayout()
        text=QLabel("buying")
        text.setStyleSheet("font-size:20px")
        hlayout=QHBoxLayout()
        hlayout.addStretch()
        hlayout.addWidget(text)
        hlayout.addStretch()
        layout.addLayout(hlayout)
        font=QFont()
        font.setPointSize(15)
        font.bold()
        for i in name.keys():
          holayout=QHBoxLayout()
          btn=QLabel(i)
          price=QLabel(str(name[i]))
          price.setFont(font)
          btn.setStyleSheet("font-size:30px;height:50px")
          holayout.addWidget(btn)
          holayout.addStretch()
          holayout.addWidget(price)
          layout.addLayout(holayout)
        widget.setLayout(layout)
        layout.addStretch()
        self.stacked.addWidget(widget)
        self.stacked.setCurrentWidget(widget)
    def initUI(self):
        widget=QWidget()
        layout=QVBoxLayout(widget)
        self.stacked=QStackedWidget()
        # toolbar=QToolBar("home",self)
        if not self.toolbar_created:
            font=QFont()
            font.setBold(True)
            toolbar=QToolBar("HOME")
            self.addToolBar(Qt.ToolBarArea.LeftToolBarArea,toolbar)
            toolbar.setStyleSheet("color:red;")
            toolbar.setFont(font)
            homeaction=QAction("Home",self)
            buying=QAction("Buying",self)
            exitaction=QAction("EXIT",self)
            homeaction.setFont(font)
            exitaction.setFont(font)
            buying.setFont(font)
            exitaction.triggered.connect(self.exit)
            buying.triggered.connect(self.send_data_to_bought)
            homeaction.triggered.connect(self.initUI)
            toolbar.addAction(homeaction)
            toolbar.addAction(buying)
            toolbar.addSeparator()
            toolbar.addAction(exitaction)
            self.toolbar_created=True
        # menubar.addMenu(menu)
        layout2=QVBoxLayout()
        hlayout=QHBoxLayout()
        self.mainwindowthread=data()
        self.mainwindowthread.mainwindowdata.connect(self.maindisplay)
        self.mainwindowthread.start()
        self.thread=timethread()
        self.thread.timesignal.connect(self.updatetime)
        self.thread.start()
        self.timelabel=QLabel("")
        self.timelabel.setAlignment(Qt.AlignmentFlag.AlignRight)
        layout2.addWidget(self.timelabel)
        self.text=QLineEdit()
        self.text.setFixedHeight(30)
        btn=QPushButton("search")
        btn.setShortcut("return")
        btn.clicked.connect(self.result)
        layout2.addLayout(hlayout)
        layout.addLayout(layout2)
        hlayout.addWidget(self.text)
        hlayout.addWidget(btn)
        layout.addWidget(self.stacked)
        self.setCentralWidget(widget)
        # self.menu()
    def searchresults(self):
        self.widget2=QWidget()
        layoutresult=QVBoxLayout(self.widget2)
        titleqlabel=QLabel("RESULTS")
        titleqlabel.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        layoutresult.addWidget(titleqlabel)
        self.stacked.addWidget(self.widget2)
        self.stacked.setCurrentWidget(self.widget2)
    def updatetime(self,current_time):
        self.timelabel.setText(current_time)
    def maindisplay(self,g):
        widgetmaindisplay=QWidget()
        maindisplaylayout=QVBoxLayout(widgetmaindisplay)
        scroll=QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setWidget(widgetmaindisplay)
        for i in g.keys():
           namelabel=QPushButton(str(i))
        #    if namelabel.clicked.connect(lambda checked,key=i: self.testing2(i))!=None:
           namelabel.clicked.connect(lambda checked,key=i,data=g[i]: self.testing2(key,data))
           namelabel.setFixedHeight(50)
           maindisplaylayout.addWidget(namelabel)
        self.stacked.addWidget(scroll)
        self.stacked.setCurrentWidget(scroll)

def main():
    app=QApplication()
    win=timeapp()
    win.show()
    sys.exit(app.exec_())
if __name__=="__main__":
    main()
