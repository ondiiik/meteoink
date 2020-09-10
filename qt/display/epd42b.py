import sys
import framebuf
from PyQt5 import QtCore, QtGui, QtWidgets, uic
from PyQt5.QtCore import Qt


EPD_WIDTH  = 400
EPD_HEIGHT = 300

class EPD(QtWidgets.QMainWindow):
    def __init__(self, spi, cs, dc, rst, busy):
        self.width  = EPD_WIDTH
        self.height = EPD_HEIGHT

    def init(self):
        pass


    def display_frame(self, fb_black, fb_yellow):
        self.display_window(fb_black, fb_yellow, 0, 0, EPD_WIDTH, EPD_HEIGHT)


    def display_window(self, fb_black, fb_yellow, x, y, w, h):
        class MainWindow(QtWidgets.QMainWindow):
            def __init__(self):
                super().__init__()
                
                self.label = QtWidgets.QLabel()
                canvas = QtGui.QPixmap(EPD_WIDTH, EPD_HEIGHT)
                self.label.setPixmap(canvas)
                self.setCentralWidget(self.label)
                self.draw_something()
            
            def draw_something(self):
                # Create painter
                painter = QtGui.QPainter(self.label.pixmap())
                pen     = QtGui.QPen()
                pen.setWidth(1)
                painter.setPen(pen)
                
                
                # Draw black frame buffer part
                fb = framebuf.FrameBuffer(fb_black, EPD_WIDTH, EPD_HEIGHT, framebuf.MONO_HLSB)
                
                for yy in range(EPD_HEIGHT):
                    for xx in range(EPD_WIDTH):
                        c = fb.pixel(xx, yy)
                        
                        if (xx >= x) and (yy >= y) and (xx < x + w) and (yy < y + h):
                            if c == 0:
                                pen.setColor(QtGui.QColor('white'))
                            else:
                                pen.setColor(QtGui.QColor('black'))
                        else:
                            if c == 0:
                                pen.setColor(QtGui.QColor('blue'))
                            else:
                                pen.setColor(QtGui.QColor('red'))
                            
                        painter.setPen(pen)
                        painter.drawPoint(xx, yy)
                
                
                # Draw yellow frame buffer part
                fb = framebuf.FrameBuffer(fb_yellow, EPD_WIDTH, EPD_HEIGHT, framebuf.MONO_HLSB)
                 
                for yy in range(EPD_HEIGHT):
                    for xx in range(EPD_WIDTH):
                        c = fb.pixel(xx, yy)
                        if c == 1:
                            pen.setColor(QtGui.QColor('yellow'))
                            painter.setPen(pen)
                            painter.drawPoint(xx, yy)
                
                painter.end()
        
        app    = QtWidgets.QApplication(sys.argv)
        window = MainWindow()
        window.show()
        app.exec_()
