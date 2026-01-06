# src/__init__.py
# This file marks the src directory as a Python package.
# Optional: Import specific modules for easier access
from .data import data_loader, external_data
from .models import  prophet_model
from .utils import pdf_generator
from .visualization import dashboard, map_view, predictions, feedback