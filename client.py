#!/usr/local/bin/python
# -*- coding: utf-8 -*-

import sip
import audiere
import blender_net
sip.setapi('QString', 2)
sip.setapi('QVariant', 2)

from PyQt4 import QtCore, QtGui

import soundviz


class SelectionRect(QtGui.QGraphicsItem):
            
        def __init__(self, p_x=0, p_y=0, p_width=50, p_height=50, p_num=1):
            super(SelectionRect,self).__init__()
            self.setZValue(10)
            self.x=p_x
            self.y=p_y
            self.height=p_height
            self.width=p_width
            self.num=p_num
                
        def paint(self, painter, option, widget=0):
            pen = QtGui.QPen()
            pen.setColor(QtGui.QColor(QtCore.Qt.green))
            pen.setWidth(3)
            painter.setPen(pen)
            painter.drawRect(self.x, self.y,self.width, self.height)
            pen.setColor(QtGui.QColor(QtCore.Qt.black))
            pen.setWidth(1)
            painter.setPen(pen)
            painter.drawRect(self.x, self.y,abs(self.width), abs(self.height))
            painter.drawText(self.x+2,self.y+10,str(self.num))
            
            painter.fillRect(QtCore.QRectF(self.x-10+self.width,self.y,10,10), QtGui.QBrush(QtCore.Qt.white))
            painter.drawText(self.x-10+self.width,self.y+10,str("X"))
            
        def boundingRect(self):
            return QtCore.QRectF(self.x-1,self.y-1,self.width+1,self.height+1)
        def mousePressEvent(self,  mouseEvent ):
            print("mouse press event" + str(mouseEvent.pos()))
            if QtCore.QRectF(self.x-10+self.width,self.y,10,10).contains(mouseEvent.pos()):
                print("pressed X")
                mouseEvent.accept()
                rect = self.boundingRect()
                scene = self.scene()
                scene.removeItem(self)
                scene.update(rect)
                scene.update()
                
            else:
                mouseEvent.ignore()
            
            

class EqualizerScene(QtGui.QGraphicsScene):
    clicked = 0
    inPoint = QtCore.QPointF()
    outPoint = QtCore.QPointF()
    
    x = 0
    y = 80
    height = 400
    width = 450
    samples = 15
    
    rects = []
    bounds = []
    marked = []
    frame_counter = []
    boxes = []
    
    def __init__(self):
        super(EqualizerScene, self).__init__()

    def mousePressEvent(self,  mouseEvent ):
        super(EqualizerScene,self).mousePressEvent(mouseEvent)
        if not self.clicked and mouseEvent.button() & QtCore.Qt.RightButton > 0:
            self.clicked = 1
            print("clicked at:")
            self.inPoint = mouseEvent.scenePos()
            print(str(mouseEvent.scenePos()))

    def mouseReleaseEvent(self,  mouseEvent ):
        
        if self.clicked :    
            self.clicked = 0
            print("released at:")
            self.outPoint = mouseEvent.scenePos()
            print(str(mouseEvent.scenePos()))
            self.marked.append(self.clipToEq())
            print(str(self.marked[-1]))
            tmp = self.marked[-1]
            wid = self.width / float(self.samples)
            #self.addRect(tmp[0]*wid,self.y + self.height*(1-tmp[1]-tmp[3]),tmp[2]*wid,tmp[3]* self.height)
            b  = SelectionRect(tmp[0]*wid, self.y + self.height*(1-tmp[1]-tmp[3]), tmp[2]*wid, max(tmp[3]*self.height,10) , len(self.marked))
            self.boxes.append(b)
            self.addItem(b)
            self.update(b.boundingRect())
            self.update()


    def clipToEq(self):
        min_x = min(self.inPoint.x(),self.outPoint.x())
        max_x = max(self.inPoint.x(),self.outPoint.x())
        min_y = min(self.inPoint.y(),self.outPoint.y())
        max_y = max(self.inPoint.y(),self.outPoint.y())
        wid = self.width /float(self.samples)
        x = round(min_x/wid)
        w = max(1, round(max_x/wid) - round(min_x/wid))
        y = -(max_y - (self.y + self.height)) / float(self.height)
        h = -(min_y - (self.y + self.height)) / float(self.height) - y

        return (x,y,w,h)
     
    def nextSample(self, row, frame=0):

        #row = self.song.getFrame(self.frame % self.song.size()[0])
        #self.scene.clear()
        #self.scene.setForegroundBrush(QtGui.QBrush(QtCore.Qt.lightGray, QtCore.Qt.CrossPattern));
        #self.scene.addRect(-10,-10,20,20, QtGui.QPen(QtGui.QColor(QtCore.Qt.red)), QtGui.QBrush(QtCore.Qt.lightGray, QtCore.Qt.CrossPattern))
        #self.scene.addRect(0,0,10,10, QtGui.QPen(QtGui.QColor(QtCore.Qt.red)), QtGui.QBrush(QtCore.Qt.lightGray, QtCore.Qt.SolidPattern))
        counter = 0
        self.samples = len(row)
        width = float(self.width)/float(self.samples)
        
        if not self.frame_counter:
            self.frame_counter = QtGui.QGraphicsTextItem("frame: 0")
            self.frame_counter.setZValue(2.0)
            self.addItem(self.frame_counter)
            self.frame_counter.setPos(10.0,100.0)
        self.frame_counter.setPlainText("frame: " + str(frame))
        
        for sample in row:
            while len(self.rects) <=counter:
                self.rects.append(self.addRect(counter*width,160,width,-1.0*(80.0), 
                    QtGui.QPen(QtGui.QColor(QtCore.Qt.black)),
                    QtGui.QBrush(QtCore.Qt.lightGray, QtCore.Qt.SolidPattern)))
            self.rects[counter].setRect(counter*width,self.y+self.height,width,self.height/-80.0*(80+float(sample))) 
            counter +=1
        if type(self.bounds) == type([]):
            self.bounds= self.addRect(counter*width,160,width,-1.0*(80.0), 
                QtGui.QPen(QtGui.QColor(QtCore.Qt.black)),
                QtGui.QBrush(QtCore.Qt.white, QtCore.Qt.SolidPattern))
            self.bounds.setZValue(-1)
        
        self.bounds.setRect(QtCore.QRectF(self.x,self.y,self.width,self.height))
        self.update(QtCore.QRectF(-1,-1,counter*width+83,160))
        
        #self.view.invalidateScene()
        #self.view.update()
        self.update()
        #self.main.update()
    
    def removeItem(self, item):
        super(EqualizerScene,self).removeItem(item)
        ind = self.boxes.index(item)
        print("index: INDD" + str(ind))
        if ind >= 0:
            del self.marked[ind]
            del self.boxes[ind]
        
