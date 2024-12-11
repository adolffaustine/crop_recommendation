import requests
from django.db import models
from sklearn.ensemble import RandomForestClassifier
import joblib
import numpy as np

class Crop(models.Model):
    Taken_at = models.DateTimeField(auto_now_add=True)
    Nitrogen = models.PositiveIntegerField(null=True)
    Phosphorus = models.PositiveIntegerField(null=True)
    Potassium = models.PositiveIntegerField(null=True)
    Temperature = models.CharField(max_length=1000, null=True)
    Humidity = models.CharField(max_length=1000, null=True)
    Soil_pH = models.CharField(max_length=1000, null=True)
    Rainfall = models.CharField(max_length=1000, null=True)
    Crop_supported = models.CharField(max_length=1000, blank=True)
    Other = models.CharField(max_length=1000, blank=True)

    def save(self, *args, **kwargs):
        # Fetch rainfall data from the Tomorrow.io API
        api_url = "https://api.tomorrow.io/v4/weather/forecast?location=42.3478,-71.0466&apikey=ClVJ8gt4NX5Dhow7AJhjZP4yUssu1gIR"
        
        try:
            response = requests.get(api_url)
            response.raise_for_status()  # Raise an error for bad status codes

            data = response.json()
            # Extract the precipitation data from the API response
            rain_intensity = data['timelines']['minutely'][0]['values']['rainIntensity']
            self.Rainfall = str(rain_intensity)  # Converting to string to match model field type
        except requests.exceptions.HTTPError as http_err:
            print(f"HTTP error occurred: {http_err}")
            self.Rainfall = 'Unknown'
        except KeyError:
            print("KeyError: 'rainIntensity' not found in API response.")
            self.Rainfall = 'Unknown'
        except Exception as err:
            print(f"Other error occurred: {err}")
            self.Rainfall = 'Unknown'

        # Ensure that all necessary fields are available and valid for prediction
        try:
            features = [
                float(self.Nitrogen) if self.Nitrogen is not None else np.nan,
                float(self.Phosphorus) if self.Phosphorus is not None else np.nan,
                float(self.Potassium) if self.Potassium is not None else np.nan,
                float(self.Temperature) if self.Temperature not in [None, ''] else np.nan,
                float(self.Humidity) if self.Humidity not in [None, ''] else np.nan,
                float(self.Soil_pH) if self.Soil_pH not in [None, ''] else np.nan,
                float(self.Rainfall) if self.Rainfall not in [None, '', 'Unknown'] else np.nan,
            ]

            if any(np.isnan(features)):
                raise ValueError("Missing or invalid feature values")

            # Load the machine learning model
            ml_model = joblib.load('./ml_model/crop_recomender.joblib')

            # Make predictions
            predictions = ml_model.predict_proba([features])

            crop_dict = {
                'rice': predictions[0][0],
                'maize': predictions[0][1],
                'peas': predictions[0][2],
                'groundnut': predictions[0][3],
                'cowpeas': predictions[0][4],
                'grapes': predictions[0][5]
            }
            crop_supported = max(crop_dict, key=crop_dict.get)
            del crop_dict[crop_supported]
            other_crops = sorted(crop_dict, key=crop_dict.get, reverse=True)[:2]
            self.Crop_supported = crop_supported
            self.Other = ", ".join(other_crops)
        except ValueError as ve:
            print(f"Error in features: {ve}")
            self.Crop_supported = 'Unknown'
            self.Other = ''
        except Exception as e:
            print(f"Error during prediction: {e}")
            self.Crop_supported = 'Unknown'
            self.Other = ''

        # Call the original save method
        return super().save(*args, **kwargs)

    class Meta:
        ordering = ['-Taken_at']

    def __str__(self):
        return self.Crop_supported
