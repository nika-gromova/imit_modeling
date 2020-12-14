from PyQt5 import uic
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
import sys
from model import Model


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
            time_limit = float(ui.time_limit.text())
            op1_m = float(ui.prof_m.text())
            op1_d = float(ui.prof_d.text())
            op2_m = float(ui.mag_m.text())
            op2_d = float(ui.mag_d.text())
            count_p = int(ui.prof_count.text())
            count_m = int(ui.mag_count.text())
            n = int(ui.client_count.text())

            model = Model(1e-3, n)

            denial_p, not_passed, reenter, passed, generated = model.time_based_modelling(client_m, client_d,
                                                                                          op1_m, op1_d, op2_m,
                                                                                          op2_d, count_p, count_m,
                                                                                          time_limit)
            self._show_results(denial_p, not_passed, reenter, passed, generated)

        except ValueError:
            QMessageBox.warning(self, 'Ошибка', 'Ошибка в данных!')
        except Exception as e:
            QMessageBox.critical(self, 'Ошибка', e)

    def _show_results(self, denial_p, not_passed, reenter, passed, generated):
        ui = self.ui
        ui.denial_p.setText(str(denial_p))
        ui.not_passed.setText(str(not_passed))
        ui.reenter.setText(str(reenter))
        ui.passed.setText(str(passed))
        ui.generated.setText(str(generated))


def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    return app.exec()


if __name__ == '__main__':
    main()
