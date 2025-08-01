"""
CONFIGO GUI - Animation Manager
===============================

Advanced animation system for smooth transitions, hover effects, and modern UI animations.
Provides a comprehensive set of animation utilities for the CONFIGO GUI.

Author: CONFIGO Team
"""

import math
from typing import Optional, Callable, Any, Dict
from PySide6.QtCore import (
    QPropertyAnimation, QEasingCurve, QTimer, QParallelAnimationGroup,
    QSequentialAnimationGroup, QAnimationGroup, QPoint, QRect, QSize
)
from PySide6.QtWidgets import QWidget, QGraphicsOpacityEffect, QGraphicsDropShadowEffect
from PySide6.QtGui import QColor


class AnimationManager:
    """
    Advanced animation manager for modern UI effects.
    
    Features:
    - Smooth transitions between screens
    - Hover effects with scaling and glow
    - Loading animations and spinners
    - Fade in/out effects
    - Slide animations
    - Bounce and elastic effects
    """
    
    def __init__(self):
        self.active_animations = {}
        self.animation_groups = {}
        
    def create_fade_animation(self, widget: QWidget, start_opacity: float = 0.0, 
                            end_opacity: float = 1.0, duration: int = 300) -> QPropertyAnimation:
        """
        Create a fade in/out animation for a widget.
        
        Args:
            widget: The widget to animate
            start_opacity: Starting opacity (0.0 to 1.0)
            end_opacity: Ending opacity (0.0 to 1.0)
            duration: Animation duration in milliseconds
            
        Returns:
            QPropertyAnimation instance
        """
        # Create opacity effect if not exists
        if not widget.graphicsEffect():
            opacity_effect = QGraphicsOpacityEffect()
            widget.setGraphicsEffect(opacity_effect)
        
        # Create animation
        animation = QPropertyAnimation(widget.graphicsEffect(), b"opacity")
        animation.setStartValue(start_opacity)
        animation.setEndValue(end_opacity)
        animation.setDuration(duration)
        animation.setEasingCurve(QEasingCurve.Type.OutCubic)
        
        return animation
    
    def create_slide_animation(self, widget: QWidget, start_pos: QPoint, end_pos: QPoint,
                             duration: int = 300) -> QPropertyAnimation:
        """
        Create a slide animation for a widget.
        
        Args:
            widget: The widget to animate
            start_pos: Starting position
            end_pos: Ending position
            duration: Animation duration in milliseconds
            
        Returns:
            QPropertyAnimation instance
        """
        animation = QPropertyAnimation(widget, b"pos")
        animation.setStartValue(start_pos)
        animation.setEndValue(end_pos)
        animation.setDuration(duration)
        animation.setEasingCurve(QEasingCurve.Type.OutCubic)
        
        return animation
    
    def create_scale_animation(self, widget: QWidget, start_scale: float = 1.0,
                             end_scale: float = 1.05, duration: int = 200) -> QPropertyAnimation:
        """
        Create a scale animation for hover effects.
        
        Args:
            widget: The widget to animate
            start_scale: Starting scale factor
            end_scale: Ending scale factor
            duration: Animation duration in milliseconds
            
        Returns:
            QPropertyAnimation instance
        """
        # Create transform animation
        animation = QPropertyAnimation(widget, b"geometry")
        
        # Calculate scaled geometry
        start_rect = widget.geometry()
        end_rect = QRect(
            int(start_rect.x() - (start_rect.width() * (end_scale - 1)) / 2),
            int(start_rect.y() - (start_rect.height() * (end_scale - 1)) / 2),
            int(start_rect.width() * end_scale),
            int(start_rect.height() * end_scale)
        )
        
        animation.setStartValue(start_rect)
        animation.setEndValue(end_rect)
        animation.setDuration(duration)
        animation.setEasingCurve(QEasingCurve.Type.OutCubic)
        
        return animation
    
    def create_glow_animation(self, widget: QWidget, start_color: QColor, end_color: QColor,
                            duration: int = 300) -> QPropertyAnimation:
        """
        Create a glow effect animation.
        
        Args:
            widget: The widget to animate
            start_color: Starting glow color
            end_color: Ending glow color
            duration: Animation duration in milliseconds
            
        Returns:
            QPropertyAnimation instance
        """
        # Create drop shadow effect if not exists
        if not widget.graphicsEffect():
            shadow_effect = QGraphicsDropShadowEffect()
            shadow_effect.setBlurRadius(20)
            shadow_effect.setOffset(0, 0)
            widget.setGraphicsEffect(shadow_effect)
        
        # Create animation for shadow color
        animation = QPropertyAnimation(widget.graphicsEffect(), b"color")
        animation.setStartValue(start_color)
        animation.setEndValue(end_color)
        animation.setDuration(duration)
        animation.setEasingCurve(QEasingCurve.Type.OutCubic)
        
        return animation
    
    def create_bounce_animation(self, widget: QWidget, property_name: bytes,
                              start_value: Any, end_value: Any, duration: int = 500) -> QPropertyAnimation:
        """
        Create a bounce animation with elastic easing.
        
        Args:
            widget: The widget to animate
            property_name: Property to animate (e.g., b"pos", b"geometry")
            start_value: Starting value
            end_value: Ending value
            duration: Animation duration in milliseconds
            
        Returns:
            QPropertyAnimation instance
        """
        animation = QPropertyAnimation(widget, property_name)
        animation.setStartValue(start_value)
        animation.setEndValue(end_value)
        animation.setDuration(duration)
        animation.setEasingCurve(QEasingCurve.Type.OutBounce)
        
        return animation
    
    def create_loading_spinner(self, widget: QWidget, duration: int = 1000) -> QPropertyAnimation:
        """
        Create a rotating loading spinner animation.
        
        Args:
            widget: The widget to animate (should be a QLabel with spinner icon)
            duration: Full rotation duration in milliseconds
            
        Returns:
            QPropertyAnimation instance
        """
        animation = QPropertyAnimation(widget, b"rotation")
        animation.setStartValue(0)
        animation.setEndValue(360)
        animation.setDuration(duration)
        animation.setLoopCount(-1)  # Infinite loop
        animation.setEasingCurve(QEasingCurve.Type.Linear)
        
        return animation
    
    def create_parallel_animation(self, animations: list) -> QParallelAnimationGroup:
        """
        Create a parallel animation group.
        
        Args:
            animations: List of QPropertyAnimation instances
            
        Returns:
            QParallelAnimationGroup instance
        """
        group = QParallelAnimationGroup()
        for animation in animations:
            group.addAnimation(animation)
        return group
    
    def create_sequential_animation(self, animations: list) -> QSequentialAnimationGroup:
        """
        Create a sequential animation group.
        
        Args:
            animations: List of QPropertyAnimation instances
            
        Returns:
            QSequentialAnimationGroup instance
        """
        group = QSequentialAnimationGroup()
        for animation in animations:
            group.addAnimation(animation)
        return group
    
    def create_hover_effect(self, widget: QWidget, scale_factor: float = 1.02,
                          glow_color: QColor = None) -> Dict[str, QPropertyAnimation]:
        """
        Create a comprehensive hover effect with scale and glow.
        
        Args:
            widget: The widget to apply hover effect to
            scale_factor: Scale factor for hover (default: 1.02)
            glow_color: Glow color (optional)
            
        Returns:
            Dictionary containing enter and exit animations
        """
        if glow_color is None:
            glow_color = QColor(99, 102, 241, 100)  # Primary color with alpha
        
        # Create animations
        scale_enter = self.create_scale_animation(widget, 1.0, scale_factor, 200)
        scale_exit = self.create_scale_animation(widget, scale_factor, 1.0, 200)
        
        glow_enter = self.create_glow_animation(widget, QColor(0, 0, 0, 0), glow_color, 200)
        glow_exit = self.create_glow_animation(widget, glow_color, QColor(0, 0, 0, 0), 200)
        
        # Create parallel groups
        enter_group = self.create_parallel_animation([scale_enter, glow_enter])
        exit_group = self.create_parallel_animation([scale_exit, glow_exit])
        
        return {
            'enter': enter_group,
            'exit': exit_group
        }
    
    def create_screen_transition(self, old_widget: QWidget, new_widget: QWidget,
                               direction: str = "slide_right") -> QSequentialAnimationGroup:
        """
        Create a smooth screen transition animation.
        
        Args:
            old_widget: Widget to animate out
            new_widget: Widget to animate in
            direction: Transition direction ("slide_right", "slide_left", "fade")
            
        Returns:
            QSequentialAnimationGroup instance
        """
        if direction == "fade":
            # Fade transition
            fade_out = self.create_fade_animation(old_widget, 1.0, 0.0, 300)
            fade_in = self.create_fade_animation(new_widget, 0.0, 1.0, 300)
            
            group = QSequentialAnimationGroup()
            group.addAnimation(fade_out)
            group.addAnimation(fade_in)
            return group
        
        elif direction == "slide_right":
            # Slide right transition
            old_slide = self.create_slide_animation(
                old_widget, 
                old_widget.pos(), 
                QPoint(old_widget.pos().x() - old_widget.width(), old_widget.pos().y()),
                300
            )
            new_slide = self.create_slide_animation(
                new_widget,
                QPoint(new_widget.pos().x() + new_widget.width(), new_widget.pos().y()),
                new_widget.pos(),
                300
            )
            
            group = QSequentialAnimationGroup()
            group.addAnimation(old_slide)
            group.addAnimation(new_slide)
            return group
        
        elif direction == "slide_left":
            # Slide left transition
            old_slide = self.create_slide_animation(
                old_widget,
                old_widget.pos(),
                QPoint(old_widget.pos().x() + old_widget.width(), old_widget.pos().y()),
                300
            )
            new_slide = self.create_slide_animation(
                new_widget,
                QPoint(new_widget.pos().x() - new_widget.width(), new_widget.pos().y()),
                new_widget.pos(),
                300
            )
            
            group = QSequentialAnimationGroup()
            group.addAnimation(old_slide)
            group.addAnimation(new_slide)
            return group
        
        return QSequentialAnimationGroup()
    
    def create_typing_animation(self, text_widget: QWidget, text: str, 
                              speed: int = 50) -> QTimer:
        """
        Create a typing animation effect.
        
        Args:
            text_widget: Widget to display text (QTextEdit or QLabel)
            text: Text to type
            speed: Typing speed in milliseconds per character
            
        Returns:
            QTimer instance for the typing animation
        """
        timer = QTimer()
        current_text = ""
        char_index = 0
        
        def type_next_char():
            nonlocal current_text, char_index
            if char_index < len(text):
                current_text += text[char_index]
                if hasattr(text_widget, 'setText'):
                    text_widget.setText(current_text)
                elif hasattr(text_widget, 'setPlainText'):
                    text_widget.setPlainText(current_text)
                char_index += 1
            else:
                timer.stop()
        
        timer.timeout.connect(type_next_char)
        timer.start(speed)
        
        return timer
    
    def create_progress_animation(self, progress_bar, start_value: int = 0,
                                end_value: int = 100, duration: int = 2000) -> QPropertyAnimation:
        """
        Create a smooth progress bar animation.
        
        Args:
            progress_bar: QProgressBar widget
            start_value: Starting progress value
            end_value: Ending progress value
            duration: Animation duration in milliseconds
            
        Returns:
            QPropertyAnimation instance
        """
        animation = QPropertyAnimation(progress_bar, b"value")
        animation.setStartValue(start_value)
        animation.setEndValue(end_value)
        animation.setDuration(duration)
        animation.setEasingCurve(QEasingCurve.Type.OutCubic)
        
        return animation
    
    def create_pulse_animation(self, widget: QWidget, min_scale: float = 0.95,
                             max_scale: float = 1.05, duration: int = 1000) -> QPropertyAnimation:
        """
        Create a pulsing animation effect.
        
        Args:
            widget: The widget to animate
            min_scale: Minimum scale factor
            max_scale: Maximum scale factor
            duration: Animation duration in milliseconds
            
        Returns:
            QPropertyAnimation instance
        """
        animation = QPropertyAnimation(widget, b"geometry")
        
        # Calculate scaled geometries
        original_rect = widget.geometry()
        min_rect = QRect(
            int(original_rect.x() - (original_rect.width() * (1 - min_scale)) / 2),
            int(original_rect.y() - (original_rect.height() * (1 - min_scale)) / 2),
            int(original_rect.width() * min_scale),
            int(original_rect.height() * min_scale)
        )
        max_rect = QRect(
            int(original_rect.x() - (original_rect.width() * (max_scale - 1)) / 2),
            int(original_rect.y() - (original_rect.height() * (max_scale - 1)) / 2),
            int(original_rect.width() * max_scale),
            int(original_rect.height() * max_scale)
        )
        
        animation.setStartValue(min_rect)
        animation.setEndValue(max_rect)
        animation.setDuration(duration)
        animation.setLoopCount(-1)  # Infinite loop
        animation.setEasingCurve(QEasingCurve.Type.InOutQuad)
        
        return animation
    
    def stop_all_animations(self):
        """Stop all active animations."""
        for animation in self.active_animations.values():
            if animation.isRunning():
                animation.stop()
        self.active_animations.clear()
        
        for group in self.animation_groups.values():
            if group.isRunning():
                group.stop()
        self.animation_groups.clear() 