from banco import Banco

def main():
    banco = Banco()

    cliente1 = banco.crear_cliente("Juan Pérez", "123")
    cuenta1 = banco.crear_cuenta("123", "0001")
    cuenta1.depositar(1000)

    cliente2 = banco.crear_cliente("Ana Gómez", "456")
    cuenta2 = banco.crear_cuenta("456", "0002")
    cuenta2.depositar(500)

    banco.transferir("0001", "0002", 200)

    print("Saldo cuenta 0001:", cuenta1.consultar_saldo())
    print("Saldo cuenta 0002:", cuenta2.consultar_saldo())

if __name__ == "__main__":
    main()
