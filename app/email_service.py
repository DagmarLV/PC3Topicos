import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import Dict, Any, Optional, Tuple
import json
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

class EmailService:
    # Configuración del servidor SMTP (ajustar según necesidades)
    SMTP_SERVER = "smtp.gmail.com"  # Ejemplo para Gmail
    SMTP_PORT = 587
    EMAIL_USER = "tu_email@gmail.com"  # Configurar
    EMAIL_PASSWORD = "tu_password"      # Configurar
    
    # Templates de emails
    TEMPLATES = {
        'login': {
            'subject': 'Acceso al Sistema Bancario',
            'body': '''
            Estimado cliente,
            
            Se ha registrado un acceso a su cuenta en el sistema bancario.
            
            Detalles:
            - Fecha: {timestamp}
            - Usuario: {usuario}
            
            Si no fue usted, contacte inmediatamente con soporte.
            
            Saludos,
            Banco Sistema
            '''
        },
        'transferencia': {
            'subject': 'Confirmación de Transferencia',
            'body': '''
            Estimado cliente,
            
            Su transferencia ha sido procesada exitosamente.
            
            Detalles:
            - Monto: ${monto}
            - Cuenta origen: {cuenta_origen}
            - Cuenta destino: {cuenta_destino}
            - Fecha: {timestamp}
            - Nuevo saldo: ${nuevo_saldo}
            
            Saludos,
            Banco Sistema
            '''
        },
        'saldo_update': {
            'subject': 'Actualización de Saldo',
            'body': '''
            Estimado cliente,
            
            Se ha registrado un cambio en el saldo de su cuenta.
            
            Detalles:
            - Cuenta: {numero_cuenta}
            - Saldo anterior: ${saldo_anterior}
            - Saldo actual: ${saldo_actual}
            - Operación: {operacion}
            - Fecha: {timestamp}
            
            Saludos,
            Banco Sistema
            '''
        },
        'error': {
            'subject': 'Error en Operación Bancaria',
            'body': '''
            Estimado cliente,
            
            Se ha producido un error al procesar su operación.
            
            Detalles:
            - Operación: {operacion}
            - Error: {error}
            - Fecha: {timestamp}
            
            Por favor, contacte con soporte.
            
            Saludos,
            Banco Sistema
            '''
        }
    }
    
    @classmethod
    def send_notification(cls, event_type: str, entity: Any, template: str = "default",
                         args: Optional[Tuple] = None, kwargs: Optional[Dict] = None, 
                         resultado: Any = None):
        """Enviar notificación por email"""
        
        try:
            # Obtener email del cliente (esto debe implementarse según tu lógica)
            email_destino = cls._get_client_email(entity)
            
            if not email_destino:
                logger.warning(f"No se pudo obtener email para notificación {event_type}")
                return
            
            # Preparar contenido del email
            template_data = cls._prepare_template_data(event_type, entity, args, kwargs, resultado)
            
            if event_type in cls.TEMPLATES:
                template_info = cls.TEMPLATES[event_type]
                subject = template_info['subject']
                body = template_info['body'].format(**template_data)
            else:
                subject = f"Notificación - {event_type}"
                body = f"Se ha ejecutado la operación: {event_type}\nDetalles: {json.dumps(template_data, indent=2)}"
            
            cls._send_email(email_destino, subject, body)
            
            logger.info(f"Email enviado para {event_type} a {email_destino}")
            
        except Exception as e:
            logger.error(f"Error enviando email para {event_type}: {str(e)}")
    
    @classmethod
    def send_error_notification(cls, event_type: str, entity: Any, error: str,
                               args: Optional[Tuple] = None, kwargs: Optional[Dict] = None):
        """Enviar notificación de error"""
        
        try:
            email_destino = cls._get_client_email(entity)
            
            if not email_destino:
                return
            
            template_data = {
                'operacion': event_type,
                'error': error,
                'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }
            
            template_info = cls.TEMPLATES['error']
            subject = template_info['subject']
            body = template_info['body'].format(**template_data)
            
            cls._send_email(email_destino, subject, body)
            
            logger.info(f"Email de error enviado para {event_type} a {email_destino}")
            
        except Exception as e:
            logger.error(f"Error enviando email de error: {str(e)}")
    
    @classmethod
    def _get_client_email(cls, entity) -> str:
        """Obtener email del cliente - implementar según tu lógica"""
        # Por ahora retornamos un email de prueba
        # En la implementación real, deberías obtener el email del cliente desde la base de datos
        if hasattr(entity, 'numero_cuenta'):
            return f"cliente_{entity.numero_cuenta}@email.com"
        elif hasattr(entity, 'identificacion'):
            return f"cliente_{entity.identificacion}@email.com"
        return "cliente@email.com"
    
    @classmethod
    def _prepare_template_data(cls, event_type: str, entity: Any, 
                              args: Optional[Tuple], kwargs: Optional[Dict], 
                              resultado: Any) -> Dict[str, Any]:
        """Preparar datos para el template del email"""
        
        data = {
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'event_type': event_type
        }
        
        # Datos específicos según el tipo de entidad
        if hasattr(entity, 'numero_cuenta'):
            data['numero_cuenta'] = entity.numero_cuenta
            data['saldo_actual'] = entity.saldo
        
        if hasattr(entity, 'identificacion'):
            data['usuario'] = entity.identificacion
        
        # Datos específicos según el tipo de evento
        if event_type == 'transferencia' and args:
            data.update({
                'cuenta_origen': args[0] if len(args) > 0 else 'N/A',
                'cuenta_destino': args[1] if len(args) > 1 else 'N/A',
                'monto': args[2] if len(args) > 2 else 'N/A'
            })
        
        return data
    
    @classmethod
    def _send_email(cls, to_email: str, subject: str, body: str):
        """Enviar email usando SMTP"""
        
        # En desarrollo, solo loggear el email
        logger.info(f"EMAIL TO: {to_email}")
        logger.info(f"SUBJECT: {subject}")
        logger.info(f"BODY: {body}")
        logger.info("=" * 50)
        
        # Para producción, descomentar el código SMTP:
        """
        try:
            msg = MIMEMultipart()
            msg['From'] = cls.EMAIL_USER
            msg['To'] = to_email
            msg['Subject'] = subject
            
            msg.attach(MIMEText(body, 'plain'))
            
            server = smtplib.SMTP(cls.SMTP_SERVER, cls.SMTP_PORT)
            server.starttls()
            server.login(cls.EMAIL_USER, cls.EMAIL_PASSWORD)
            
            text = msg.as_string()
            server.sendmail(cls.EMAIL_USER, to_email, text)
            server.quit()
            
        except Exception as e:
            logger.error(f"Error enviando email SMTP: {str(e)}")
            raise
        """