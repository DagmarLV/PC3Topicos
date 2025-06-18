from datetime import datetime

class Transaccion:
    def __init__(self, tipo, monto, cuenta_origen, cuenta_destino=None):
        self.tipo = tipo  # 'deposito', 'retiro', 'transferencia'
        self.monto = monto
        self.fecha = datetime.now()
        self.cuenta_origen = cuenta_origen
        self.cuenta_destino = cuenta_destino

    def __str__(self):
        if self.tipo == 'transferencia':
            return f"[{self.fecha}] Transferencia de {self.monto} de {self.cuenta_origen} a {self.cuenta_destino}"
        return f"[{self.fecha}] {self.tipo.capitalize()} de {self.monto} en cuenta {self.cuenta_origen}"
