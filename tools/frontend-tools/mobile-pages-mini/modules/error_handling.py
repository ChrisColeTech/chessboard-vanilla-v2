"""
Centralized error handling and exception management for template-based page generator.
"""

import sys
import traceback
import logging
from pathlib import Path
from typing import Optional, Dict, Any, Callable, Type, Union
from functools import wraps
from dataclasses import dataclass
from enum import Enum


class ErrorSeverity(Enum):
    """Error severity levels."""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


@dataclass
class ErrorContext:
    """Context information for error reporting."""
    operation: str
    component: str
    inputs: Dict[str, Any]
    stage: str = ""
    suggestions: list = None
    
    def __post_init__(self):
        if self.suggestions is None:
            self.suggestions = []


class GeneratorError(Exception):
    """Base exception for all generator errors."""
    
    def __init__(self, message: str, context: Optional[ErrorContext] = None, 
                 severity: ErrorSeverity = ErrorSeverity.HIGH, cause: Optional[Exception] = None):
        super().__init__(message)
        self.context = context
        self.severity = severity
        self.cause = cause
        self.timestamp = None


class ProjectStructureError(GeneratorError):
    """Errors related to project structure and configuration."""
    pass


class TemplateError(GeneratorError):
    """Errors related to template processing."""
    pass


class FileOperationError(GeneratorError):
    """Errors related to file operations."""
    pass


class RoutingError(GeneratorError):
    """Errors related to routing updates."""
    pass


class ValidationError(GeneratorError):
    """Errors related to validation."""
    pass


class DependencyError(GeneratorError):
    """Errors related to dependency management."""
    pass


