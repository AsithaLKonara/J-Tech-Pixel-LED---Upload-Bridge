#!/usr/bin/env python3
"""
Test ESP8266 build process directly
"""

import sys
from pathlib import Path
from core.pattern import create_test_pattern
from uploaders.esp_uploader import EspUploader

def test_esp_build():
    """Test ESP8266 firmware build"""
    print("🧪 Testing ESP8266 Build Process")
    print("=" * 40)
    
    # Create test pattern
    pattern = create_test_pattern(led_count=8, frame_count=5)
    print(f"✅ Created test pattern: {pattern.led_count} LEDs, {pattern.frame_count} frames")
    
    # Create ESP uploader
    uploader = EspUploader("esp8266")
    
    # Test build
    try:
        result = uploader.build_firmware(
            pattern=pattern,
            build_opts={
                "gpio_pin": 3, 
                "output_dir": "build/test_esp8266",
                "template_path": "firmware/templates/esp8266"
            }
        )
        
        print(f"✅ Build result: {result}")
        
        # Check if binary exists and has content
        binary_path = Path("build/test_esp8266/test_esp8266.ino.bin")
        if binary_path.exists():
            size = binary_path.stat().st_size
            print(f"✅ Binary file size: {size} bytes")
            if size > 0:
                print("🎯 Build successful!")
            else:
                print("❌ Binary file is empty!")
        else:
            print("❌ Binary file not found!")
            
    except Exception as e:
        print(f"❌ Build failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_esp_build()
