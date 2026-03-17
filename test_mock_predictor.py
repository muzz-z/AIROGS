#!/usr/bin/env python
"""
Test script to verify the improved mock predictor gives varied results
for different fundus images.
"""

import os
import sys

# Add project to path
sys.path.insert(0, os.path.dirname(__file__))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'glaucoma_project.settings')

import django
django.setup()

from glaucoma_detection.utils import mock_predict
import glob

def test_mock_predictor():
    """Test mock predictor on available images"""
    
    print("=" * 70)
    print("TESTING IMPROVED MOCK PREDICTOR")
    print("=" * 70)
    print()
    
    # Find test images
    test_image_paths = glob.glob('media/fundus/*.jpg') + glob.glob('media/fundus/*.png')
    
    if not test_image_paths:
        print("No test images found in media/fundus/")
        print("\nTesting with dummy values to verify logic...")
        
        # Simulate predictions for different scenarios
        test_cases = [
            ("Normal_eye_1", 0.3),
            ("Normal_eye_2", 0.35),
            ("Glaucoma_eye_1", 0.65),
            ("Glaucoma_eye_2", 0.72),
        ]
        
        print("\nExpected behavior:")
        for name, prob in test_cases:
            pred = "Glaucoma" if prob >= 0.5 else "Normal"
            conf = round(prob * 100, 2) if pred == "Glaucoma" else round((1-prob) * 100, 2)
            print(f"  {name:20} -> Prob: {prob:.2f} -> {pred:10} (Conf: {conf}%)")
        
        return
    
    print(f"Found {len(test_image_paths)} test images\n")
    print(f"{'Image Name':40} | {'Probability':12} | {'Prediction':12} | {'Confidence':12}")
    print("-" * 90)
    
    results = []
    for image_path in test_image_paths[:10]:  # Test first 10 images
        try:
            prob = mock_predict(image_path)
            prediction = "Glaucoma" if prob >= 0.5 else "Normal"
            confidence = round(prob * 100, 2) if prediction == "Glaucoma" else round((1-prob) * 100, 2)
            
            filename = os.path.basename(image_path)
            print(f"{filename:40} | {prob:12.4f} | {prediction:12} | {confidence:12}%")
            
            results.append({
                'file': filename,
                'prob': prob,
                'prediction': prediction,
                'confidence': confidence
            })
        except Exception as e:
            print(f"{os.path.basename(image_path):40} | Error: {str(e)}")
    
    print()
    print("=" * 70)
    print("SUMMARY")
    print("=" * 70)
    
    if results:
        glaucoma_count = sum(1 for r in results if r['prediction'] == 'Glaucoma')
        normal_count = sum(1 for r in results if r['prediction'] == 'Normal')
        
        print(f"Total images processed: {len(results)}")
        print(f"Glaucoma predictions: {glaucoma_count}")
        print(f"Normal predictions: {normal_count}")
        print()
        
        # Check if we get varied results
        probs = [r['prob'] for r in results]
        if len(set([round(p, 2) for p in probs])) > 1:
            print("✅ Mock predictor is giving VARIED results (GOOD!)")
        else:
            print("⚠️  Mock predictor is giving SIMILAR results")
        
        print()
        print("Expected behavior:")
        print("- Different images should get different probabilities")
        print("- Images with large optic cups → Higher glaucoma probability")
        print("- Images with small optic cups → Higher normal probability")
        print("- Glaucomatous features should push probability towards 0.8+")
        print("- Normal features should push probability towards 0.1-0.3")
    else:
        print("No images were successfully processed")

if __name__ == '__main__':
    test_mock_predictor()
