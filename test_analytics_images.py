#!/usr/bin/env python3
"""
Test script to check analytics image serving
"""

import requests
import os

def test_analytics_images():
    """Test if analytics images are being served correctly"""
    base_url = "http://127.0.0.1:5000"
    
    # Test images
    images = [
        'comprehensive_data_analysis.png',
        'user_behavior_analysis.png'
    ]
    
    print("🔍 Testing analytics image serving...")
    
    for image_name in images:
        url = f"{base_url}/analytics_image/{image_name}"
        print(f"\n📸 Testing: {url}")
        
        try:
            response = requests.get(url, timeout=10)
            print(f"   Status Code: {response.status_code}")
            print(f"   Content Type: {response.headers.get('content-type', 'N/A')}")
            print(f"   Content Length: {len(response.content)} bytes")
            
            if response.status_code == 200:
                print(f"   ✅ {image_name} served successfully!")
            else:
                print(f"   ❌ {image_name} failed to serve")
                print(f"   Response: {response.text[:200]}...")
                
        except Exception as e:
            print(f"   ❌ Error: {e}")
    
    # Test analytics page
    print(f"\n🌐 Testing analytics page...")
    try:
        url = f"{base_url}/data_analytics"
        response = requests.get(url, timeout=30)
        print(f"   Status Code: {response.status_code}")
        
        if response.status_code == 200:
            print(f"   ✅ Analytics page loaded successfully!")
        else:
            print(f"   ❌ Analytics page failed to load")
            print(f"   Response: {response.text[:200]}...")
            
    except Exception as e:
        print(f"   ❌ Error: {e}")

if __name__ == "__main__":
    test_analytics_images()