class MainWindow(QtGui.QMainWindow):
    _addtime = 0

    def __init__(self):
        super(MainWindow, self).__init__()
        
        #initialize Window
        self.setWindowTitle("Frequency Key Generator")
        self.resize(500, 500)
        
        #create Objects
        self.song = soundviz.Song("left_new3.dat",45)
        size = self.song.size()
        print("size is " + str(size))
        self.frames=size[0]
        self.samples=size[1]
        
        self.main = QtGui.QWidget()
        self.main_layout = QtGui.QVBoxLayout()
        self.controls_layout = QtGui.QHBoxLayout()

        self.scene = EqualizerScene()
        self.view = QtGui.QGraphicsView(self.scene)
        
        self.fps = QtGui.QSpinBox()
        self.frame_slider = FrameSlider(self)
        self.frame_slider.setMinimum(0)
        self.frame_slider.setMaximum(self.frames)
        self.frame_slider.setTickInterval(self.frames/10)
        self.slider_moving=False

        self.start_button = QtGui.QPushButton("Start")
        self.stop_button = QtGui.QPushButton("Stop")
        
        #setLayout
        self.main.setLayout(self.main_layout)
        self.setCentralWidget(self.main)
        self.main_layout.addWidget(self.view)
        self.main_layout.addWidget(self.frame_slider)
        self.main_layout.addLayout(self.controls_layout)
        
        self.controls_layout.addWidget(self.start_button)
        self.controls_layout.addWidget(self.stop_button)
        self.controls_layout.addStretch()
        self.controls_layout.addWidget(QtGui.QLabel("FPS:"))
        self.controls_layout.addWidget(self.fps)
        
        self.test_layout = QtGui.QHBoxLayout()
        self.test_box_text = QtGui.QLabel("box:")
        self.test_box_input = QtGui.QSpinBox()
        self.test_frame_text = QtGui.QLabel("frame:")
        self.test_frame_input = QtGui.QSpinBox()
        self.test_calculate = QtGui.QPushButton("calc")
        self.test_val_text = QtGui.QLabel("result:")
        self.test_val_disp = QtGui.QLabel("0.0")
        
        self.main_layout.addLayout(self.test_layout)
        self.test_layout.addWidget(self.test_box_text)
        self.test_layout.addWidget(self.test_box_input)
        self.test_layout.addWidget(self.test_frame_text)
        self.test_layout.addWidget(self.test_frame_input)
        self.test_layout.addWidget(self.test_calculate)
        self.test_layout.addWidget(self.test_val_text)
        self.test_layout.addWidget(self.test_val_disp)
        QtCore.QObject.connect(self.test_calculate, QtCore.SIGNAL("clicked()"),self.showBoxVal)
        
        #Signal Slot connections
        QtCore.QObject.connect(self.start_button, QtCore.SIGNAL("clicked()"),self.startPlayback)
        QtCore.QObject.connect(self.stop_button, QtCore.SIGNAL("clicked()"),self.stopPlayback)
        
        #fill Data
        self.fps.setValue(24)
        self.fps.setRange(1,500)

        self.server = blender_net.TCPEq.startServing(blender_net.HOST,blender_net.PORT)
        blender_net.TCPEq.setFrameMethod(self.getFrameCount)
        blender_net.TCPEq.setSelectedMethod(self.getSelectionCount)
        blender_net.TCPEq.setRetrieveMethod(self.getSample)
        self.audio=audiere.open_device()
        self.song_wav = self.audio.open_file("song.ogg")

    def getFrameCount(self):
        return self.frames
    def getSampleCount(self):
        return self.samples
    def getSelectionCount(self):
        return len(self.scene.marked)
        
    def showBoxVal(self):
        box = self.test_box_input.value()
        frame = self.test_frame_input.value()
        self.test_val_disp.setText(str(self.getSample(box,frame)))
        
        
    def skipToFrame(self, frame):
        self.frame = frame
        if self.slider_moving:
            pass
        else:
            self.slider_moving = True
            self.timer = QtCore.QTimer()
            self.timer.setSingleShot(True)
            QtCore.QObject.connect(self.timer, QtCore.SIGNAL("timeout()"),self.commitFrameChange)
            self.timer.start(250)
        #self.nextSample()
        
    def commitFrameChange(self):
        self._addtime = 1000.0 * self.frame/self.fps.value()
        self.nextSample()
        self.slider_moving=False
        del(self.timer)
        
    def nextSample(self):
        try:
            #print("frame:"+ str(self.frame))
            if self.frame*(1000.0/self.fps.value()) < self.elapsed():
                self.frame +=1
            else:
                return
        except AttributeError:
            self.frame=0
            return
        
        
        row = self.song.getFrame(self.frame % self.song.size()[0])
        self.scene.nextSample(row, self.frame)
        self.frame_slider.setValue(self.frame)
        '''
        self.scene.clear()
        #self.scene.setForegroundBrush(QtGui.QBrush(QtCore.Qt.lightGray, QtCore.Qt.CrossPattern));
        self.scene.addRect(-10,-10,20,20, QtGui.QPen(QtGui.QColor(QtCore.Qt.red)), QtGui.QBrush(QtCore.Qt.lightGray, QtCore.Qt.CrossPattern))
        self.scene.addRect(0,0,10,10, QtGui.QPen(QtGui.QColor(QtCore.Qt.red)), QtGui.QBrush(QtCore.Qt.lightGray, QtCore.Qt.SolidPattern))
        counter = 0
        width = 10
        for sample in row:
            self.scene.addRect(counter*width,160,width,-1.0*(80.0+float(sample)), 
                QtGui.QPen(QtGui.QColor(QtCore.Qt.black)),
                QtGui.QBrush(QtCore.Qt.lightGray, QtCore.Qt.SolidPattern))
            counter +=1
        self.scene.addRect(QtCore.QRectF(-1,160,counter*width+83,-160))
        
        self.scene.update(QtCore.QRectF(-1,-1,counter*width+83,160))
        
        self.view.invalidateScene()
        self.view.update()
        self.update()
        self.main.update()
        '''

    def startPlayback(self):
        try:
            if not  self.timer.isActive():
                self.timer.start(1000.0/(2*self.fps.getValue()))
            if(self.time_stopped):
                self.time.restart()
                self.time_stopped = 0
                self.song_wav.position=self.elapsed()*44.1
                self.song_wav.play()
        except (NameError, AttributeError):
            self.time_stopped = 0
            self.timer = QtCore.QTimer(self)
            self.time = QtCore.QTime(1,1)
            self.timer.setSingleShot(0)
            QtCore.QObject.connect(self.timer,QtCore.SIGNAL("timeout()"), self.nextSample)
            self.time.start()
            self.timer.start(1000.0/(2*self.fps.value()))
            self.song_wav.position=self.elapsed()*44.1
            self.song_wav.play()
    
    def stopPlayback(self):
        try:
            self.timer.stop()
            self.time_stopped = self.time.elapsed()
            self._addtime += self.time_stopped
            self.song_wav.pause()
        except (NameError, AttributeError):
            print("nothing to stop there yet")

    def elapsed(self):
        return self.time.elapsed()+self._addtime

        
    def getSample(self,box,frame):
        row = self.song.getFrame(frame)
        if len(self.scene.marked)<=box:
            return -1.0
        bx = self.scene.marked[box]
        samples = row[int(bx[0]):int(bx[0]+bx[2])]
        result = 0
        for sample in samples:
            print("processing:" + str(sample))
            sample = abs(80+sample)/80.0
            sample = sample - bx[1]
            print("after sub:" + str(sample))
            sample = min(max(0,sample / bx[3]), 1.0)
            print("it's:" + str(sample))

            result = result + (sample /len(samples))
        print("sum:" + str(result))

        return result

        
class FrameSlider(QtGui.QSlider):
    def __init__(self, parent):
        super(FrameSlider,self).__init__()
        self.setOrientation(QtCore.Qt.Horizontal)
        self.setTickPosition(self.TicksBothSides)
        print("connecting slots")
        #QtCore.QObject.connect(self,QtCore.SIGNAL("valueChanged( int )"),parent.skipToFrame)
        QtCore.QObject.connect(self,QtCore.SIGNAL("sliderMoved( int )"),parent.skipToFrame)
        print("connectedslots")

    def slider_moved(self, new_position):
        print("(moved)new value is:" + str(new_position))
    def slider_value(self, new_position):
        print("(value)new value is:" + str(new_position))

if __name__ == '__main__':

    import sys

    app = QtGui.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())