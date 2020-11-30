from PyQt5 import uic
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QApplication, QWidget, QMessageBox
import sys
from model import Model


class MainWindow(QWidget):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.ui = uic.loadUi("gui.ui", self)

    @pyqtSlot(name='on_pushButton_clicked')
    def _parse_parameters(self):
        try:
            ui = self.ui
            a = float(ui.lineEdit_generator_a.text())
            b = float(ui.lineEdit_generator_b.text())
            m = float(ui.lineEdit_m.text())
            d = float(ui.lineEdit_sigma.text())
            n = int(ui.lineEdit_queue_count.text())
            req_count = int(ui.lineEdit_request_count.text())
            reenter_prob = float(ui.lineEdit_reenter_probability.text())

            dt = float(ui.lineEdit_dt.text())
            model_time = Model(dt, req_count, reenter_prob, n)
            results_time = model_time.time_based_modelling(a, b, m, d)
            model_event = Model(dt, req_count, reenter_prob, n)
            results_event = model_event.event_based_modelling(a, b, m, d)
            self._show_results(results_time, results_event)

        except ValueError:
            QMessageBox.warning(self, 'Ошибка', 'Ошибка в данных!')
        except Exception as e:
            QMessageBox.critical(self, 'Ошибка', e)

    def _show_results(self, results_time, results_event):
        ui = self.ui
        req_done_count1, reenter1, missed1 = results_time
        ui.lineEdit_res_request_count.setText(str(req_done_count1))
        ui.lineEdit_res_reentered_count.setText(str(reenter1))
        ui.lineEdit_res_max_queue_size.setText(str(missed1))
        req_done_count2, reenter2, missed2 = results_event
        ui.lineEdit_res_request_count_e.setText(str(req_done_count2))
        ui.lineEdit_res_reentered_count_e.setText(str(reenter2))
        ui.lineEdit_res_max_queue_size_e.setText(str(missed2))


def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    return app.exec()


if __name__ == '__main__':
    main()