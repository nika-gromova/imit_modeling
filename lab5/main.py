from PyQt5 import uic
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
import sys
from model import event_based_modelling


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.ui = uic.loadUi("gui.ui", self)

    @pyqtSlot(name='on_pushButton_clicked')
    def _parse_parameters(self):
        try:
            ui = self.ui
            client_m = float(ui.client_m.text())
            client_d = float(ui.client_d.text())
            op1_m = float(ui.operator_m_1.text())
            op1_d = float(ui.operator_d_1.text())
            op2_m = float(ui.operator_m_2.text())
            op2_d = float(ui.operator_d_2.text())
            op3_m = float(ui.operator_m_3.text())
            op3_d = float(ui.operator_d_3.text())
            comp1 = float(ui.computer_m_1.text())
            comp2 = float(ui.computer_m_2.text())
            n = int(ui.client_count.text())
            denial_probability, missed_clients = event_based_modelling(client_m, client_d, op1_m, op1_d, op2_m, op2_d,
                                                                       op3_m, op3_d, comp1, comp2,
                                                                       n)
            self._show_results(denial_probability, missed_clients)

        except ValueError:
            QMessageBox.warning(self, 'Ошибка', 'Ошибка в данных!')
        except Exception as e:
            QMessageBox.critical(self, 'Ошибка', e)

    def _show_results(self, denial_p, missed):
        ui = self.ui
        ui.denial_p.setText(str(denial_p))
        ui.missed_count.setText(str(missed))


def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    return app.exec()


if __name__ == '__main__':
    main()
