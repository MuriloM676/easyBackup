import os
import sys
import shutil
import psutil
import random
from datetime import datetime
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QCheckBox, QListWidget, QListWidgetItem, QLabel, 
    QMessageBox, QGraphicsScene, QGraphicsView, QGraphicsRectItem, QProgressBar
)
from PyQt5.QtCore import Qt, QThread, pyqtSignal, QTimer, QRectF
from PyQt5.QtGui import QBrush, QColor

class CopyThread(QThread):
    progress = pyqtSignal(int)
    finished = pyqtSignal()
    error = pyqtSignal(str)

    def __init__(self, src_dirs, dst_dir):
        super().__init__()
        self.src_dirs = src_dirs
        self.dst_dir = dst_dir
        self.total_files = 0
        self.copied_files = 0

    def count_files(self, path):
        count = 0
        try:
            for root, _, files in os.walk(path):
                count += len(files)
        except Exception:
            pass
        return count

    def copy_with_progress(self, src, dst):
        try:
            if os.path.isdir(src):
                shutil.copytree(src, dst, dirs_exist_ok=True, copy_function=self.copy_file)
            else:
                shutil.copy2(src, dst)
                self.copied_files += 1
                self.progress.emit(int((self.copied_files / self.total_files) * 100))
        except Exception as e:
            self.error.emit(str(e))

    def copy_file(self, src, dst):
        shutil.copy2(src, dst)
        self.copied_files += 1
        self.progress.emit(int((self.copied_files / self.total_files) * 100))

    def run(self):
        try:
            for src_dir in self.src_dirs:
                self.total_files += self.count_files(src_dir)
            
            for src_dir in self.src_dirs:
                user = os.path.basename(src_dir)
                dst = os.path.join(self.dst_dir, user)
                self.copy_with_progress(src_dir, dst)
            self.finished.emit()
        except Exception as e:
            self.error.emit(str(e))

class DinoGame(QGraphicsView):
    def __init__(self):
        super().__init__()
        self.scene = QGraphicsScene(self)
        self.setScene(self.scene)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scene.setSceneRect(0, 0, 600, 200)

        # Chão
        self.ground = QGraphicsRectItem(0, 180, 600, 20)
        self.ground.setBrush(QBrush(QColor("#dcdcdc")))
        self.scene.addItem(self.ground)

        # Dinossauro
        self.dino = QGraphicsRectItem(50, 150, 30, 30)
        self.dino.setBrush(QBrush(QColor("#2ecc71")))
        self.scene.addItem(self.dino)
        self.dino_y = 150
        self.dino_velocity = 0
        self.is_jumping = False

        # Obstáculos
        self.obstacles = []
        self.obstacle_timer = QTimer()
        self.obstacle_timer.timeout.connect(self.add_obstacle)
        self.obstacle_timer.start(2000)

        # Animação
        self.animation_timer = QTimer()
        self.animation_timer.timeout.connect(self.update_animation)
        self.animation_timer.start(30)

    def add_obstacle(self):
        obstacle = QGraphicsRectItem(600, 160, 10, 20)
        obstacle.setBrush(QBrush(QColor("#e74c3c")))
        self.scene.addItem(obstacle)
        self.obstacles.append(obstacle)

    def update_animation(self):
        # Pulo automático do dinossauro
        if not self.is_jumping and random.random() < 0.05:
            self.is_jumping = True
            self.dino_velocity = -10

        if self.is_jumping:
            self.dino_y += self.dino_velocity
            self.dino_velocity += 0.5
            if self.dino_y >= 150:
                self.dino_y = 150
                self.dino_velocity = 0
                self.is_jumping = False
            self.dino.setRect(50, self.dino_y, 30, 30)

        # Mover obstáculos
        for obstacle in self.obstacles[:]:
            rect = obstacle.rect()
            rect.moveLeft(rect.left() - 5)
            obstacle.setRect(rect)
            if rect.right() < 0:
                self.scene.removeItem(obstacle)
                self.obstacles.remove(obstacle)

    def stop_animation(self):
        self.animation_timer.stop()
        self.obstacle_timer.stop()

class BackupApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Backup de Usuários")
        self.setGeometry(100, 100, 600, 400)
        self.selected_users = []
        self.init_ui()
        self.apply_styles()

    def init_ui(self):
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)
        self.layout.setContentsMargins(20, 20, 20, 20)
        self.layout.setSpacing(15)

        # Tela 1: Seleção de usuários
        self.user_selection_widget = QWidget()
        self.user_selection_layout = QVBoxLayout(self.user_selection_widget)
        self.user_selection_layout.setSpacing(10)
        
        self.label_users = QLabel("Selecione os usuários para backup:")
        self.user_selection_layout.addWidget(self.label_users)

        self.user_list = QListWidget()
        self.populate_users()
        self.user_selection_layout.addWidget(self.user_list)

        self.btn_next = QPushButton("Avançar")
        self.btn_next.clicked.connect(self.show_drive_selection)
        self.user_selection_layout.addWidget(self.btn_next)

        self.layout.addWidget(self.user_selection_widget)

        # Tela 2: Seleção de unidade
        self.drive_selection_widget = QWidget()
        self.drive_selection_layout = QVBoxLayout(self.drive_selection_widget)
        self.drive_selection_layout.setSpacing(10)
        
        self.label_drives = QLabel("Selecione a unidade de destino:")
        self.drive_selection_layout.addWidget(self.label_drives)

        self.drive_list = QListWidget()
        self.populate_drives()
        self.drive_selection_layout.addWidget(self.drive_list)

        self.btn_backup = QPushButton("Iniciar Backup")
        self.btn_backup.clicked.connect(self.start_backup)
        self.drive_selection_layout.addWidget(self.btn_backup)

        self.btn_back = QPushButton("Voltar")
        self.btn_back.clicked.connect(self.show_user_selection)
        self.drive_selection_layout.addWidget(self.btn_back)

        self.layout.addWidget(self.drive_selection_widget)
        self.drive_selection_widget.hide()

        # Tela 3: Progresso do backup com animação
        self.progress_widget = QWidget()
        self.progress_layout = QVBoxLayout(self.progress_widget)
        self.progress_layout.setSpacing(10)
        
        self.label_progress = QLabel("Realizando backup...")
        self.progress_layout.addWidget(self.label_progress)

        self.dino_game = DinoGame()
        self.progress_layout.addWidget(self.dino_game)

        self.progress_bar = QProgressBar()
        self.progress_bar.setMinimum(0)
        self.progress_bar.setMaximum(100)
        self.progress_layout.addWidget(self.progress_bar)

        self.btn_cancel = QPushButton("Cancelar")
        self.btn_cancel.clicked.connect(self.confirm_cancel)
        self.progress_layout.addWidget(self.btn_cancel)

        self.layout.addWidget(self.progress_widget)
        self.progress_widget.hide()

    def apply_styles(self):
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f0f4f8;
            }
            QLabel {
                font-size: 16px;
                font-weight: bold;
                color: #2c3e50;
            }
            QListWidget {
                background-color: #ffffff;
                border: 1px solid #dcdcdc;
                border-radius: 5px;
                padding: 5px;
                font-size: 14px;
                color: #34495e;
            }
            QListWidget::item {
                padding: 10px;
            }
            QListWidget::item:selected {
                background-color: #3498db;
                color: #ffffff;
            }
            QPushButton {
                background-color: #3498db;
                color: #ffffff;
                font-size: 14px;
                font-weight: bold;
                padding: 10px;
                border: none;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
            QPushButton:pressed {
                background-color: #20638f;
            }
            QProgressBar {
                border: 1px solid #dcdcdc;
                border-radius: 5px;
                text-align: center;
                height: 25px;
                background-color: #ecf0f1;
            }
            QProgressBar::chunk {
                background-color: #2ecc71;
                border-radius: 3px;
            }
        """)

    def populate_users(self):
        users_path = r"C:\Users"
        try:
            for user in os.listdir(users_path):
                user_path = os.path.join(users_path, user)
                if os.path.isdir(user_path) and user not in ["Public", "Default"]:
                    item = QListWidgetItem(user)
                    item.setFlags(item.flags() | Qt.ItemIsUserCheckable)
                    item.setCheckState(Qt.Unchecked)
                    self.user_list.addItem(item)
        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Erro ao listar usuários: {e}")

    def populate_drives(self):
        self.drive_list.clear()
        try:
            for partition in psutil.disk_partitions():
                if "removable" in partition.opts or partition.fstype in ["FAT32", "NTFS", "exFAT"]:
                    item = QListWidgetItem(f"{partition.device} ({partition.mountpoint})")
                    self.drive_list.addItem(item)
        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Erro ao listar unidades: {e}")

    def show_drive_selection(self):
        self.selected_users = []
        for i in range(self.user_list.count()):
            item = self.user_list.item(i)
            if item.checkState() == Qt.Checked:
                self.selected_users.append(os.path.join(r"C:\Users", item.text()))
        
        if not self.selected_users:
            QMessageBox.warning(self, "Aviso", "Selecione pelo menos um usuário!")
            return
        
        self.user_selection_widget.hide()
        self.drive_selection_widget.show()

    def show_user_selection(self):
        self.drive_selection_widget.hide()
        self.user_selection_widget.show()

    def start_backup(self):
        selected_drives = self.drive_list.selectedItems()
        if not selected_drives:
            QMessageBox.warning(self, "Aviso", "Selecione uma unidade de destino!")
            return

        drive = selected_drives[0].text().split("(")[1].strip(")")
        backup_date = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        self.backup_dir = os.path.join(drive, f"Backup_{backup_date}")

        try:
            os.makedirs(self.backup_dir, exist_ok=True)
            self.drive_selection_widget.hide()
            self.progress_widget.show()
            
            self.copy_thread = CopyThread(self.selected_users, self.backup_dir)
            self.copy_thread.progress.connect(self.update_progress)
            self.copy_thread.finished.connect(self.backup_finished)
            self.copy_thread.error.connect(self.backup_error)
            self.copy_thread.start()
            
        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Erro ao iniciar backup: {e}")
            self.progress_widget.hide()
            self.drive_selection_widget.show()

    def update_progress(self, value):
        self.progress_bar.setValue(value)

    def backup_finished(self):
        self.dino_game.stop_animation()
        QMessageBox.information(self, "Sucesso", "Backup concluído com sucesso!")
        self.progress_widget.hide()
        self.user_selection_widget.show()
        self.progress_bar.setValue(0)

    def backup_error(self, error):
        self.dino_game.stop_animation()
        QMessageBox.critical(self, "Erro", f"Erro durante o backup: {error}")
        self.progress_widget.hide()
        self.drive_selection_widget.show()
        self.progress_bar.setValue(0)

    def confirm_cancel(self):
        reply = QMessageBox.question(
            self, 
            "Confirmação", 
            "Deseja realmente cancelar o backup?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        if reply == QMessageBox.Yes:
            self.cancel_backup()

    def cancel_backup(self):
        if hasattr(self, 'copy_thread') and self.copy_thread.isRunning():
            self.copy_thread.terminate()
        self.dino_game.stop_animation()
        self.progress_widget.hide()
        self.drive_selection_widget.show()
        self.progress_bar.setValue(0)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = BackupApp()
    window.show()
    sys.exit(app.exec_())