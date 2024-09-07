import numpy as np
from PIL import Image
import json
import base64
import io

def image_from_base64(base64_str):
    image_data = base64.b64decode(base64_str)
    image = Image.open(io.BytesIO(image_data))
    return np.array(image)

def custom_filter(image_array, filter_size, filter_func):
    padded_image = np.pad(image_array, pad_width=filter_size//2, mode='reflect')
    filtered_image = np.zeros_like(image_array)
    
    for i in range(image_array.shape[0]):
        for j in range(image_array.shape[1]):
            region = padded_image[i:i+filter_size, j:j+filter_size]
            filtered_image[i, j] = filter_func(region)
    
    return filtered_image

def lambda_handler(event, context):
    print("Received event: " + json.dumps(event, indent=2))
    
    try:
        image_array = image_from_base64(event['image_data'])
        
        # Example filter function: mean filter
        def mean_filter(region):
            return np.mean(region)
        
        filter_size = 3  # Example filter size
        filtered_image = custom_filter(image_array, filter_size, mean_filter)
        
        # Calculate surface texture parameters
        Sa = np.mean(np.abs(filtered_image))
        Sq = np.sqrt(np.mean(filtered_image**2))
        Sz = np.max(filtered_image) - np.min(filtered_image)
        Ssk = np.mean((filtered_image - Sa)**3) / (Sq**3)
        Sku = np.mean((filtered_image - Sa)**4) / (Sq**4)
        Sp = np.max(filtered_image)
        Sv = np.min(filtered_image)
        Sal = np.mean(np.abs(np.diff(filtered_image, axis=0))) + np.mean(np.abs(np.diff(filtered_image, axis=1)))
        
        response = {
            'statusCode': 200,
            'body': json.dumps({
                'processor': 'custom_filter',
                'image_format': 'numpy_array',
                'dimensions': image_array.shape,
                'Sa': Sa,
                'Sq': Sq,
                'Sz': Sz,
                'Ssk': Ssk,
                'Sku': Sku,
                'Sp': Sp,
                'Sv': Sv,
                'Sal': Sal
            })
        }
        
        return response
    
    except Exception as e:
        print(e)
        return {
            'statusCode': 500,
            'body': json.dumps('Error processing image')
        }