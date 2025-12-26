#!/usr/bin/env python3
"""
Test script to verify numeric username functionality
"""

import requests
import json

def test_numeric_username():
    """Test the API with a numeric username"""
    
    # Test the problematic username
    test_username = "5439300655350779"
    api_url = "https://clx8580ut5.execute-api.us-east-1.amazonaws.com/Prod/quote/"
    
    print(f"🧪 Testing API with numeric username: {test_username}")
    print("=" * 50)
    
    try:
        # Make API request
        response = requests.get(f"{api_url}?name={test_username}", timeout=30)
        
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Success!")
            print(f"Quote: {data.get('quote', 'N/A')}")
            print(f"Personalized: {data.get('personalized', False)}")
            print(f"Model: {data.get('model', 'N/A')}")
            
            # Verify the quote contains the username
            if test_username in data.get('quote', ''):
                print(f"✅ Username '{test_username}' found in quote")
            else:
                print(f"⚠️  Username '{test_username}' not found in quote")
                
        else:
            print(f"❌ API Error: {response.status_code}")
            print(f"Response: {response.text}")
            
    except Exception as e:
        print(f"❌ Request failed: {str(e)}")

if __name__ == "__main__":
    test_numeric_username()