from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import Car
from .serializer import CarSerializer
from django.conf import settings
import os
import json
from datetime import datetime
from django.shortcuts import render
@api_view(['GET'])
def get_fuel_types(request):
    """Fetch all unique fuel types from the JSON file."""
    file_path = os.path.join(settings.BASE_DIR, 'Data', 'all-vehicles-model.json')
    with open(file_path, 'r') as f:
        data = json.load(f)

    # Extract unique fuel types
    fuel_types = list(set(item.get('fueltype') for item in data if item.get('fueltype')))
    
    response_data = {
        'fuel_types': fuel_types
    }
    
    return Response(response_data)

@api_view(['GET'])
def get_data(request):
    """Load data from the JSON file and return it."""
    file_path = os.path.join(settings.BASE_DIR, 'Data', 'all-vehicles-model.json')
    with open(file_path, 'r') as f:
        data = json.load(f)
    
    response_data = {
        'count': len(data),
        'records': data
    }
    
    return Response(response_data)

@api_view(['GET'])
def query_data(request):
    """Filter data based on query parameters."""
    file_path = os.path.join(settings.BASE_DIR, 'Data', 'all-vehicles-model.json')
    with open(file_path, 'r') as f:
        data = json.load(f)

    filters = {k: v for k, v in request.GET.items()}
    filtered_data = [item for item in data if all(str(item.get(k)) == str(v) for k, v in filters.items())]
    
    response_data = {
        'count': len(filtered_data),
        'records': filtered_data
    }
    
    return Response(response_data)

def get_latest_records(data):
    """Return the latest record for each model within the same make."""
    latest_records = {}
    
    for record in data:
        make = record.get('make')
        model = record.get('model')
        createdon = record.get('createdon')
        modifiedon = record.get('modifiedon')
        
        date_str = createdon if createdon else modifiedon
        date = datetime.strptime(date_str, '%Y-%m-%d') if date_str else datetime.min
        
        if make not in latest_records:
            latest_records[make] = {}
        
        if model not in latest_records[make] or date > latest_records[make][model]['date']:
            latest_records[make][model] = {
                'record': record,
                'date': date
            }
    
    result = [entry['record'] for make in latest_records.values() for entry in make.values()]
    return result

@api_view(['GET'])
def query_by_brand(request, brand):
    """Return the latest records for a given brand."""
    file_path = os.path.join(settings.BASE_DIR, 'Data', 'all-vehicles-model.json')
    with open(file_path, 'r') as f:
        data = json.load(f)
    
    filtered_data = [item for item in data if item.get('make') == brand]
    latest_data = get_latest_models_by_brand(filtered_data)
    
    
    response_data = {
        'count': len(latest_data),
        'records': latest_data
    }
    
    return Response(response_data)

def get_latest_models_by_brand(records):
    """Return only the latest records for each model based on 'createdon'."""
    if not records:
        return []

    try:
        records_sorted = sorted(records, key=lambda x: datetime.strptime(x.get('createdon', '1970-01-01'), '%Y-%m-%d'), reverse=True)
    except ValueError as e:
        print(f"Date parsing error: {e}")
        return []

    latest_records = {}
    for record in records_sorted:
        model = record.get('model')
        if model not in latest_records:
            latest_records[model] = record
    
    return list(latest_records.values())

def get_latest_record(records):
    """Return the latest record based on 'createdon' or 'modifiedon'."""
    if not records:
        return None
    
    try:
        records_sorted = sorted(records, key=lambda x: datetime.strptime(x.get('createdon', '1970-01-01'), '%Y-%m-%d'), reverse=True)
    except ValueError as e:
        print(f"Date parsing error: {e}")
        return None
    
    return records_sorted[0]

@api_view(['GET'])
def query_by_model(request, model):
    """Return the latest record for a given model."""
    file_path = os.path.join(settings.BASE_DIR, 'Data', 'all-vehicles-model.json')
    with open(file_path, 'r') as f:
        data = json.load(f)
    
    filtered_data = [item for item in data if item.get('model') == model]
    latest_record = get_latest_record(filtered_data)
    
    if latest_record:
        return Response(latest_record)
    else:
        return Response({'error': 'No records found'}, status=404)


@api_view(['GET'])
def get_brands(request):
    """Fetch all unique brands from the JSON file."""
    file_path = os.path.join(settings.BASE_DIR, 'Data', 'all-vehicles-model.json')
    with open(file_path, 'r') as f:
        data = json.load(f)

    # Extract unique brands
    brands = list(set(item.get('make') for item in data if item.get('make')))
    
    response_data = {
        'brands': brands
    }
    
    return Response(response_data)

def index(request):
    return render(request, 'index.html')