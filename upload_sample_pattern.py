#!/usr/bin/env python3
"""
Upload Sample Pattern - Load and upload the last pattern from SamplePatterns folder
"""

import sys
import os
from pathlib import Path

# Add project root to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__)))

from core.pattern import Pattern
from parsers.parser_registry import ParserRegistry
from firmware.builder import FirmwareBuilder

def load_sample_pattern():
    """Load the last pattern from SamplePatterns folder"""
    sample_patterns_dir = Path("C:/Users/asith/Documents/LEDMatrixStudioSource/SamplePatterns")
    
    # Find all .leds files
    leds_files = list(sample_patterns_dir.glob("*.leds"))
    
    if not leds_files:
        print("❌ No .leds files found in SamplePatterns folder")
        return None
    
    # Get the last file (alphabetically)
    last_file = sorted(leds_files)[-1]
    print(f"📁 Loading pattern: {last_file.name}")
    print(f"   Size: {last_file.stat().st_size:,} bytes")
    
    try:
        # Use parser registry to load the pattern
        registry = ParserRegistry()
        is_valid, message, info = registry.validate_file(str(last_file))
        
        if not is_valid:
            print(f"❌ Invalid pattern file: {message}")
            return None
        
        print(f"✅ Pattern validation successful")
        print(f"   LEDs: {info.get('leds', 'Unknown')}")
        print(f"   Frames: {info.get('frames', 'Unknown')}")
        
        # Load the pattern
        pattern = registry.parse_file(str(last_file))
        if pattern:
            print(f"✅ Pattern loaded successfully: {pattern.name}")
            print(f"   LEDs: {pattern.led_count}")
            print(f"   Frames: {pattern.frame_count}")
            print(f"   FPS: {pattern.metadata.fps}")
            return pattern
        else:
            print("❌ Failed to parse pattern file")
            return None
            
    except Exception as e:
        print(f"❌ Error loading pattern: {e}")
        return None

def upload_pattern_to_esp8266(pattern):
    """Upload pattern to ESP8266"""
    print(f"\n🚀 Uploading pattern to ESP8266...")
    
    # Create firmware builder
    builder = FirmwareBuilder()
    
    # Build firmware for ESP8266
    print("📱 Building firmware...")
    result = builder.build_universal_firmware(
        pattern, 
        "esp8266", 
        {"gpio_pin": 2}
    )
    
    if result.success:
        print(f"✅ Firmware built successfully")
        print(f"   File: {result.firmware_path}")
        print(f"   Size: {result.size_bytes:,} bytes")
        
        # Check if esptool is available
        try:
            import subprocess
            result = subprocess.run(["esptool.py", "--version"], 
                                 capture_output=True, text=True, timeout=10)
            if result.returncode == 0:
                print("✅ esptool.py is available")
                print("\n📋 Upload Instructions:")
                print("1. Connect your ESP8266 to COM4 (or your port)")
                print("2. Hold GPIO0 LOW, press RESET, release GPIO0")
                print("3. Use the Upload Bridge app to flash the firmware")
                print(f"4. Firmware file: {result.firmware_path}")
            else:
                print("⚠️ esptool.py not found - install with: pip install esptool")
        except Exception as e:
            print(f"⚠️ Could not check esptool: {e}")
            
    else:
        print(f"❌ Firmware build failed: {result.error_message}")
        return False
    
    return True

def main():
    """Main function"""
    print("🎨 Upload Bridge - Sample Pattern Uploader")
    print("=" * 50)
    
    # Load the sample pattern
    pattern = load_sample_pattern()
    if not pattern:
        return False
    
    # Upload to ESP8266
    success = upload_pattern_to_esp8266(pattern)
    
    if success:
        print(f"\n🎉 Pattern ready for upload!")
        print(f"   Pattern: {pattern.name}")
        print(f"   LEDs: {pattern.led_count}")
        print(f"   Frames: {pattern.frame_count}")
        print(f"\n💡 Use the Upload Bridge app to flash to your ESP8266!")
    else:
        print(f"\n❌ Upload preparation failed")
    
    return success

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)













