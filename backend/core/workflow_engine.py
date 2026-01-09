"""
Motor de Flujos de Trabajo Inteligente (Smart Workflow Engine)
Implementación prototipo en Python compatible con Vectora.
"""
import uuid
import re
from typing import List, Dict, Optional, Any
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
    DOWNLOAD = "descargar"
    UNKNOWN = "unknown"

class WorkflowStep:
    def __init__(self, action: ActionType, params: Dict[str, Any] = None):
        self.id = str(uuid.uuid4())[:8]
        self.action = action
        self.params = params or {}
        self.status = StepStatus.PENDING
        
    def to_dict(self):
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

    def to_dict(self):
        return {
            "workflow_id": self.id,
            "steps": [s.to_dict() for s in self.steps],
            "context": self.context
        }

class WorkflowAssistant:
    def __init__(self):
        # Patrones simples para detección de intención
        self.patterns = {
            r"(unir|juntar|combinar)": ActionType.MERGE,
            r"(dividir|separar|extraer)": ActionType.SPLIT,
            r"(convertir|pasar|transformar).*?(word|doc|excel|xls|imagen|jpg|png)": ActionType.CONVERT,
            r"(comprimir|reducir|optimizar)": ActionType.COMPRESS,
            r"(descargar|guardar|bajar)": ActionType.DOWNLOAD
        }
        
    def parse_intent(self, text: str) -> List[ActionType]:
        """Detecta acciones en el texto, respetando orden aproximado"""
        text = text.lower()
        detected_actions = []
        
        # Estrategia simple: dividir por conectores clave y analizar partes
        parts = re.split(r"(?: y | luego | despues | finalmente | para )", text)
        
        for part in parts:
            part_action = ActionType.UNKNOWN
            
            # Detectar conversión específica primero (captura formato)
            if "convertir" in part or "pasar" in part:
                 if any(x in part for x in ["word", "doc"]):
                     detected_actions.append((ActionType.CONVERT, {"format": "docx"}))
                     continue
                 elif any(x in part for x in ["excel", "xls"]):
                     detected_actions.append((ActionType.CONVERT, {"format": "xlsx"}))
                     continue
                 elif any(x in part for x in ["imagen", "jpg"]):
                     detected_actions.append((ActionType.CONVERT, {"format": "jpg"}))
                     continue

            # Detectar otras acciones
            for pattern, action in self.patterns.items():
                if re.search(pattern, part):
                    if action == ActionType.CONVERT: continue # Ya manejado arriba con params
                    detected_actions.append((action, {}))
                    break
                    
        return detected_actions

    def handle_user_intent(self, user_input: str, workflow: Workflow = None) -> Dict[str, Any]:
        """
        Función principal expuesta al frontend.
        Procesa el input, actualiza el workflow y genera respuesta.
        """
        if workflow is None:
            workflow = Workflow()
            
        actions_data = self.parse_intent(user_input)
        
        if not actions_data:
            return {
                "message": "No entendí muy bien qué quieres hacer. ¿Puedes intentar con 'Unir PDFs' o 'Convertir a Word'?",
                "workflow": workflow.to_dict(),
                "needs_input": False
            }
            
        new_step_count = 0
        for action_type, params in actions_data:
            # Lógica de encadenamiento inteligente
            # Si hay un paso previo, asumimos que el input de este paso es el output del anterior
            if workflow.get_last_step():
                params["input_source"] = f"step_ref:{workflow.get_last_step().id}"
            
            step = WorkflowStep(action_type, params)
            workflow.add_step(step)
            new_step_count += 1
            
        # Análisis Contextual y Slots Faltantes
        response_msg = ""
        missing_param = None
        
        # Especulativo: Sugerir 'descargar' si termina en conversión o unión
        last = workflow.get_last_step()
        if last and last.action in [ActionType.MERGE, ActionType.CONVERT]:
             response_msg = "He añadido los pasos. Al finalizar, ¿quieres descargar el archivo resultante?"
        
        # Validar slots (Ejemplo simple)
        for step in workflow.steps:
            if step.status == StepStatus.PENDING:
                if step.action == ActionType.CONVERT and "format" not in step.params:
                    # Falta formato
                    missing_param = "format"
                    response_msg = "¿A qué formato te gustaría convertir los archivos? (Word, Excel, Imagen)"
                    break # Detener y preguntar
        
        if not response_msg:
            action_names = [s.action.value.replace("_", " ") for s in workflow.steps[-new_step_count:]]
            response_msg = f"Entendido. Agregué: {', '.join(action_names)}. ¿Todo listo para ejecutar?"

        return {
            "message": response_msg,
            "workflow": workflow.to_dict(),
            "needs_input": missing_param is not None,
            "suggested_next_action": "descargar" if not missing_param else None
        }

# --- Bloque de Prueba (Main Stub) ---
if __name__ == "__main__":
    assistant = WorkflowAssistant()
    wf = Workflow()
    
    print("--- Inicio Simulación ---")
    user_in = "Une estos PDFs y luego pásalos a Word"
    print(f"User: {user_in}")
    
    result = assistant.handle_user_intent(user_in, wf)
    
    import json
    print("\nAssistant Response:")
    print(f"Message: {result['message']}")
    print("Workflow State:")
    print(json.dumps(result['workflow'], indent=2))
