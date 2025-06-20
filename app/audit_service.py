import json
import sqlite3
from datetime import datetime
from typing import Dict, Any, Optional, Tuple, List

import logging
logger = logging.getLogger(__name__)

class AuditService:
    DB_PATH = "audit_log.db"
    
    @classmethod
    def _init_db(cls):
        """Inicializar base de datos de auditoría"""
        try:
            conn = sqlite3.connect(cls.DB_PATH)
            cursor = conn.cursor()
            
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS audit_log (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp TEXT NOT NULL,
                    operation_type TEXT NOT NULL,
                    entity_type TEXT NOT NULL,
                    entity_id TEXT NOT NULL,
                    usuario TEXT NOT NULL,
                    estado_antes TEXT,
                    estado_despues TEXT,
                    campos_modificados TEXT,
                    status TEXT NOT NULL,
                    error TEXT,
                    args TEXT,
                    kwargs TEXT
                )
            ''')
            
            conn.commit()
            conn.close()
            
        except Exception as e:
            logger.error(f"Error inicializando base de datos: {e}")
    
    @classmethod
    def log_change(cls, operation_type: str, entity_type: str, entity_id: str,
                   estado_antes: Dict[str, Any], estado_despues: Dict[str, Any], 
                   usuario: str, status: str, error: Optional[str] = None, 
                   args: Optional[Tuple] = None, kwargs: Optional[Dict] = None):
        """Registrar cambio en la auditoría"""
        
        try:
            cls._init_db()
            
            # Identificar campos modificados
            campos_modificados = cls._get_modified_fields(estado_antes, estado_despues)
            
            # Preparar datos para insertar
            timestamp = datetime.now().isoformat()
            
            conn = sqlite3.connect(cls.DB_PATH)
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO audit_log 
                (timestamp, operation_type, entity_type, entity_id, usuario,
                 estado_antes, estado_despues, campos_modificados, status, error, args, kwargs)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                timestamp, 
                operation_type, 
                entity_type, 
                entity_id, 
                usuario,
                json.dumps(estado_antes), 
                json.dumps(estado_despues),
                json.dumps(campos_modificados), 
                status, 
                error,
                json.dumps(list(args)) if args else None,
                json.dumps(kwargs) if kwargs else None
            ))
            
            conn.commit()
            conn.close()
            
            # También log en archivo
            logger.info(f"AUDIT: {operation_type} on {entity_type}({entity_id}) by {usuario} - {status}")
            if campos_modificados:
                logger.info(f"Modified fields: {campos_modificados}")
                
        except Exception as e:
            logger.error(f"Error registrando en auditoría: {e}")
    
    @classmethod
    def _get_modified_fields(cls, antes: Dict[str, Any], despues: Dict[str, Any]) -> Dict[str, Any]:
        """Identificar campos que cambiaron"""
        modificados = {}
        
        try:
            all_keys = set(antes.keys()) | set(despues.keys())
            
            for key in all_keys:
                valor_antes = antes.get(key)
                valor_despues = despues.get(key)
                
                if valor_antes != valor_despues:
                    modificados[key] = {
                        'antes': valor_antes,
                        'despues': valor_despues
                    }
        
        except Exception as e:
            logger.error(f"Error identificando campos modificados: {e}")
            
        return modificados
    
    @classmethod
    def get_audit_history(cls, entity_id: Optional[str] = None, 
                         operation_type: Optional[str] = None) -> List[Tuple]:
        """Obtener historial de auditoría"""
        try:
            cls._init_db()
            
            conn = sqlite3.connect(cls.DB_PATH)
            cursor = conn.cursor()
            
            query = "SELECT * FROM audit_log WHERE 1=1"
            params = []
            
            if entity_id:
                query += " AND entity_id = ?"
                params.append(entity_id)
                
            if operation_type:
                query += " AND operation_type = ?"
                params.append(operation_type)
            
            query += " ORDER BY timestamp DESC"
            
            cursor.execute(query, params)
            results = cursor.fetchall()
            
            conn.close()
            return results
            
        except Exception as e:
            logger.error(f"Error obteniendo historial de auditoría: {e}")
            return []
    
    @classmethod
    def get_audit_summary(cls) -> Dict[str, Any]:
        """Obtener resumen de auditoría"""
        try:
            cls._init_db()
            
            conn = sqlite3.connect(cls.DB_PATH)
            cursor = conn.cursor()
            
            # Contar operaciones por tipo
            cursor.execute('''
                SELECT operation_type, COUNT(*) as count, status
                FROM audit_log 
                GROUP BY operation_type, status
                ORDER BY count DESC
            ''')
            
            operations = cursor.fetchall()
            
            # Contar total de registros
            cursor.execute('SELECT COUNT(*) FROM audit_log')
            total = cursor.fetchone()[0]
            
            conn.close()
            
            return {
                'total_operations': total,
                'operations_by_type': operations,
                'last_updated': datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error obteniendo resumen de auditoría: {e}")
            return {'error': str(e)}

# ===============================
# VERSIÓN SIMPLIFICADA (SIN TYPE HINTS)
# ===============================

class SimpleAuditService:
    """
    Versión simplificada sin type hints para evitar errores
    """
    DB_PATH = "simple_audit.log"
    
    @classmethod
    def log_change(cls, operation_type, entity_type, entity_id, 
                   estado_antes, estado_despues, usuario, status, 
                   error=None, args=None, kwargs=None):
        """Registrar cambio en archivo de texto simple"""
        
        try:
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            
            # Identificar campos modificados
            modificados = {}
            if estado_antes and estado_despues:
                for key in set(list(estado_antes.keys()) + list(estado_despues.keys())):
                    antes = estado_antes.get(key, 'N/A')
                    despues = estado_despues.get(key, 'N/A')
                    if antes != despues:
                        modificados[key] = f"{antes} -> {despues}"
            
            # Escribir en archivo
            with open(cls.DB_PATH, 'a', encoding='utf-8') as f:
                f.write(f"\n{'='*80}\n")
                f.write(f"TIMESTAMP: {timestamp}\n")
                f.write(f"OPERATION: {operation_type}\n")
                f.write(f"ENTITY: {entity_type}({entity_id})\n")
                f.write(f"USER: {usuario}\n")
                f.write(f"STATUS: {status}\n")
                
                if error:
                    f.write(f"ERROR: {error}\n")
                
                if modificados:
                    f.write("CHANGES:\n")
                    for campo, cambio in modificados.items():
                        f.write(f"  - {campo}: {cambio}\n")
                
                if args:
                    f.write(f"ARGS: {args}\n")
                
                if kwargs:
                    f.write(f"KWARGS: {kwargs}\n")
            
            # También mostrar en consola
            print(f"\n📋 AUDIT LOG: {operation_type} on {entity_type}({entity_id}) - {status}")
            if modificados:
                print(f"🔄 Changes: {modificados}")
                
        except Exception as e:
            print(f"❌ Error en audit log: {e}")
    
    @classmethod
    def get_audit_history(cls, entity_id=None, operation_type=None):
        """Leer historial desde archivo"""
        try:
            with open(cls.DB_PATH, 'r', encoding='utf-8') as f:
                content = f.read()
            return content.split('='*80)[-10:]  # Últimos 10 registros
        except FileNotFoundError:
            return ["No hay registros de auditoría aún"]
        except Exception as e:
            return [f"Error leyendo auditoría: {e}"]