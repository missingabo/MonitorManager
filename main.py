import sys
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QComboBox, QSpinBox, QMessageBox
from monitores import mostrar_estado_monitores, obtener_salidas, listar_modos, cambiar_modo, posicionar_monitor, rotar_monitor, activar_o_desactivar, guardar_config, restaurar_config, modo_juego


class Ventana(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Control de Monitores")
        self.resize(800, 500)

        layout = QVBoxLayout()
        self.setLayout(layout)

        boton = QPushButton("Mostrar estado")
        layout.addWidget(boton)


        self.estado = QLabel("Aquí aparecerá el estado de los monitores")
        layout.addWidget(self.estado)

        boton.clicked.connect(self.mostrar_estado)

        self.combo = QComboBox(self)
        salidas = obtener_salidas()
        for salida in salidas:
            if salida["connected"]:
                self.combo.addItem(salida["name"])

        layout.addWidget(self.combo)
        self.combo.currentIndexChanged.connect(self.monitor_seleccionado)
        self.combo_modo = QComboBox(self)
        layout.addWidget(self.combo_modo)

        if self.combo.count() > 0:
            self.monitor_seleccionado()

        self.boton_modo = QPushButton("Cambiar modo")
        self.boton_modo.clicked.connect(self.aplicar_modo)
        layout.addWidget(self.boton_modo)

        self.pos_x = QSpinBox()
        self.pos_y = QSpinBox()

        self.pos_x.setRange(-10000, 10000)
        self.pos_y.setRange(-10000, 10000)

        layout.addWidget(self.pos_x)
        layout.addWidget(self.pos_y)

        self.boton_posicion = QPushButton("Cambiar posición")
        self.boton_posicion.clicked.connect(self.aplicar_posicion)
        layout.addWidget(self.boton_posicion)

        self.combo_rotacion = QComboBox(self)
        layout.addWidget(self.combo_rotacion)
        self.combo_rotacion.addItem("Normal", "none")
        self.combo_rotacion.addItem("90º Izquierda", "left")
        self.combo_rotacion.addItem("90º Derecha", "right")
        self.combo_rotacion.addItem("180º", "inverted")
        self.boton_rotacion = QPushButton("Cambiar rotación")
        self.boton_rotacion.clicked.connect(self.aplicar_rotacion)
        layout.addWidget(self.boton_rotacion)

        self.combo_estado = QComboBox(self)
        self.combo_estado.addItem("Activar", "enable")
        self.combo_estado.addItem("Desactivar", "disable")
        layout.addWidget(self.combo_estado)
        self.boton_estado = QPushButton("Aplicar")
        self.boton_estado.clicked.connect(self.aplicar_estado)
        layout.addWidget(self.boton_estado)

        self.configuracion = None

        self.boton_guardar = QPushButton("Guardar configuración")
        self.boton_guardar.clicked.connect(self.guardar_configuracion)
        layout.addWidget(self.boton_guardar)

        self.boton_restaurar = QPushButton("Restaurar configuración")
        self.boton_restaurar.clicked.connect(self.restaurar_configuracion)
        layout.addWidget(self.boton_restaurar)

        self.boton_juego = QPushButton("Modo juego")
        self.boton_juego.clicked.connect(self.aplicar_modo_juego)
        layout.addWidget(self.boton_juego)

    def aplicar_estado(self):       
        monitor = self.combo.currentText()
        accion = self.combo_estado.currentData()
        print("Acción seleccionada:", repr(accion))
        try:
            activar_o_desactivar(monitor, accion)
            QMessageBox.information(self, "Éxito", "Estado cambiado correctamente")
        except Exception as e:
            QMessageBox.critical(self, "Error al aplicar estado", str(e))
        

    def mostrar_estado(self):
        try:
            texto = mostrar_estado_monitores()
            self.estado.setText(texto)
        except Exception as e:
            QMessageBox.critical(self, "Error al consultar monitores", str(e))

    def monitor_seleccionado(self):
        monitor = self.combo.currentText()
        print("Monitor seleccionado:", monitor)  
        modos = listar_modos(monitor)       
        self.combo_modo.clear()
        for modo in modos:
            texto = f"{modo['size']['width']} x {modo['size']['height']} @ {modo['refreshRate']} Hz"
            self.combo_modo.addItem(texto, modo)

    def aplicar_modo(self):
        monitor = self.combo.currentText()
        modo = self.combo_modo.currentData()
        try:
            cambiar_modo(monitor, modo)
            QMessageBox.information(self, "Éxito", "Modo cambiado correctamente")
        except ValueError as e:
            QMessageBox.critical(self, "Error", str(e))

    def aplicar_posicion(self):
        monitor = self.combo.currentText()
        x = self.pos_x.value()
        y = self.pos_y.value()        
        try:
            posicionar_monitor(monitor, x, y)
            QMessageBox.information(self, "Éxito", "Posición cambiada correctamente")
        except ValueError as e:
            QMessageBox.critical(self, "Error", str(e))

    def aplicar_rotacion(self):
        monitor = self.combo.currentText()
        orientacion = self.combo_rotacion.currentData()
        try:
            rotar_monitor(monitor, orientacion)
            QMessageBox.information(self, "Éxito", "Monitor rotado correctamente")
        except Exception as e:
            QMessageBox.critical(self, "Error al rotar", str(e))        

    def guardar_configuracion(self):
        self.configuracion = guardar_config()
        print("CONFIGURACIÓN GUARDADA:")
        print(self.configuracion)
        QMessageBox.information(self, "Éxito", "Configuración guardada correctamente")

    def restaurar_configuracion(self):
        print("CONFIGURACIÓN A RESTAURAR:")
        print(self.configuracion)

        if self.configuracion is None:
            QMessageBox.warning(self, "Aviso", "No hay configuración que restaurar")
            return
        try:
            restaurar_config(self.configuracion)
            QMessageBox.information(self, "Éxito", "Restauración completada correctamente")
        except ValueError as e:
            QMessageBox.critical(self, "Error", str(e))

    def aplicar_modo_juego(self):
        try:
            self.configuracion = modo_juego()
            QMessageBox.information(self, "Modo juego", "Configuración de juego aplicada")
        except Exception as e:
            QMessageBox.critical(self, "Error al activar modo juego", str(e))
if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = Ventana()
    ventana.show()
    sys.exit(app.exec())

