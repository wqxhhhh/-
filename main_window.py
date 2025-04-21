from PyQt5.QtWidgets import (QMainWindow, QToolBar, QAction, QColorDialog, 
                           QSlider, QLabel, QStatusBar, QFileDialog, QWidget,
                           QHBoxLayout)
from PyQt5.QtCore import Qt, QSize
import json

from canvas import Canvas

class MainWindow(QMainWindow):
    #主窗口的初始化
    def __init__(self):
        super().__init__()
        self.setWindowTitle("光滑曲线绘制工具")
        self.setGeometry(100, 100, 800, 600)
        
        # 创建画布
        self.canvas = Canvas()
        self.setCentralWidget(self.canvas)
        
        # 创建工具栏
        self.create_toolbar()
        
        # 创建状态栏
        self.statusBar = QStatusBar()
        self.setStatusBar(self.statusBar)
        self.statusBar.showMessage("就绪")
        
        # 创建控制面板
        self.create_control_panel()
        
    def create_toolbar(self):
        toolbar = QToolBar("主工具栏")
        toolbar.setIconSize(QSize(16, 16))
        self.addToolBar(toolbar)
        
        # 保存按钮
        save_action = QAction("保存", self)
        save_action.triggered.connect(self.save_curve)
        toolbar.addAction(save_action)
        
        # 加载按钮
        load_action = QAction("加载", self)
        load_action.triggered.connect(self.load_curve)
        toolbar.addAction(load_action)
        
        toolbar.addSeparator()
        
        # 清除按钮
        clear_action = QAction("清除", self)
        clear_action.triggered.connect(self.clear_canvas)
        toolbar.addAction(clear_action)
        
        # 显示/隐藏控制点按钮
        toggle_points_action = QAction("显示/隐藏控制点", self)
        toggle_points_action.triggered.connect(self.toggle_points)
        toolbar.addAction(toggle_points_action)
        
        # 颜色选择按钮
        color_action = QAction("选择颜色", self)
        color_action.triggered.connect(self.choose_color)
        toolbar.addAction(color_action)
        
        toolbar.addSeparator()
        
    def create_control_panel(self):
        # 创建控制面板
        control_panel = QWidget()
        control_layout = QHBoxLayout()
        
        # 线宽滑块
        width_label = QLabel("线宽:")
        control_layout.addWidget(width_label)
        
        width_slider = QSlider(Qt.Horizontal)
        width_slider.setMinimum(1)
        width_slider.setMaximum(10)
        width_slider.setValue(self.canvas.curve_width)
        width_slider.valueChanged.connect(self.change_width)
        control_layout.addWidget(width_slider)
        
        control_panel.setLayout(control_layout)
        
        # 创建底部工具栏
        bottom_toolbar = QToolBar("控制面板")
        bottom_toolbar.addWidget(control_panel)
        self.addToolBar(Qt.BottomToolBarArea, bottom_toolbar)
        
    def clear_canvas(self):
        self.canvas.points = []
        self.canvas.update()
        self.statusBar.showMessage("画布已清除")
        
    def toggle_points(self):
        self.canvas.show_points = not self.canvas.show_points
        self.canvas.update()
        self.statusBar.showMessage("控制点已" + ("显示" if self.canvas.show_points else "隐藏"))
        
    def choose_color(self):
        color = QColorDialog.getColor(self.canvas.curve_color, self)
        if color.isValid():
            self.canvas.curve_color = color
            self.canvas.update()
            self.statusBar.showMessage("颜色已更改")
            
    def change_width(self, value):
        self.canvas.curve_width = value
        self.canvas.update()
        self.statusBar.showMessage(f"线宽已更改为 {value}")
    
    #保存曲线到文件
    def save_curve(self):
        file_name, _ = QFileDialog.getSaveFileName(
            self,
            "保存曲线",
            "",
            "JSON Files (*.json);;All Files (*)"
        )
        
        if file_name:
            try:
                data = self.canvas.get_curve_data()
                with open(file_name, 'w') as f:
                    json.dump(data, f)
                self.statusBar.showMessage(f"曲线已保存到 {file_name}")
            except Exception as e:
                self.statusBar.showMessage(f"保存失败: {str(e)}")
    
    # 从文件加载曲线数据
    def load_curve(self):
        file_name, _ = QFileDialog.getOpenFileName(
            self,
            "加载曲线",
            "",
            "JSON Files (*.json);;All Files (*)"
        )
        
        if file_name:
            try:
                with open(file_name, 'r') as f:
                    data = json.load(f)
                self.canvas.set_curve_data(data)
                self.statusBar.showMessage(f"已加载曲线 {file_name}")
            except Exception as e:
                self.statusBar.showMessage(f"加载失败: {str(e)}") 