class ErrorHandler:
    """Centralized error handling and logging."""
    
    def __init__(self, log_file: Optional[Path] = None, verbose: bool = False):
        self.verbose = verbose
        self.error_count = 0
        self.warning_count = 0
        self._setup_logging(log_file)
        
        # Error recovery strategies
        self.recovery_strategies: Dict[Type[Exception], Callable] = {
            FileNotFoundError: self._handle_file_not_found,
            PermissionError: self._handle_permission_error,
            ProjectStructureError: self._handle_project_structure_error,
            TemplateError: self._handle_template_error,
            FileOperationError: self._handle_file_operation_error,
            RoutingError: self._handle_routing_error,
            ValidationError: self._handle_validation_error,
            DependencyError: self._handle_dependency_error,
        }
    
    def _setup_logging(self, log_file: Optional[Path]):
        """Setup logging configuration."""
        # Create logger
        self.logger = logging.getLogger('template_generator')
        self.logger.setLevel(logging.DEBUG if self.verbose else logging.INFO)
        
        # Clear existing handlers
        self.logger.handlers.clear()
        
        # Console handler
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(logging.INFO)
        console_format = logging.Formatter('%(levelname)s: %(message)s')
        console_handler.setFormatter(console_format)
        self.logger.addHandler(console_handler)
        
        # File handler (if specified)
        if log_file:
            try:
                log_file.parent.mkdir(parents=True, exist_ok=True)
                file_handler = logging.FileHandler(log_file)
                file_handler.setLevel(logging.DEBUG)
                file_format = logging.Formatter(
                    '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
                )
                file_handler.setFormatter(file_format)
                self.logger.addHandler(file_handler)
            except Exception:
                # If file logging fails, continue without it
                pass
    
    def handle_exception(self, error: Exception, context: Optional[ErrorContext] = None,
                        exit_on_critical: bool = True) -> bool:
        """
        Handle an exception with appropriate logging and recovery.
        
        Returns:
            bool: True if error was handled and execution can continue, False otherwise
        """
        # Wrap non-GeneratorError exceptions
        if not isinstance(error, GeneratorError):
            error = self._wrap_exception(error, context)
        
        # Log the error
        self._log_error(error)
        
        # Update counters
        if error.severity == ErrorSeverity.CRITICAL:
            self.error_count += 1
        else:
            self.warning_count += 1
        
        # Try recovery
        can_continue = self._attempt_recovery(error)
        
        # Exit on critical errors if requested
        if error.severity == ErrorSeverity.CRITICAL and exit_on_critical and not can_continue:
            self._exit_with_error(error)
        
        return can_continue
    
    def _wrap_exception(self, error: Exception, context: Optional[ErrorContext]) -> GeneratorError:
        """Wrap standard exceptions in GeneratorError."""
        error_type_mapping = {
            FileNotFoundError: FileOperationError,
            PermissionError: FileOperationError,
            ImportError: DependencyError,
            ValueError: ValidationError,
            KeyError: TemplateError,
        }
        
        error_class = error_type_mapping.get(type(error), GeneratorError)
        severity = ErrorSeverity.HIGH if isinstance(error, (FileNotFoundError, ImportError)) else ErrorSeverity.MEDIUM
        
        return error_class(
            message=str(error),
            context=context,
            severity=severity,
            cause=error
        )
    
    def _log_error(self, error: GeneratorError):
        """Log error with appropriate level and detail."""
        severity_mapping = {
            ErrorSeverity.LOW: logging.INFO,
            ErrorSeverity.MEDIUM: logging.WARNING,
            ErrorSeverity.HIGH: logging.ERROR,
            ErrorSeverity.CRITICAL: logging.CRITICAL
        }
        
        level = severity_mapping.get(error.severity, logging.ERROR)
        
        # Base error message
        message = f"{error.__class__.__name__}: {error}"
        
        # Add context information
        if error.context:
            context_info = [
                f"Operation: {error.context.operation}",
                f"Component: {error.context.component}"
            ]
            
            if error.context.stage:
                context_info.append(f"Stage: {error.context.stage}")
            
            if error.context.inputs:
                inputs_str = ", ".join(f"{k}={v}" for k, v in error.context.inputs.items())
                context_info.append(f"Inputs: {inputs_str}")
            
            message += f" ({', '.join(context_info)})"
        
        self.logger.log(level, message)
        
        # Log stack trace for critical errors or verbose mode
        if error.severity == ErrorSeverity.CRITICAL or self.verbose:
            if error.cause:
                self.logger.debug("Original exception:", exc_info=(type(error.cause), error.cause, error.cause.__traceback__))
            else:
                self.logger.debug("Stack trace:", exc_info=True)
    
    def _attempt_recovery(self, error: GeneratorError) -> bool:
        """Attempt to recover from the error."""
        # Get recovery strategy
        strategy = self.recovery_strategies.get(type(error))
        if not strategy:
            strategy = self.recovery_strategies.get(type(error.cause)) if error.cause else None
        
        if strategy:
            try:
                return strategy(error)
            except Exception as recovery_error:
                self.logger.error(f"Recovery strategy failed: {recovery_error}")
                return False
        
        return False
    
    def _exit_with_error(self, error: GeneratorError):
        """Exit with appropriate error code and message."""
        print(f"\n❌ Critical Error: {error}")
        
        if error.context and error.context.suggestions:
            print("💡 Suggestions:")
            for suggestion in error.context.suggestions:
                print(f"   - {suggestion}")
        
        print(f"\n📊 Session Summary:")
        print(f"   Errors: {self.error_count}")
        print(f"   Warnings: {self.warning_count}")
        
        # Exit with appropriate code
        exit_code_mapping = {
            FileOperationError: 2,
            ProjectStructureError: 3,
            TemplateError: 4,
            ValidationError: 5,
            DependencyError: 6,
            RoutingError: 7,
        }
        
        exit_code = exit_code_mapping.get(type(error), 1)
        sys.exit(exit_code)
    
    def _handle_file_not_found(self, error: GeneratorError) -> bool:
        """Handle file not found errors."""
        if error.context:
            error.context.suggestions.extend([
                "Check if the file path is correct",
                "Ensure the file exists and is accessible",
                "Run project analysis to verify structure"
            ])
        
        # Can't recover from missing critical files
        return error.severity != ErrorSeverity.CRITICAL
    
    def _handle_permission_error(self, error: GeneratorError) -> bool:
        """Handle permission errors."""
        if error.context:
            error.context.suggestions.extend([
                "Check file permissions",
                "Ensure you have write access to the directory",
                "Try running with appropriate privileges"
            ])
        return False  # Permission errors usually can't be recovered from
    
    def _handle_project_structure_error(self, error: GeneratorError) -> bool:
        """Handle project structure errors."""
        if error.context:
            error.context.suggestions.extend([
                "Run 'analyze' command to check project structure",
                "Ensure you're in the correct frontend directory",
                "Check that this is a valid React project"
            ])
        return False  # Structure errors are usually critical
    
    def _handle_template_error(self, error: GeneratorError) -> bool:
        """Handle template errors."""
        if error.context:
            error.context.suggestions.extend([
                "Check if all required templates exist",
                "Verify template syntax and variables",
                "Ensure templates directory is accessible"
            ])
        return False  # Template errors usually prevent generation
    
    def _handle_file_operation_error(self, error: GeneratorError) -> bool:
        """Handle file operation errors."""
        if error.context:
            error.context.suggestions.extend([
                "Check disk space and file permissions",
                "Ensure target directories are writable",
                "Verify file paths are valid"
            ])
        return False  # File operation errors are usually critical
    
    def _handle_routing_error(self, error: GeneratorError) -> bool:
        """Handle routing errors."""
        if error.context:
            error.context.suggestions.extend([
                "Check if parent page exists",
                "Verify parent page has routing markers",
                "Run validation to check routing sync"
            ])
        return True  # Routing errors might be recoverable
    
    def _handle_validation_error(self, error: GeneratorError) -> bool:
        """Handle validation errors."""
        if error.context:
            error.context.suggestions.extend([
                "Run comprehensive validation to see all issues",
                "Check project structure and dependencies",
                "Verify generated files exist"
            ])
        return True  # Validation errors are often informational
    
    def _handle_dependency_error(self, error: GeneratorError) -> bool:
        """Handle dependency errors."""
        if error.context:
            error.context.suggestions.extend([
                "Ensure all required hooks and components exist",
                "Run dependency creation if needed",
                "Check import paths and module structure"
            ])
        return True  # Dependency errors might be auto-recoverable


