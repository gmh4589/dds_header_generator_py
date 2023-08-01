
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox, QFileDialog
from PyQt5 import uic
import sys

import codec_list


class MainWindow(QMainWindow):

    def __init__(self):
        super(MainWindow, self).__init__()
        self.window = uic.loadUi('dds_hg.ui', self)
        self.file_name = ''
        window = self.window

        codecs = [key for key in codec_list.codec_list]
        window.cInput.addItems(codecs)
        window.cInput.setCurrentText('BC3_UNORM')
        window.okBTN.clicked.connect(self.dds_save)
        window.cancelBTN.clicked.connect(window.close)
        window.fileBTN.clicked.connect(self.fileOpen)
        window.folderBTN.clicked.connect(self.folderOpen)

        self.show()

    def folderOpen(self):
        options = QFileDialog.Options()
        options |= QFileDialog.ShowDirsOnly | QFileDialog.DontUseNativeDialog
        self.file_name = QFileDialog.getExistingDirectory(None, "Выберите папку", "", options=options)
        print(self.file_name)

    def fileOpen(self):
        self.file_name = QFileDialog.getOpenFileName(self, 'Open File')[0]
        print(self.file_name)

    def dds_save(self):

        if self.file_name:
            with open(self.file_name, 'rb') as sf:
                sf.seek(int(self.window.oData.value()))
                data = sf.read()
        else:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Warning)
            msg.setText("Файл не выбран!")
            msg.setWindowTitle("ВНИМАНИЕ!")
            msg.setStandardButtons(QMessageBox.Ok)
            msg.exec()
            return

        x = int(self.window.wInput.value())
        y = int(self.window.hInput.value())
        codec = self.window.cInput.currentText()
        flags = codec_list.codec_list[codec]['flags']
        cdc = codec_list.codec_list[codec]['codec']
        bpp = codec_list.codec_list[codec]['bpp']
        rgba_mask = codec_list.codec_list[codec]['rgb_mask']
        h_flg = codec_list.codec_list[codec]['head_flg']

        with open('temp.dds', 'wb') as dds_file:
            dds_file.write(b'DDS\x20\x7C\x00\x00\x00' + h_flg +  # DDS Header
                           x.to_bytes(4, 'little') + # Height
                           y.to_bytes(4, 'little') * 2 + # width and linear size
                           b'\x01\x00\x00\x00' * 2 + b'\x00' * 44 + b'\x20\x00\x00\x00' +
                           flags + cdc + bpp + rgba_mask + b'\x08\x10\x40\x00' + b'\x00' * 16 + data)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    sys.exit(app.exec())
