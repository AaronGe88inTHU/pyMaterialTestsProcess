import sys
from PyQt5 import QtCore, QtWidgets
from Ui_Dialog import Ui_Dialog
import Transformer
import numpy as np
import matplotlib.pyplot as plt

class Main_Dialog(QtWidgets.QMainWindow, Ui_Dialog):
    def __init__(self,  parent = None):
        super(Main_Dialog, self).__init__(parent)
        self.setupUi(self)
        self.pushButton.clicked.connect(self.slot_original_file)
        self.pushButton_2.clicked.connect(self.slot_formed_file)
        self.pushButton_3.clicked.connect(self.slot_calculate_curves)



        self.lineEdit.returnPressed.connect(self.slot_set_YoungModule)
        self.lineEdit_4.returnPressed.connect(self.slot_set_coef)
    
        self.original_file = None
        self.formed_file = None
        self.YoungModule = 210000.
        self.coef = 0
        self.lineEdit.setText(str(self.YoungModule))
        self.lineEdit_4.setText(str(self.coef))
 
    @QtCore.pyqtSlot(bool)
    def slot_original_file(self,  triggered):
        fileName = QtWidgets.QFileDialog.getOpenFileName(self,  u"打开原始板材曲线",u"",
                                                 u"Excel文件(*.xlsx *.xls)")
        if not fileName[0] == u"":
            self.original_file = fileName[0]
            QtWidgets.QMessageBox.information(self, self.tr(u"打开原始板材曲线成功"),\
                                u"成功", QtWidgets.QMessageBox.Ok)
        else:
            QtWidgets.QMessageBox.warning(self, self.tr(u"打开原始板材曲线错误"),\
                                u"失败", QtWidgets.QMessageBox.Cancel)
            return
            
    @QtCore.pyqtSlot(bool)
    def slot_formed_file(self, triggered):
        fileName = QtWidgets.QFileDialog.getOpenFileName(self,  u"打开加工后板材曲线",u"",
                                                 u"Excel文件(*.xlsx *.xls)")
        if not fileName[0] == u"":
            self.formed_file = fileName[0]
            QtWidgets.QMessageBox.information(self, self.tr(u"打开加工后曲线成功"),\
                                u"成功", QtWidgets.QMessageBox.Ok)

        else:
            QtWidgets.QMessageBox.warning(self, self.tr(u"打开加工后板材曲线错误"),\
                                u"失败", QtWidgets.QMessageBox.Cancel)
            return

    @QtCore.pyqtSlot(bool)
    def slot_calculate_curves(self, triggered):
        if self.original_file == None or self.formed_file == None:
            QtWidgets.QMessageBox.warning(self, self.tr(u"打开文件"),\
                                u"请检查输入文件", QtWidgets.QMessageBox.Cancel)
            return

        origin_all, formed = Transformer.read_files(self.original_file, self.formed_file)

        sorted_keys = sorted(origin_all.keys(), key=lambda x: float(x))

        original = origin_all[sorted_keys[0]]

        res = Transformer.transform_low_rate(original, formed)
        #print(res.x)
        transed = np.array([formed[:, 0], Transformer.transform(res.x, original, formed)]).T
        plt.plot(original[:, 0], original[:, 1],'k')
        plt.plot(formed[:, 0], formed[:, 1],'r')

        output = original[:,0] + res.x[0], original[:, 1]+res.x[1]
        #df = pd.DataFrame(np.array(output).T)
        #df.to_excel("500.xlsx")

        plt.plot(transed[:,0], transed[:,1])
        plt.plot(output[0], output[1],'b')


        fileName = QtWidgets.QFileDialog.getSaveFileName(self,  u"保存加工后板材曲线",u"",
                                                 u"Excel文件(*.xlsx *.xls)") 
        outputs = Transformer.transform_all(origin_all, res, self.coef, self.YoungModule)
        Transformer.output_to_excel(fileName[0], outputs)

        plt.show()
        self.lineEdit_2.setText('{0:.4f}'.format(res.x[0]))
        self.lineEdit_3.setText('{0:.1f}'.format(res.x[1]))
    
    @QtCore.pyqtSlot()
    def slot_set_YoungModule(self):
        self.YoungModule = float(self.lineEdit.text())

    @QtCore.pyqtSlot()
    def slot_set_coef(self):
        self.coef = float(self.lineEdit4.text())
        
if __name__ == "__main__":
    
    #print("lll")
    app = QtWidgets.QApplication(sys.argv)
    main_dialog = Main_Dialog()
    main_dialog.show()
    sys.exit(app.exec_())