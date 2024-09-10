import numpy as np
from scipy.ndimage import generic_filter
from PIL import Image
import io
import base64

def arithmetical_mean_height(surface):
    """Calculate the arithmetical mean height (Sa)."""
    Sa = np.mean(np.abs(surface))
    return Sa

def root_mean_square_height(surface):
    """Calculate the root mean square height (Sq)."""
    Sq = np.sqrt(np.mean(surface**2))
    return Sq

def maximum_height(surface):
    """Calculate the maximum height (Sz)."""
    Sz = np.max(surface) - np.min(surface)
    return Sz

def skewness(surface):
    """Calculate the skewness (Ssk)."""
    Sa = arithmetical_mean_height(surface)
    Sq = root_mean_square_height(surface)
    Ssk = np.mean((surface - Sa)**3) / (Sq**3)
    return Ssk

def kurtosis(surface):
    """Calculate the kurtosis (Sku)."""
    Sq = root_mean_square_height(surface)
    Sku = np.mean(surface**4) / (Sq**4)
    return Sku

def maximum_peak_height(surface):
    """Calculate the maximum peak height (Sp)."""
    Sp = np.max(surface)
    return Sp

def maximum_pit_height(surface):
    """Calculate the maximum pit height (Sv)."""
    Sv = np.min(surface)
    return Sv

def auto_correlation_length(surface):
    """Calculate the auto-correlation length (Sal)."""
    def correlation_function(window):
        # Calculate mean and standard deviation for the window
        mean_x = np.mean(window)
        std_x = np.std(window)

        # Calculate auto-correlation (normalized covariance)
        auto_corr = np.mean((window - mean_x) * (window - mean_x)) / (std_x * std_x)
        return auto_corr

    def calculate_sal(surface):
        # Apply the generic filter with the correlation function
        return generic_filter(surface, correlation_function, size=3)

    Sal = calculate_sal(surface)
    return np.mean(Sal)

def lambda_handler(event, context):
    # Assume the image is passed as a base64-encoded string in the event
    base64_image = event['body']

    # Decode the base64 string to bytes
    image_data = base64.b64decode(base64_image)
    image = Image.open(io.BytesIO(image_data))

    # Convert the image to grayscale (if not already) and to a NumPy array
    surface = np.array(image.convert('L'))

    # Calculate surface texture parameters
    Sa = arithmetical_mean_height(surface).item()  # Convert to Python float
    Sq = root_mean_square_height(surface).item()
    Sz = maximum_height(surface).item()
    Ssk = skewness(surface).item()
    Sku = kurtosis(surface).item()
    Sp = maximum_peak_height(surface).item()
    Sv = maximum_pit_height(surface).item()
    Sal = auto_correlation_length(surface).item()

    # Return results
    return {
        "statusCode": 200,
        "body": {
            "Arithmetical Mean Height (Sa)": Sa,
            "Root Mean Square Height (Sq)": Sq,
            "Maximum Height (Sz)": Sz,
            "Skewness (Ssk)": Ssk,
            "Kurtosis (Sku)": Sku,
            "Maximum Peak Height (Sp)": Sp,
            "Maximum Pit Height (Sv)": Sv,
            "Auto-Correlation Length (Sal)": Sal
        }
    }