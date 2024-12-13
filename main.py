import cv2
import io
import sqlite3
import sys
from PIL import Image
import os

from PyQt6.QtSql import QSqlDatabase, QSqlTableModel

import test
import datetime
from PyQt6 import uic
from PyQt6.QtWidgets import QApplication, QWidget, QFileDialog
from PyQt6.QtCore import QTimer
from PyQt6.QtGui import QImage, QPixmap

design = '''<?xml version="1.0" encoding="UTF-8"?>
<ui version="4.0">
 <class>Form</class>
 <widget class="QWidget" name="Form">
  <property name="geometry">
   <rect>
    <x>0</x>
    <y>0</y>
    <width>1104</width>
    <height>900</height>
   </rect>
  </property>
  <property name="windowTitle">
   <string>Form</string>
  </property>
  <widget class="QComboBox" name="modes">
   <property name="geometry">
    <rect>
     <x>20</x>
     <y>20</y>
     <width>181</width>
     <height>31</height>
    </rect>
   </property>
   <item>
    <property name="text">
     <string>Сделать снимок с веб камеры</string>
    </property>
   </item>
   <item>
    <property name="text">
     <string>Редактор</string>
    </property>
   </item>
   <item>
    <property name="text">
     <string>Просмотр</string>
    </property>
   </item>
   <item>
    <property name="text">
     <string>Добавить файл</string>
    </property>
   </item>
  </widget>
  <widget class="QLabel" name="veb_screen">
   <property name="geometry">
    <rect>
     <x>20</x>
     <y>70</y>
     <width>640</width>
     <height>640</height>
    </rect>
   </property>
   <property name="text">
    <string/>
   </property>
  </widget>
  <widget class="QPushButton" name="save_button">
   <property name="geometry">
    <rect>
     <x>820</x>
     <y>350</y>
     <width>161</width>
     <height>51</height>
    </rect>
   </property>
   <property name="text">
    <string>Сохранить изображение</string>
   </property>
  </widget>
  <widget class="QLineEdit" name="name_file">
   <property name="geometry">
    <rect>
     <x>790</x>
     <y>290</y>
     <width>231</width>
     <height>31</height>
    </rect>
   </property>
  </widget>
  <widget class="QLabel" name="label_2">
   <property name="geometry">
    <rect>
     <x>810</x>
     <y>240</y>
     <width>171</width>
     <height>31</height>
    </rect>
   </property>
   <property name="text">
    <string>Название сохраняемого файла</string>
   </property>
  </widget>
  <widget class="QLabel" name="eror_label">
   <property name="geometry">
    <rect>
     <x>750</x>
     <y>460</y>
     <width>231</width>
     <height>21</height>
    </rect>
   </property>
   <property name="text">
    <string/>
   </property>
  </widget>
  <widget class="QLineEdit" name="load_name">
   <property name="geometry">
    <rect>
     <x>20</x>
     <y>100</y>
     <width>181</width>
     <height>21</height>
    </rect>
   </property>
  </widget>
  <widget class="QLabel" name="loaded_image">
   <property name="geometry">
    <rect>
     <x>20</x>
     <y>170</y>
     <width>640</width>
     <height>640</height>
    </rect>
   </property>
   <property name="text">
    <string/>
   </property>
  </widget>
  <widget class="QPushButton" name="save_loaded_but">
   <property name="geometry">
    <rect>
     <x>910</x>
     <y>800</y>
     <width>161</width>
     <height>71</height>
    </rect>
   </property>
   <property name="text">
    <string>Сохранить изображение</string>
   </property>
  </widget>
  <widget class="QComboBox" name="filters">
   <property name="enabled">
    <bool>true</bool>
   </property>
   <property name="geometry">
    <rect>
     <x>20</x>
     <y>820</y>
     <width>221</width>
     <height>31</height>
    </rect>
   </property>
   <property name="currentText">
    <string>Фильтры</string>
   </property>
   <item>
    <property name="text">
     <string>Фильтры</string>
    </property>
   </item>
   <item>
    <property name="text">
     <string>Размытие</string>
    </property>
   </item>
   <item>
    <property name="text">
     <string>Только красный канал</string>
    </property>
   </item>
   <item>
    <property name="text">
     <string>Только синий канал</string>
    </property>
   </item>
   <item>
    <property name="text">
     <string>Только зеленый канал</string>
    </property>
   </item>
   <item>
    <property name="text">
     <string>Черно-Белый</string>
    </property>
   </item>
   <item>
    <property name="text">
     <string>Альтернативные цвета</string>
    </property>
   </item>
   <item>
    <property name="text">
     <string>Сепия</string>
    </property>
   </item>
   <item>
    <property name="text">
     <string>Сделать ярче</string>
    </property>
   </item>
  </widget>
  <widget class="QPushButton" name="load_but">
   <property name="geometry">
    <rect>
     <x>210</x>
     <y>100</y>
     <width>75</width>
     <height>23</height>
    </rect>
   </property>
   <property name="text">
    <string>загрузить</string>
   </property>
  </widget>
  <widget class="QLabel" name="label">
   <property name="geometry">
    <rect>
     <x>20</x>
     <y>70</y>
     <width>181</width>
     <height>16</height>
    </rect>
   </property>
   <property name="text">
    <string>Название загружаемого файла</string>
   </property>
  </widget>
  <widget class="QPushButton" name="discard_but">
   <property name="geometry">
    <rect>
     <x>380</x>
     <y>820</y>
     <width>151</width>
     <height>31</height>
    </rect>
   </property>
   <property name="text">
    <string>Отменить изменения</string>
   </property>
  </widget>
  <widget class="QLabel" name="load_eror_label">
   <property name="geometry">
    <rect>
     <x>20</x>
     <y>130</y>
     <width>261</width>
     <height>16</height>
    </rect>
   </property>
   <property name="text">
    <string/>
   </property>
  </widget>
  <widget class="QPushButton" name="use_filter_but">
   <property name="geometry">
    <rect>
     <x>250</x>
     <y>820</y>
     <width>121</width>
     <height>31</height>
    </rect>
   </property>
   <property name="text">
    <string>Применить фильтр</string>
   </property>
  </widget>
  <widget class="QLabel" name="label_3">
   <property name="geometry">
    <rect>
     <x>810</x>
     <y>680</y>
     <width>171</width>
     <height>16</height>
    </rect>
   </property>
   <property name="text">
    <string>Название сохраняемого файла</string>
   </property>
  </widget>
  <widget class="QLineEdit" name="saved_name">
   <property name="geometry">
    <rect>
     <x>780</x>
     <y>720</y>
     <width>221</width>
     <height>31</height>
    </rect>
   </property>
  </widget>
  <widget class="QPushButton" name="resave_but">
   <property name="geometry">
    <rect>
     <x>720</x>
     <y>800</y>
     <width>151</width>
     <height>71</height>
    </rect>
   </property>
   <property name="text">
    <string>Пересохранить текущее</string>
   </property>
  </widget>
  <widget class="QLabel" name="saved_eror_label">
   <property name="geometry">
    <rect>
     <x>760</x>
     <y>770</y>
     <width>271</width>
     <height>16</height>
    </rect>
   </property>
   <property name="text">
    <string/>
   </property>
  </widget>
  <widget class="QLabel" name="label_4">
   <property name="geometry">
    <rect>
     <x>20</x>
     <y>740</y>
     <width>271</width>
     <height>21</height>
    </rect>
   </property>
   <property name="text">
    <string>Заметка для изображения</string>
   </property>
  </widget>
  <widget class="QLineEdit" name="note_text">
   <property name="geometry">
    <rect>
     <x>20</x>
     <y>780</y>
     <width>541</width>
     <height>31</height>
    </rect>
   </property>
   <property name="autoFillBackground">
    <bool>false</bool>
   </property>
   <property name="text">
    <string/>
   </property>
   <property name="cursorPosition">
    <number>0</number>
   </property>
   <property name="clearButtonEnabled">
    <bool>false</bool>
   </property>
  </widget>
  <widget class="QLabel" name="label_5">
   <property name="geometry">
    <rect>
     <x>750</x>
     <y>290</y>
     <width>231</width>
     <height>16</height>
    </rect>
   </property>
   <property name="text">
    <string>Ваша заметка к данному изображению:</string>
   </property>
  </widget>
  <widget class="QLineEdit" name="note">
   <property name="enabled">
    <bool>true</bool>
   </property>
   <property name="geometry">
    <rect>
     <x>740</x>
     <y>320</y>
     <width>251</width>
     <height>71</height>
    </rect>
   </property>
  </widget>
  <widget class="QPushButton" name="save_red_note">
   <property name="geometry">
    <rect>
     <x>790</x>
     <y>410</y>
     <width>151</width>
     <height>41</height>
    </rect>
   </property>
   <property name="text">
    <string>Сохранить заметку</string>
   </property>
  </widget>
  <widget class="QPushButton" name="db_show_but">
   <property name="geometry">
    <rect>
     <x>110</x>
     <y>690</y>
     <width>141</width>
     <height>41</height>
    </rect>
   </property>
   <property name="text">
    <string>Показать изображение</string>
   </property>
  </widget>
  <widget class="QLabel" name="db_image">
   <property name="geometry">
    <rect>
     <x>430</x>
     <y>120</y>
     <width>640</width>
     <height>640</height>
    </rect>
   </property>
   <property name="text">
    <string/>
   </property>
  </widget>
  <widget class="QLineEdit" name="db_note">
   <property name="geometry">
    <rect>
     <x>600</x>
     <y>780</y>
     <width>471</width>
     <height>31</height>
    </rect>
   </property>
  </widget>
  <widget class="QTableView" name="db_table">
   <property name="enabled">
    <bool>false</bool>
   </property>
   <property name="geometry">
    <rect>
     <x>10</x>
     <y>230</y>
     <width>381</width>
     <height>421</height>
    </rect>
   </property>
  </widget>
  <widget class="QLabel" name="note_eror_label">
   <property name="geometry">
    <rect>
     <x>760</x>
     <y>380</y>
     <width>211</width>
     <height>21</height>
    </rect>
   </property>
   <property name="text">
    <string/>
   </property>
  </widget>
  <widget class="QLineEdit" name="db_name">
   <property name="geometry">
    <rect>
     <x>110</x>
     <y>660</y>
     <width>251</width>
     <height>20</height>
    </rect>
   </property>
  </widget>
  <widget class="QLabel" name="label_6">
   <property name="geometry">
    <rect>
     <x>50</x>
     <y>660</y>
     <width>51</width>
     <height>16</height>
    </rect>
   </property>
   <property name="text">
    <string>Название:</string>
   </property>
  </widget>
  <widget class="QLabel" name="db_eror_label">
   <property name="geometry">
    <rect>
     <x>380</x>
     <y>660</y>
     <width>231</width>
     <height>16</height>
    </rect>
   </property>
   <property name="text">
    <string/>
   </property>
  </widget>
  <widget class="QPushButton" name="del_from_bd">
   <property name="geometry">
    <rect>
     <x>270</x>
     <y>690</y>
     <width>141</width>
     <height>41</height>
    </rect>
   </property>
   <property name="text">
    <string>Удалить</string>
   </property>
  </widget>
  <widget class="QLabel" name="dialog_image">
   <property name="geometry">
    <rect>
     <x>20</x>
     <y>150</y>
     <width>640</width>
     <height>640</height>
    </rect>
   </property>
   <property name="text">
    <string/>
   </property>
  </widget>
  <widget class="QPushButton" name="load_dialog">
   <property name="geometry">
    <rect>
     <x>760</x>
     <y>500</y>
     <width>201</width>
     <height>81</height>
    </rect>
   </property>
   <property name="text">
    <string>Загрузить файл</string>
   </property>
  </widget>
  <widget class="QLabel" name="note_look">
   <property name="geometry">
    <rect>
     <x>510</x>
     <y>780</y>
     <width>541</width>
     <height>31</height>
    </rect>
   </property>
   <property name="text">
    <string/>
   </property>
  </widget>
  <widget class="QPushButton" name="repeat_save_but">
   <property name="geometry">
    <rect>
     <x>930</x>
     <y>750</y>
     <width>161</width>
     <height>131</height>
    </rect>
   </property>
   <property name="text">
    <string>Добавить</string>
   </property>
  </widget>
  <zorder>db_image</zorder>
  <zorder>modes</zorder>
  <zorder>veb_screen</zorder>
  <zorder>save_button</zorder>
  <zorder>name_file</zorder>
  <zorder>label_2</zorder>
  <zorder>eror_label</zorder>
  <zorder>load_name</zorder>
  <zorder>loaded_image</zorder>
  <zorder>save_loaded_but</zorder>
  <zorder>filters</zorder>
  <zorder>load_but</zorder>
  <zorder>label</zorder>
  <zorder>discard_but</zorder>
  <zorder>load_eror_label</zorder>
  <zorder>use_filter_but</zorder>
  <zorder>label_3</zorder>
  <zorder>saved_name</zorder>
  <zorder>resave_but</zorder>
  <zorder>saved_eror_label</zorder>
  <zorder>label_4</zorder>
  <zorder>note_text</zorder>
  <zorder>label_5</zorder>
  <zorder>note</zorder>
  <zorder>save_red_note</zorder>
  <zorder>db_show_but</zorder>
  <zorder>db_note</zorder>
  <zorder>db_table</zorder>
  <zorder>note_eror_label</zorder>
  <zorder>db_name</zorder>
  <zorder>label_6</zorder>
  <zorder>db_eror_label</zorder>
  <zorder>del_from_bd</zorder>
  <zorder>dialog_image</zorder>
  <zorder>load_dialog</zorder>
  <zorder>note_look</zorder>
  <zorder>repeat_save_but</zorder>
 </widget>
 <resources/>
 <connections/>
</ui>
'''


