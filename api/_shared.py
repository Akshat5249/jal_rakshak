"""
Shared utilities for Vercel serverless functions.
This module handles data loading with caching for serverless environments.
"""

import pandas as pd
import joblib
import os
from math import radians, sin, cos, sqrt, atan2
import numpy as np
from datetime import datetime, timedelta

# Cache for loaded data (persists within a single function execution)
_data_cache = {}
_model_cache = {}

NORTHEAST_STATES = [
    "Arunachal Pradesh", "Assam", "Manipur", "Meghalaya", 
    "Mizoram", "Nagaland", "Sikkim", "Tripura"
]

def convert_nan_to_none(obj):
    """Helper function to convert NaN to None for JSON serialization"""
    if isinstance(obj, dict):
        return {k: convert_nan_to_none(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [convert_nan_to_none(elem) for elem in obj]
    elif pd.isna(obj) or obj == float('inf') or obj == float('-inf'):
        return None
    return obj

def haversine_distance(lat1, lon1, lat2, lon2):
    """Calculate distance between two coordinates in kilometers"""
    R = 6371  # Radius of Earth in kilometers
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    return R * c

def load_data():
    """Load and preprocess data with caching"""
    if 'data' in _data_cache:
        return _data_cache['data']
    
    try:
        # Path to Excel file (adjust based on your deployment structure)
        excel_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'final_nhs-wq_pre_2023_compressed.xlsx')
        
        # If not found, try alternative paths
        if not os.path.exists(excel_path):
            excel_path = os.path.join(os.path.dirname(__file__), '..', '..', 'final_nhs-wq_pre_2023_compressed.xlsx')
        
        df = pd.read_excel(excel_path)
        
        cols_to_fix = ["NO3", "As (ppb)", "Fe (ppm)", "Total Hardness", "pH", "EC (µS/cm at"]
        all_numeric_cols = cols_to_fix + ['Latitude', 'Longitude']

        if 'Latitude' in df.columns:
            df['Latitude'] = df['Latitude'].astype(str).str.replace(r'[^0-9.-]', '', regex=True)
        if 'Longitude' in df.columns:
            df['Longitude'] = df['Longitude'].astype(str).str.replace(r'[^0-9.-]', '', regex=True)

        for col in all_numeric_cols:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors="coerce")
        
        df[all_numeric_cols] = df[all_numeric_cols].fillna(df[all_numeric_cols].median())
        df['Location'] = df['Location'].fillna('Unknown Location').astype(str)
        df = df[df['State'].isin(NORTHEAST_STATES)]

        def water_quality_label(row):
            if (
                row["NO3"] > 45 or
                row["As (ppb)"] > 10 or
                row["Fe (ppm)"] > 0.3 or
                row["Total Hardness"] > 300 or
                row["pH"] < 6.5 or row["pH"] > 8.5 or
                row["EC (µS/cm at"] > 1500
            ):
                return 1
            return 0

        df["WaterQuality_Label"] = df.apply(water_quality_label, axis=1)

        def disease_risk_mapping(row):
            risks = []
            if row["NO3"] > 45:
                risks.append("Blue Baby Syndrome (Methemoglobinemia)")
            if row["As (ppb)"] > 10:
                risks.append("Arsenic Poisoning (Skin, Cancer risk)")
            if row["Fe (ppm)"] > 0.3:
                risks.append("Stomach Issues / Teeth Staining")
            if row["Total Hardness"] > 300:
                risks.append("Hair Fall, Kidney Stones")
            if row["pH"] < 6.5 or row["pH"] > 8.5:
                risks.append("Diarrhea, Stomach Irritation")
            if row["EC (µS/cm at"] > 1500:
                risks.append("Hypertension Risk (High Salinity)")
            return ", ".join(risks) if risks else "Safe"

        df["Possible_Diseases"] = df.apply(disease_risk_mapping, axis=1)
        
        _data_cache['data'] = df
        return df
    except Exception as e:
        print(f"Error loading data: {e}")
        return pd.DataFrame()

def load_model():
    """Load ML model with caching"""
    if 'model' in _model_cache:
        return _model_cache['model'], _model_cache['features']
    
    try:
        model_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'model.joblib')
        if not os.path.exists(model_path):
            model_path = os.path.join(os.path.dirname(__file__), '..', 'backend', 'model.joblib')
        
        if os.path.exists(model_path):
            model = joblib.load(model_path)
            # Get features from the loaded data
            df = load_data()
            if not df.empty:
                numeric_cols = df.select_dtypes(include=['float64', 'int64']).columns.tolist()
                if 'WaterQuality_Label' in numeric_cols:
                    numeric_cols.remove('WaterQuality_Label')
                features = numeric_cols
            else:
                features = []
            
            _model_cache['model'] = model
            _model_cache['features'] = features
            return model, features
    except Exception as e:
        print(f"Error loading model: {e}")
    
    return None, []
