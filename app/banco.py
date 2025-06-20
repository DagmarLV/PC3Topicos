from app.cliente import Cliente
from app.cuenta import Cuenta
from .decorators import log_data_changes, notify_by_email

class Banco:
    def __init__(self):
        self.clientes = {}
        self.cuentas = {}

    def _get_current_state(self):
        """Método para AOP - obtener estado actual"""
        return {
            'total_clientes': len(self.clientes),
            'total_cuentas': len(self.cuentas),
            'clientes': list(self.clientes.keys()),
            'cuentas': list(self.cuentas.keys())
        }

    @log_data_changes("crear_cliente")
    def crear_cliente(self, nombre, identificacion):
        cliente = Cliente(nombre, identificacion)
        self.clientes[identificacion] = cliente
        return cliente

    @log_data_changes("crear_cuenta")
    def crear_cuenta(self, identificacion, numero_cuenta):
        if identificacion not in self.clientes:
            raise ValueError("Cliente no encontrado")
        cuenta = Cuenta(numero_cuenta)
        self.clientes[identificacion].agregar_cuenta(cuenta)
        self.cuentas[numero_cuenta] = cuenta
        return cuenta

    @log_data_changes("transferencia")
    @notify_by_email("transferencia", "transferencia")
    def transferir(self, origen, destino, monto):
        c_origen = self.cuentas[origen]
        c_destino = self.cuentas[destino]
        c_origen.retirar(monto)
        c_destino.depositar(monto)
