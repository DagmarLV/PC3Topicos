from app.banco import Banco
from app.audit_service import AuditService
import time

def main():
    print("🏦 Iniciando Sistema Bancario con AOP")
    print("=" * 50)
    
    # Crear instancia del banco
    banco = Banco()
    
    try:
        # 1. Crear clientes
        print("\n📋 Creando clientes...")
        cliente1 = banco.crear_cliente("Juan Pérez", "123")
        cliente2 = banco.crear_cliente("Ana Gómez", "456")
        print(f"✅ Cliente creado: {cliente1}")
        print(f"✅ Cliente creado: {cliente2}")
        
        # 2. Crear cuentas
        print("\n💳 Creando cuentas...")
        cuenta1 = banco.crear_cuenta("123", "0001")
        cuenta2 = banco.crear_cuenta("456", "0002")
        print(f"✅ Cuenta creada: {cuenta1.numero_cuenta}")
        print(f"✅ Cuenta creada: {cuenta2.numero_cuenta}")
        
        # 3. Realizar depósitos
        print("\n💰 Realizando depósitos...")
        cuenta1.depositar(1000)
        cuenta2.depositar(500)
        print(f"✅ Depósito en cuenta 0001: $1000")
        print(f"✅ Depósito en cuenta 0002: $500")
        
        # 4. Realizar transferencia
        print("\n🔄 Realizando transferencia...")
        banco.transferir("0001", "0002", 200)
        print(f"✅ Transferencia de $200 de 0001 a 0002")
        
        # 5. Mostrar saldos finales
        print("\n📊 Saldos finales:")
        print(f"💳 Cuenta 0001: ${cuenta1.consultar_saldo()}")
        print(f"💳 Cuenta 0002: ${cuenta2.consultar_saldo()}")
        
        # 6. Probar manejo de errores
        print("\n⚠️ Probando manejo de errores...")
        try:
            cuenta1.retirar(10000)  # Debería fallar
        except ValueError as e:
            print(f"❌ Error capturado: {e}")
        
        # 7. Mostrar algunos logs de auditoría
        print("\n📜 Últimos registros de auditoría:")
        audit_logs = AuditService.get_audit_history()
        for i, log in enumerate(audit_logs[:3]):  # Mostrar solo los 3 más recientes
            print(f"📝 Log {i+1}: {log[2]} en {log[3]} - {log[8]}")
            
    except Exception as e:
        print(f"❌ Error en ejecución: {e}")
    
    print("\n🎉 Ejecución completada")
    print("📁 Revisa los archivos generados:")
    print("   - banco_audit.log (logs de texto)")
    print("   - audit_log.db (base de datos SQLite)")

if __name__ == "__main__":
    main()