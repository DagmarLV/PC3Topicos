from app.cliente import Cliente
from app.cuenta import Cuenta

class Banco:
    def __init__(self):
        self.clientes = {}
        self.cuentas = {}

    def crear_cliente(self, nombre, identificacion):
        cliente = Cliente(nombre, identificacion)
        self.clientes[identificacion] = cliente
        return cliente

    def crear_cuenta(self, identificacion, numero_cuenta):
        if identificacion not in self.clientes:
            raise ValueError("Cliente no encontrado")
        cuenta = Cuenta(numero_cuenta)
        self.clientes[identificacion].agregar_cuenta(cuenta)
        self.cuentas[numero_cuenta] = cuenta
        return cuenta

    def transferir(self, origen, destino, monto):
        c_origen = self.cuentas[origen]
        c_destino = self.cuentas[destino]
        c_origen.retirar(monto)
        c_destino.depositar(monto)