def with_error_handling(operation: str, component: str, stage: str = ""):
    """Decorator for automatic error handling."""
    def decorator(func: Callable):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Get error handler from first argument if it's a class with error_handler
            error_handler = None
            if args and hasattr(args[0], 'error_handler'):
                error_handler = args[0].error_handler
            elif args and hasattr(args[0], '_error_handler'):
                error_handler = args[0]._error_handler
            
            if not error_handler:
                error_handler = ErrorHandler()  # Fallback handler
            
            try:
                return func(*args, **kwargs)
            except Exception as e:
                context = ErrorContext(
                    operation=operation,
                    component=component,
                    stage=stage,
                    inputs={"args": str(args), "kwargs": str(kwargs)}
                )
                
                can_continue = error_handler.handle_exception(e, context, exit_on_critical=False)
                if not can_continue:
                    raise e
                
                # Return None or appropriate default for failed operations
                return None
        
        return wrapper
    return decorator


def create_error_context(operation: str, component: str, **kwargs) -> ErrorContext:
    """Helper function to create error context."""
    return ErrorContext(
        operation=operation,
        component=component,
        inputs=kwargs
    )


def safe_execute(func: Callable, error_handler: ErrorHandler, 
                context: Optional[ErrorContext] = None, 
                default_return: Any = None) -> Any:
    """Safely execute a function with error handling."""
    try:
        return func()
    except Exception as e:
        can_continue = error_handler.handle_exception(e, context, exit_on_critical=False)
        if can_continue:
            return default_return
        raise e


# Convenience functions for common error scenarios
def handle_file_operation(error_handler: ErrorHandler, operation: str, file_path: Path):
    """Handle file operation errors with appropriate context."""
    def execute_with_context(func: Callable):
        context = ErrorContext(
            operation=operation,
            component="FileWriter",
            inputs={"file_path": str(file_path)},
            suggestions=[
                f"Check if {file_path.parent} directory exists",
                "Verify write permissions",
                "Ensure sufficient disk space"
            ]
        )
        return safe_execute(func, error_handler, context)
    return execute_with_context


def handle_template_operation(error_handler: ErrorHandler, operation: str, template_name: str):
    """Handle template operation errors with appropriate context."""
    def execute_with_context(func: Callable):
        context = ErrorContext(
            operation=operation,
            component="TemplateEngine",
            inputs={"template_name": template_name},
            suggestions=[
                f"Check if {template_name} template exists",
                "Verify template syntax",
                "Ensure all variables are provided"
            ]
        )
        return safe_execute(func, error_handler, context)
    return execute_with_context