#!/usr/bin/env python3
"""
Frontend Tools Package
Refactored frontend generator with modular components
"""

from .frontend_orchestrator import FrontendOrchestrator
from .base_generator import BaseFrontendGenerator
from .domain_mapping import DomainMapping
from .types_generator import TypesGenerator
from .services_generator import ServicesGenerator
from .hooks_generator import HooksGenerator
from .components_generator import ComponentsGenerator
from .clients_generator import ClientsGenerator
from .stores_generator import StoresGenerator

__all__ = [
    'FrontendOrchestrator',
    'BaseFrontendGenerator',
    'DomainMapping',
    'TypesGenerator',
    'ServicesGenerator',
    'HooksGenerator',
    'ComponentsGenerator',
    'ClientsGenerator',
    'StoresGenerator'
]

__version__ = '4.0.0'
__author__ = 'Frontend Tools Team'
__description__ = 'Modular frontend generator for domain-driven architecture'