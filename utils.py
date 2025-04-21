from PyQt5.QtCore import QPointF
from PyQt5.QtGui import QColor

#将QPointF转换为字典
def point_to_dict(point: QPointF) -> dict:
    return {'x': point.x(), 'y': point.y()}

#将字典转换为QPointF
def dict_to_point(point_dict: dict) -> QPointF:
    return QPointF(point_dict['x'], point_dict['y'])

#将QColor转换为字典
def color_to_dict(color: QColor) -> dict:
    return {
        'red': color.red(),
        'green': color.green(),
        'blue': color.blue(),
        'alpha': color.alpha()
    }

# 将字典转换为QColor
def dict_to_color(color_dict: dict) -> QColor:
    return QColor(
        color_dict['red'],
        color_dict['green'],
        color_dict['blue'],
        color_dict['alpha']
    ) 