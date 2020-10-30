from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication
import sys
import interfaz
from minizinc import Instance, Model, Solver


class ExampleApp(QtWidgets.QMainWindow,interfaz.Ui_MainWindow):
    def __init__(self, parent=None):
        super(ExampleApp, self).__init__(parent)
        self.setupUi(self)
        self.btn1.clicked.connect(self.resolver)
        
        self.btn1_2.clicked.connect(self.limpiar)

   
#|1000,800,1000,900,|800,150,3300,250|
    
    def resolver(self):
        #Se crea el archivo dzn con los datos ingresados
        path = "../Modelo/Datos.dzn"
        file = open(path, "w")
        #Se 
        file.write("dias="+ str(self.spinDias.value())+";\n")
        file.write("clientes="+str(self.spinClientes.value())+";\n")
        file.write("plantaEnergetica=[|"+self.plainTextN.toPlainText()+
                  ","+self.plainTextCN.toPlainText()+",|" +self.plainTextH.toPlainText()+
                  ","+self.plainTextCH.toPlainText()+",|"+self.plainTextT.toPlainText()+
                  ","+self.plainTextTC.toPlainText()+"|"+"];\n")
        file.write("demanda=["+ self.textNecesidades.toPlainText()+"];\n")
        file.write("diasRegimen="+str(self.spinRegimen.value())+";\n")
        file.write("porcentaje="+str(self.doubleSpinPorcentaje.value())+";\n")
        #Se cierra el archivo
        file.close()
        #Se carga el modelo
        M1 = Model("../Modelo/PlantaEnergia.mzn")
        #Se añaden los datos
        M1.add_file("../Modelo/Datos.dzn")
        #Se selecciona el solver
        solver = Solver.lookup("coin-bc")
        instance = Instance(solver, M1)
        #Se ejecuta el modelo
        result = instance.solve()
      
        #Se muestran resultados
        if(result.solution is None):
            self.labelResultado.setText("Insatisfactible")
        else:
            self.labelResultado.setText("Satisfactible")
            self.labelCosto.setText(str(getattr(result.solution, 'costoTotal')))
            matriz=getattr(result.solution, 'produccion')
            self.textN.setPlainText(str(matriz[0]))
            self.textH.setPlainText(str(matriz[1]))
            self.textT.setPlainText(str(matriz[2]))

    #Funcion que limpia todos los campos
    def limpiar(self):
        self.plainTextN.setPlainText("")
        self.plainTextCN.setPlainText("")
        self.plainTextH.setPlainText("")
        self.plainTextCH.setPlainText("")
        self.plainTextT.setPlainText("")
        self.plainTextTC.setPlainText("")
        self.textNecesidades.setPlainText("")
        self.labelResultado.setText("")
        self.labelCosto.setText("")
        self.textN.setPlainText("")
        self.textH.setPlainText("")
        self.textT.setPlainText("")
        self.spinDias.setValue(0)
        self.spinClientes.setValue(0)
        self.spinRegimen.setValue(0)
        self.doubleSpinPorcentaje.setValue(0)
  


def main():
    app = QApplication(sys.argv)
    form = ExampleApp()
    form.show()
    app.exec_()

if __name__ == '__main__':
    main()