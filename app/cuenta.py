from .decorators import log_data_changes, notify_by_email

class Cuenta:
    def __init__(self, numero_cuenta, saldo_inicial=0):
        self.numero_cuenta = numero_cuenta
        self.saldo = saldo_inicial

    def _get_current_state(self):
        """Método para AOP - obtener estado actual"""
        return {
            'numero_cuenta': self.numero_cuenta,
            'saldo': self.saldo
        }

    @log_data_changes("deposito")
    @notify_by_email("saldo_update", "saldo_update")
    def depositar(self, monto):
        self.saldo += monto

    @log_data_changes("retiro")
    @notify_by_email("saldo_update", "saldo_update")
    def retirar(self, monto):
        if monto > self.saldo:
            raise ValueError("Fondos insuficientes")
        self.saldo -= monto

    def consultar_saldo(self):
        return self.saldo