class CameraWidget(QWidget):
    def __init__(self):
        super().__init__()
        f = io.StringIO(design)
        uic.loadUi(f, self)
        current_file = os.path.realpath(__file__)
        self.current_directory = os.path.dirname(current_file)
        self.setWindowTitle('Проект PyQT6')
        self.setFixedSize(1100, 900)
        self.capture = cv2.VideoCapture(0)
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(60)
        self.save_button.clicked.connect(self.load_web)
        self.modes.activated.connect(self.change_mode)
        self.main_dir = os.getcwd()
        self.num_mode = 0
        self.change_mode(self.num_mode)
        self.load_but.clicked.connect(self.load_image)
        self.filters.activated.connect(self.change_filter)
        self.use_filter_but.clicked.connect(self.use_filter)
        self.num_filter = 0
        self.copy = f'{hash('PAVEL_ROSTISLAVOVICH')}'
        self.discard_but.clicked.connect(self.return_back)
        self.save_loaded_but.clicked.connect(self.save_loaded)
        self.resave_but.clicked.connect(self.resave)
        self.save_red_note.clicked.connect(self.resave_note)
        self.db_show_but.clicked.connect(self.show_db_image)
        self.del_from_bd.clicked.connect(self.remove_image)
        self.load_dialog.clicked.connect(self.load_dialog_but)
        self.repeat_save_but.clicked.connect(self.repeat)
        for elem in os.listdir(self.main_dir):
            if elem not in ['.idea', 'build', 'databased.sqlite', 'dist', 'images', 'main.py', 'project.ui', 'test.py',
                            'venv', '__pycache__', 'main.exe']:
                os.remove(os.path.realpath(elem))

    def repeat(self):
        self.change_mode(3)

    def remove_image(self):
        self.db_eror_label.setText('')
        try:
            if self.name_db_file in os.listdir('images'):
                self.db_image.setPixmap(QPixmap(''))
                con = sqlite3.connect("databased.sqlite")
                cursor = con.cursor()
                cursor.execute(f"DELETE from Images where name = '{self.name_db_file}'")
                con.commit()
                os.chdir('images')
                for elem in os.listdir(os.getcwd()):
                    if elem == self.name_db_file:
                        os.remove(os.path.realpath(elem))
                self.name_db_file = ''
                self.db_eror_label.setText('Изображение удалено')
                self.note_look.setText('')
                os.chdir(self.main_dir)
                self.mode_2_to_show()
            else:
                self.db_eror_label.setText('Загрузите изображение')
        except Exception:
            self.db_eror_label.setText('Загрузите изображение')

    def show_db_image(self):
        self.db_eror_label.setText('')
        if not self.db_name.text():
            self.db_eror_label.setText('Некорректное название файла')
            self.db_image.setPixmap(QPixmap(''))
        else:
            self.name_db_file = f'{self.db_name.text()}.png'
            if self.name_db_file in os.listdir('images'):
                os.chdir('images')
                self.db_image.setPixmap(QPixmap(QImage(self.name_db_file)))
                os.chdir(self.main_dir)
                con = sqlite3.connect("databased.sqlite")
                cursor = con.cursor()
                data = cursor.execute(f"SELECT description"
                                      f" from Images WHERE name == '{self.name_db_file}'").fetchall()[0][0]
                con.commit()
                self.note_look.setText(data)
            else:
                self.db_eror_label.setText('Такого файла нет в Базе данных')
                self.db_image.setPixmap(QPixmap(''))

    def resave(self):
        try:
            self.saved_eror_label.setText('')
            copy = Image.open(self.copy_name)
            os.chdir('images')
            copy.save(f'{self.name}.png')
            os.chdir(self.main_dir)
        except Exception:
            self.saved_eror_label.setText('Загрузите изображение')

    def resave_note(self):
        try:
            con = sqlite3.connect("databased.sqlite")
            cursor = con.cursor()
            cursor.execute(f"UPDATE Images SET description = '{self.note.text()}' WHERE name == '{f'{self.name}.png'}'")
            con.commit()
            self.eror_label.setText('Изображение успешно сохранено')
        except Exception:
            self.note_eror_label.setText('Загрузите изображение')

    def save_loaded(self):
        try:
            self.saved_eror_label.setText('')
            new_name = self.saved_name.text()
            if not new_name:
                self.saved_eror_label.setText('Некорректное название файла')
            else:
                new_name = f'{new_name}.png'
                if new_name in os.listdir('images'):
                    self.saved_eror_label.setText('Файл с таким названием уже существует')
                else:
                    copy = Image.open(self.copy_name)
                    os.chdir('images')
                    copy.save(new_name)
                    os.chdir(self.main_dir)
                    con = sqlite3.connect("databased.sqlite")
                    cursor = con.cursor()
                    cursor.execute(
                        f"INSERT INTO Images VALUES('{new_name}', '{self.note.text()}',"
                        f" '{datetime.datetime.now().strftime('%Y-%m-%d')}')")
                    con.commit()
        except Exception:
            self.saved_eror_label.setText('Загрузите изображение')

    def return_back(self):
        try:
            if self.loaded_image:
                os.chdir('images')
                self.loaded_image.setPixmap(QPixmap(QImage(f'{self.name}.png')))
                orig = Image.open(f'{self.name}.png')
                os.chdir(self.main_dir)
                orig.save(self.copy_name)
        except Exception:
            pass

    def change_filter(self, value):
        self.num_filter = value

    def use_filter(self):
        try:
            if self.num_filter == 8:
                test.brighter(self.copy_name)
            if self.num_filter == 7:
                test.sepia(self.copy_name)
            if self.num_filter == 6:
                test.negative(self.copy_name)
            if self.num_filter == 5:
                test.black_white(self.copy_name)
            if self.num_filter == 4:
                test.green_only(self.copy_name)
            if self.num_filter == 3:
                test.blue_only(self.copy_name)
            if self.num_filter == 2:
                test.red_only(self.copy_name)
            if self.num_filter == 1:
                test.blur(self.copy_name)
            self.loaded_image.setPixmap(QPixmap(QImage(self.copy_name)))
        except Exception:
            pass

    def load_image(self):
        self.filters.setCurrentIndex(0)
        self.name = self.load_name.text()
        self.load_eror_label.setText('')
        if not self.load_name.text():
            self.load_eror_label.setText('Некорректное название файла')
            self.loaded_image.setPixmap(QPixmap(''))
            self.copy_name = hash('s')
            self.note.setText('')
        elif f'{self.name}.png' not in os.listdir('images'):
            self.load_eror_label.setText('Такого файла не существует')
            self.loaded_image.setPixmap(QPixmap(''))
            self.copy_name = hash('s')
            self.note.setText('')
        else:
            os.chdir('images')
            self.loaded_image.setPixmap(QPixmap(QImage(f'{self.name}.png')))
            im = Image.open(f'{self.name}.png')
            x, y = im.size
            if x > y:
                im = im.resize((640, 480))
            elif x < y:
                im = im.resize((480, 640))
            else:
                im = im.resize((640, 640))
            os.chdir(self.main_dir)
            im.save(f'{self.copy}.png')
            self.copy_name = f'{self.copy}.png'
            con = sqlite3.connect("databased.sqlite")
            cursor = con.cursor()
            data = cursor.execute(f"SELECT description"
                                  f" from Images WHERE name == '{f'{self.name}.png'}'").fetchall()[0][0]
            con.commit()
            self.note.setText(data)
            self.note_eror_label.setText('')

    def mode_4_to_hide(self):
        self.dialog_image.hide()
        self.load_dialog.hide()
        self.label_4.hide()
        self.note_text.hide()
        self.eror_label.hide()
        self.repeat_save_but.hide()

    def mode_4_to_show(self):
        self.dialog_image.show()
        self.load_dialog.show()
        self.label_4.show()
        self.note_text.show()
        self.eror_label.show()
        self.repeat_save_but.show()

    def mode_1_to_hide(self):
        self.note_text.hide()
        self.veb_screen.hide()
        self.name_file.hide()
        self.label_2.hide()
        self.save_button.hide()
        self.eror_label.hide()
        self.label_4.hide()
        self.name_file.setText('')
        self.eror_label.setText('')

    def mode_1_to_show(self):
        self.veb_screen.show()
        self.name_file.show()
        self.label_2.show()
        self.save_button.show()
        self.eror_label.show()
        self.note_text.show()
        self.label_4.show()

    def mode_3_to_hide(self):
        self.saved_name.setText('')
        self.load_name.setText('')
        self.filters.setCurrentIndex(0)
        self.loaded_image.setPixmap(QPixmap(''))
        self.copy_name = hash('s')
        self.load_eror_label.setText('')
        self.saved_eror_label.setText('')
        self.note_text.setText('')
        self.note.setText('')
        self.load_eror_label.hide()
        self.discard_but.hide()
        self.label.hide()
        self.load_name.hide()
        self.load_but.hide()
        self.filters.hide()
        self.save_loaded_but.hide()
        self.loaded_image.hide()
        self.use_filter_but.hide()
        self.label_3.hide()
        self.resave_but.hide()
        self.saved_name.hide()
        self.note.hide()
        self.label_5.hide()
        self.save_red_note.hide()
        self.db_name.setText('')
        self.db_name.hide()
        self.note_eror_label.setText('')

    def mode_3_to_show(self):
        self.load_eror_label.show()
        self.discard_but.show()
        self.label.show()
        self.load_name.show()
        self.load_but.show()
        self.filters.show()
        self.save_loaded_but.show()
        self.loaded_image.show()
        self.use_filter_but.show()
        self.label_3.show()
        self.resave_but.show()
        self.saved_name.show()
        self.note.show()
        self.label_5.show()
        self.save_red_note.show()

    def mode_2_to_show(self):
        db = QSqlDatabase.addDatabase('QSQLITE')
        db.setDatabaseName('databased.sqlite')
        db.open()
        model = QSqlTableModel(self, db)
        model.setTable('Images')
        model.select()
        self.db_table.setModel(model)
        self.del_from_bd.show()
        self.db_table.show()
        self.db_show_but.show()
        self.db_name.show()
        self.label_6.show()
        self.note_look.show()

    def mode_2_to_hide(self):
        self.del_from_bd.hide()
        self.db_name.hide()
        self.db_table.hide()
        self.db_show_but.hide()
        self.db_note.hide()
        self.label_6.hide()
        self.db_note.setText('')
        self.db_image.setPixmap(QPixmap(''))
        self.db_eror_label.setText('')
        self.note_look.hide()
        self.note_look.setText('')

    def change_mode(self, value):
        self.num_mode = value
        if not self.num_mode:
            self.mode_3_to_hide()
            self.mode_2_to_hide()
            self.mode_4_to_hide()
            self.mode_1_to_show()
        elif self.num_mode == 1:
            self.mode_1_to_hide()
            self.mode_3_to_show()
            self.mode_2_to_hide()
            self.mode_4_to_hide()
        elif self.num_mode == 2:
            self.mode_1_to_hide()
            self.mode_3_to_hide()
            self.mode_2_to_show()
            self.mode_4_to_hide()
        else:
            self.mode_1_to_hide()
            self.mode_3_to_hide()
            self.mode_2_to_hide()
            self.mode_4_to_show()
            self.dialog_image.setText('Изображение не выбрано')
            self.dialog_file_name = QFileDialog.getOpenFileName(self, 'Выбрать картинку', '')[0]
            name = os.path.basename(self.dialog_file_name)
            if name not in os.listdir('images'):
                if 'png' in self.dialog_file_name:
                    im = Image.open(self.dialog_file_name)
                    x, y = im.size
                    if x > y:
                        im = im.resize((640, 480))
                    elif x < y:
                        im = im.resize((480, 640))
                    else:
                        im = im.resize((640, 640))
                    im.save(self.dialog_file_name)
                    self.pixmap = QPixmap(QImage(self.dialog_file_name))
                    self.dialog_image.setPixmap(self.pixmap)
                else:
                    self.dialog_file_name = ''
            else:
                self.eror_label.setText('Такой файл уже есть в Базе данных')

    def load_dialog_but(self):
        try:
            if not self.dialog_file_name:
                raise ValueError
            name = os.path.basename(self.dialog_file_name)
            if name in os.listdir('images'):
                self.eror_label.setText('Такой файл уже есть в Базе данных')
                self.dialog_file_name.setText('')
            else:
                copy = Image.open(self.dialog_file_name)
                os.chdir('images')
                copy.save(name)
                os.chdir(self.main_dir)
                con = sqlite3.connect("databased.sqlite")
                cursor = con.cursor()
                cursor.execute(
                    f"INSERT INTO Images VALUES('{name}', '{self.note_text.text()}',"
                    f" '{datetime.datetime.now().strftime('%Y-%m-%d')}')")
                con.commit()
                self.eror_label.setText('Файл сохранен')
        except ValueError:
            self.eror_label.setText('')
            self.dialog_image.setPixmap(QPixmap('Изображение не выбрано'))
        except Exception:
            self.eror_label.setText('Такой файл есть в Базе данных')
            self.dialog_image.setPixmap(QPixmap('Изображение не выбрано'))

    def update_frame(self):
        con, frame = self.capture.read()
        if con:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            height, width, channel = frame.shape
            bytes_per_line = 3 * width
            image = QImage(frame.data, width, height, bytes_per_line, QImage.Format.Format_RGB888)
            self.veb_screen.setPixmap(QPixmap.fromImage(image))
        else:
            self.veb_screen.setText('Не найдена камера')

    def closeEvent(self, event):
        self.capture.release()

    def load_web(self):
        self.eror_label.setText('')
        if self.name_file.text():
            name = f'{self.name_file.text()}.png'
            if name in os.listdir('images'):
                self.eror_label.setText('Файл с таким названием уже существует')
            else:
                ret, frame = self.capture.read()
                if not ret:
                    return
                data = datetime.datetime.now().strftime('%Y-%m-%d')
                os.chdir('images')
                cv2.imwrite(name, frame)
                os.chdir(self.main_dir)
                note = self.note_text.text()
                con = sqlite3.connect("databased.sqlite")
                cursor = con.cursor()
                cursor.execute(f"INSERT INTO Images VALUES('{name}', '{note}', '{data}')")
                con.commit()
                self.eror_label.setText('Изображение успешно сохранено')
        else:
            self.eror_label.setText('Неккоректное название')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    camera_widget = CameraWidget()
    camera_widget.show()
    sys.exit(app.exec())
