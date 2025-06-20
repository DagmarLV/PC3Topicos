import functools
import logging
from datetime import datetime
import json
from typing import Any, Dict, Optional
from .email_service import EmailService
from .audit_service import AuditService

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('banco_audit.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

def log_data_changes(operation_type: str = ""):
    """
    Decorador para registrar cambios de datos automáticamente
    """
    def decorator(func):
        @functools.wraps(func)
        def wrapper(self, *args, **kwargs):
            # Obtener estado antes de la operación
            estado_antes = self._get_current_state() if hasattr(self, '_get_current_state') else {}
            
            try:
                # Ejecutar la función original
                resultado = func(self, *args, **kwargs)
                
                # Obtener estado después de la operación
                estado_despues = self._get_current_state() if hasattr(self, '_get_current_state') else {}
                
                # Registrar la operación exitosa
                AuditService.log_change(
                    operation_type=operation_type or func.__name__,
                    entity_type=self.__class__.__name__,
                    entity_id=getattr(self, 'numero_cuenta', getattr(self, 'identificacion', 'unknown')),
                    estado_antes=estado_antes,
                    estado_despues=estado_despues,
                    usuario="sistema",  # Aquí podrías obtener el usuario actual
                    status="SUCCESS",
                    args=args,
                    kwargs=kwargs
                )
                
                return resultado
                
            except Exception as e:
                # Registrar error
                AuditService.log_change(
                    operation_type=operation_type or func.__name__,
                    entity_type=self.__class__.__name__,
                    entity_id=getattr(self, 'numero_cuenta', getattr(self, 'identificacion', 'unknown')),
                    estado_antes=estado_antes,
                    estado_despues={},
                    usuario="sistema",
                    status="ERROR",
                    error=str(e),
                    args=args,
                    kwargs=kwargs
                )
                raise
                
        return wrapper
    return decorator

def notify_by_email(event_type: str = "", template: str = "default"):
    """
    Decorador para envío automático de emails
    """
    def decorator(func):
        @functools.wraps(func)
        def wrapper(self, *args, **kwargs):
            try:
                # Ejecutar función original
                resultado = func(self, *args, **kwargs)
                
                # Enviar notificación por email
                EmailService.send_notification(
                    event_type=event_type or func.__name__,
                    entity=self,
                    template=template,
                    args=args,
                    kwargs=kwargs,
                    resultado=resultado
                )
                
                return resultado
                
            except Exception as e:
                # Enviar email de error si es necesario
                if event_type in ['transferencia', 'login', 'update_administrativo']:
                    EmailService.send_error_notification(
                        event_type=event_type,
                        entity=self,
                        error=str(e),
                        args=args,
                        kwargs=kwargs
                    )
                raise
                
        return wrapper
    return decorator
