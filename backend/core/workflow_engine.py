"""
Motor de Flujos de Trabajo Inteligente (Smart Workflow Engine)
Implementación prototipo en Python compatible con Vectora.
"""
import uuid
import re
import unicodedata
from typing import List, Dict, Optional, Any, Tuple
from enum import Enum

class StepStatus(Enum):
    PENDING = "pending"
    COMPLETED = "completed"
    FAILED = "failed"

class ActionType(Enum):
    MERGE = "unir_pdf"
    SPLIT = "dividir_pdf"
    CONVERT = "convertir_pdf"
    COMPRESS = "comprimir_pdf"
    SECURITY = "seguridad_pdf"
    OCR = "ocr_pdf"
    DOWNLOAD = "descargar"
    UNKNOWN = "unknown"

class WorkflowStep:
    def __init__(self, action: ActionType, params: Dict[str, Any] = None):
        self.id = str(uuid.uuid4())[:8]
        self.action = action
        self.params = params or {}
        self.status = StepStatus.PENDING
        
    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "action": self.action.value,
            "params": self.params,
            "status": self.status.value
        }

class Workflow:
    def __init__(self):
        self.id = str(uuid.uuid4())
        self.steps: List[WorkflowStep] = []
        self.context: Dict[str, Any] = {}
        
    def add_step(self, step: WorkflowStep):
        self.steps.append(step)
        
    def get_last_step(self) -> Optional[WorkflowStep]:
        return self.steps[-1] if self.steps else None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "workflow_id": self.id,
            "steps": [s.to_dict() for s in self.steps],
            "context": self.context
        }

class WorkflowAssistant:
    def __init__(self):
        # Patrones para detección de intención (incluyendo conjugaciones comunes)
        self.patterns = {
            r"(unir|juntar|combinar|une|junta|combina|unific)": ActionType.MERGE,
            r"(dividir|separar|extraer|fragment|troce|parte)": ActionType.SPLIT,
            r"(convert|pas|transform|llev|cambi|vuelv|pasa)": ActionType.CONVERT,
            r"(comprim|reduc|optimiz|achic)": ActionType.COMPRESS,
            r"(descarg|guard|baj|salv)": ActionType.DOWNLOAD,
            r"(seguridad|prote|encrip|contrase)": ActionType.SECURITY,
            r"(ocr|texto|reconoc)": ActionType.OCR
        }
        
    def _normalize_text(self, text: str) -> str:
        """Elimina acentos y normaliza a minúsculas"""
        text = text.lower()
        return ''.join(
            c for c in unicodedata.normalize('NFD', text)
            if unicodedata.category(c) != 'Mn'
        )

    def parse_intent(self, text: str) -> List[Tuple[ActionType, Dict[str, Any]]]:
        """Detecta acciones en el texto de forma secuencial y robusta"""
        normalized = self._normalize_text(text)
        detected_actions = []
        
        # Split por conectores comunes con flexibilidad de espacios
        parts = re.split(r"\s+(?:y|luego|despues|finalmente|para|entonces)\s+|\.\s*", normalized)
        
        for part in parts:
            part = part.strip()
            if not part: continue
            
            found_in_part = False
            
            # 1. Lógica especial de conversión (necesita formato)
            if any(x in part for x in ["convert", "pas", "transform", "llev", "cambi", "vuelv"]):
                 params = {}
                 if any(x in part for x in ["word", "doc"]): params["format"] = "docx"
                 elif any(x in part for x in ["excel", "xls"]): params["format"] = "xlsx"
                 elif any(x in part for x in ["imagen", "jpg"]): params["format"] = "jpg"
                 elif any(x in part for x in ["png"]): params["format"] = "png"
                 elif any(x in part for x in ["pdf"]): params["format"] = "pdf"
                 
                 if "format" in params:
                     detected_actions.append((ActionType.CONVERT, params))
                     found_in_part = True
                     continue

            # 2. Búsqueda por patrones generales
            if not found_in_part:
                for pattern, action in self.patterns.items():
                    if re.search(pattern, part):
                        # Evitar duplicar conversión si ya se intentó arriba y falló el formato
                        if action == ActionType.CONVERT: continue
                        
                        detected_actions.append((action, {}))
                        found_in_part = True
                        break
                    
        return detected_actions

    def handle_user_intent(self, user_input: str, workflow: Optional[Workflow] = None) -> Dict[str, Any]:
        """
        Procesa el input del usuario, actualiza el flujo y genera respuesta.
        """
        if workflow is None:
            workflow = Workflow()
            
        actions_data = self.parse_intent(user_input)
        
        if not actions_data:
            return {
                "message": "¿Qué te gustaría hacer con tus archivos? Puedo unirlos, dividirlos, convertirlos o comprimirlos.",
                "workflow": workflow.to_dict(),
                "needs_input": False
            }
            
        new_step_count = 0
        for action_type, params in actions_data:
            # Encadenamiento: el output de uno es el input del siguiente
            if workflow.get_last_step():
                params["input_source"] = f"step_ref:{workflow.get_last_step().id}"
            
            step = WorkflowStep(action_type, params)
            workflow.add_step(step)
            new_step_count += 1
            
        # Generar respuesta contextual
        last_step = workflow.get_last_step()
        missing_param = None
        response_msg = ""

        # Validar si falta información crítica (SLOT FILLING)
        for step in workflow.steps:
            if step.status == StepStatus.PENDING:
                if step.action == ActionType.CONVERT and "format" not in step.params:
                    missing_param = "format"
                    response_msg = "¿A qué formato prefieres convertir? (Word, Excel, JPG, PNG)"
                    break
        
        if not response_msg:
            # Mensaje de éxito acumulativo
            action_names = [s.action.value.replace("_", " ") for s in workflow.steps[-new_step_count:]]
            if len(action_names) > 1:
                response_msg = f"Genial, he configurado los pasos: {', '.join(action_names)}. ¿Ejecutamos?"
            else:
                response_msg = f"Entendido, paso de '{action_names[0]}' añadido. ¿Algo más o ejecutamos?"

        return {
            "message": response_msg,
            "workflow": workflow.to_dict(),
            "needs_input": missing_param is not None,
            "can_execute": True if not missing_param else False
        }

# --- Bloque de Prueba (Main Stub) ---
if __name__ == "__main__":
    assistant = WorkflowAssistant()
    wf = Workflow()
    
    print("--- Inicio Simulación de Flujo Inteligente ---")
    inputs = [
        "Une estos PDFs y luego pásalos a Word",
        "También comprímelos un poco",
        "Y al final ponles contraseña"
    ]
    
    for i in inputs:
        print(f"\n> Usuario: {i}")
        result = assistant.handle_user_intent(i, wf)
        print(f"< Asistente: {result['message']}")
        
    import json
    print("\n--- Estado Final del Workflow ---")
    print(json.dumps(wf.to_dict(), indent=2))
