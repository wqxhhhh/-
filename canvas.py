from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import QPainter, QPainterPath, QPen, QColor, QBrush
from PyQt5.QtCore import Qt, QPointF

# 继承自Qwidget，自定义的QT组件
class Canvas(QWidget):
    def __init__(self):
        super().__init__()
        self.points = []  # 存储所有点
        self.selected_point = None  # 当前选中的点（用于拖拽）
        self.show_points = True  # 是否显示控制点
        self.curve_color = QColor(Qt.blue)  # 曲线颜色
        self.curve_width = 2  # 曲线宽度
        self.setMouseTracking(True)
        
    def catmull_rom_spline(self, p0, p1, p2, p3, t):
        """计算 Catmull-Rom 样条曲线上的点"""
        t2 = t * t
        t3 = t2 * t
        
        # Catmull-Rom 样条曲线公式
        x = 0.5 * ((2 * p1.x()) +
                  (-p0.x() + p2.x()) * t +
                  (2 * p0.x() - 5 * p1.x() + 4 * p2.x() - p3.x()) * t2 +
                  (-p0.x() + 3 * p1.x() - 3 * p2.x() + p3.x()) * t3)
        
        y = 0.5 * ((2 * p1.y()) +
                  (-p0.y() + p2.y()) * t +
                  (2 * p0.y() - 5 * p1.y() + 4 * p2.y() - p3.y()) * t2 +
                  (-p0.y() + 3 * p1.y() - 3 * p2.y() + p3.y()) * t3)
        
        return QPointF(x, y)
        
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        # 绘制背景
        painter.fillRect(self.rect(), Qt.white)
        
        if len(self.points) > 1:
            # 创建并绘制光滑曲线路径
            path = QPainterPath()
            path.moveTo(self.points[0])
            
            # 使用 Catmull-Rom 样条曲线连接点
            for i in range(len(self.points) - 1):
                # 获取四个控制点
                p0 = self.points[max(0, i-1)]
                p1 = self.points[i]
                p2 = self.points[i+1]
                p3 = self.points[min(len(self.points)-1, i+2)]
                
                # 在两点之间生成多个插值点
                for t in range(1, 11):
                    t = t / 10.0
                    point = self.catmull_rom_spline(p0, p1, p2, p3, t)
                    path.lineTo(point)
            
            # 绘制曲线
            pen = QPen(self.curve_color, self.curve_width)
            painter.setPen(pen)
            painter.drawPath(path)
        
        # 只在需要时绘制点
        if self.show_points:
            brush = QBrush(Qt.red)
            painter.setBrush(brush)
            for point in self.points:
                painter.drawEllipse(point, 5, 5)
    
    #处理鼠标点击的事件
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            pos = event.pos()
            
            # 检查是否点击了现有的点
            for i, point in enumerate(self.points):
                #如果鼠标点击的位置在当前已有点的10个像素的范围内，则意味着选中该点
                if (point - pos).manhattanLength() < 10:  
                    self.selected_point = i
                    return
            
            # 如果没有点击现有点，则添加新点
            self.points.append(pos)
            self.selected_point = len(self.points) - 1
            #更新图
            self.update()
    
    def mouseMoveEvent(self, event):
        if self.selected_point is not None and event.buttons() & Qt.LeftButton:
            # 移动选中的点
            self.points[self.selected_point] = event.pos()
            self.update()
    
    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.selected_point = None
            
    def get_curve_data(self):
        #获取曲线数据
        return {
            'points': [(p.x(), p.y()) for p in self.points],
            'color': self.curve_color.name(),
            'width': self.curve_width,
            'show_points': self.show_points
        }
        
    def set_curve_data(self, data):
        #设置曲线数据
        self.points = [QPointF(x, y) for x, y in data['points']]
        self.curve_color = QColor(data['color'])
        self.curve_width = data['width']
        self.show_points = data['show_points']
        self.update() 