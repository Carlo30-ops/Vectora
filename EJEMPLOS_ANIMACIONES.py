"""
Ejemplo de integración de animaciones Apple-style en widgets Vectora
Copia el código relevante a tus widgets operacionales
"""

# EJEMPLO 1: Agregar HoverEffect a botones
# ==========================================

from ui.styles.animations import HoverEffect, AnimationHelper, TransitionManager
from PySide6.QtWidgets import QPushButton


class ExampleOperationWidget:
    """Ejemplo de uso de animaciones en un widget operacional"""
    
    def __init__(self):
        self.process_button = QPushButton("Procesar")
        
        # Agregar efecto hover Apple-style
        HoverEffect(self.process_button)
        
        # Aplicar otros estilos
        self.process_button.setObjectName("primaryButton")


# EJEMPLO 2: Transición entre vistas
# ===================================

class MainWindowWithTransitions:
    """Ejemplo de transiciones suaves entre vistas"""
    
    def navigate_to_view(self, view_name: str):
        """Navega a una vista con transición suave"""
        
        current_view = self.stacked_widget.currentWidget()
        new_view = self.views.get(view_name)
        
        if current_view and new_view:
            # Transición suave entre widgets
            TransitionManager.transition_between_widgets(
                current_view, 
                new_view,
                duration=300  # 300ms es el estándar Apple
            )
        
        self.stacked_widget.setCurrentWidget(new_view)


# EJEMPLO 3: Animación escalonada en Dashboard
# ============================================

class DashboardWithAnimation:
    """Dashboard con animaciones escalonadas de entrada"""
    
    def setup_staggered_animations(self):
        """Configura animaciones escalonadas para las tarjetas"""
        
        # Lista de cards del dashboard
        cards = [
            self.merge_card,
            self.split_card,
            self.compress_card,
            self.convert_card,
            self.security_card,
            self.ocr_card,
            self.batch_card,
        ]
        
        # Animar con 50ms de retardo entre cada una
        TransitionManager.staggered_animation(
            cards,
            duration=300,      # Cada animación dura 300ms
            stagger_delay=50   # 50ms entre cada una
        )


# EJEMPLO 4: Fade in al cargar datos
# ==================================

class OperationWidgetWithFade:
    """Widget que hace fade in cuando carga datos"""
    
    def on_data_loaded(self):
        """Llamado cuando los datos se cargan"""
        
        # Hacer fade in del contenedor de resultados
        animation = AnimationHelper.create_fade_in(
            self.results_container,
            duration=300
        )
        animation.start()


# EJEMPLO 5: Cambios de tema con transición
# ==========================================

class ThemeAwareWidget:
    """Widget que responde a cambios de tema con transición"""
    
    def __init__(self):
        from ui.styles.theme_manager import theme_manager
        
        # Conectar señal de cambio de tema
        theme_manager.theme_changed.connect(self.on_theme_changed)
    
    def on_theme_changed(self, new_theme: str):
        """Llamado cuando cambia el tema"""
        
        # El QSS se aplica automáticamente
        # Pero puedes hacer cosas adicionales aquí
        print(f"Tema cambiado a: {new_theme}")


# EJEMPLO 6: Animación personalizada de progreso
# =============================================

class ProgressWithAnimation:
    """Progreso con animación de barra suave"""
    
    def update_progress(self, value: int):
        """Actualiza el progreso con animación suave"""
        
        # La animación se aplica automáticamente en QSS
        # con transition: width 300ms ease-in-out
        self.progress_bar.setValue(value)


# ============================================
# CÓMO IMPLEMENTAR EN TUS WIDGETS ACTUALES
# ============================================

"""
1. MERGE WIDGET - Agregar animación a botones:

   from ui.styles.animations import HoverEffect
   
   class MergeWidget:
       def __init__(self):
           # ... código existente ...
           
           # Agregar efectos hover
           HoverEffect(self.merge_button)
           HoverEffect(self.clear_button)


2. SPLIT WIDGET - Agregar fade in a resultados:

   from ui.styles.animations import AnimationHelper
   
   class SplitWidget:
       def on_split_complete(self, files):
           # Hacer fade in de resultados
           animation = AnimationHelper.create_fade_in(self.results_frame, 300)
           animation.start()


3. DASHBOARD - Agregar staggered animations:

   from ui.styles.animations import TransitionManager
   
   class Dashboard:
       def __init__(self):
           # ... código existente ...
           
           # Animar entrada de cards
           self.setup_staggered_animations()
       
       def setup_staggered_animations(self):
           cards = [self.card1, self.card2, ...]
           TransitionManager.staggered_animation(cards, 300, 50)
"""

print("""
✨ ANIMACIONES APPLE-STYLE IMPLEMENTADAS ✨

Estas funciones están disponibles:
- HoverEffect(): Efectos hover suaves en botones
- AnimationHelper.create_fade_in(): Fade in suave
- AnimationHelper.create_fade_out(): Fade out suave
- AnimationHelper.create_slide_in_left(): Slide desde izquierda
- TransitionManager.transition_between_widgets(): Cambio de vista
- TransitionManager.staggered_animation(): Animaciones escalonadas

Duración estándar: 300ms (Apple-style)

Para usar en tus widgets, importa:
from ui.styles.animations import HoverEffect, AnimationHelper, TransitionManager
""")
