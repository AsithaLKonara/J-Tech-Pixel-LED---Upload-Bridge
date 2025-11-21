# 📐 UPLOAD BRIDGE - ARCHITECTURE & DATA FLOW GUIDE

## Table of Contents
1. [System Architecture](#system-architecture)
2. [Data Flow Diagrams](#data-flow-diagrams)
3. [Component Interactions](#component-interactions)
4. [Design Patterns](#design-patterns)
5. [Extensibility Points](#extensibility-points)

---

## System Architecture

### Layered Architecture Model

```
┌──────────────────────────────────────────────────────┐
│                 PRESENTATION LAYER                   │
│  Main Window, Tabs, Widgets, Dialogs (PySide6)      │
├──────────────────────────────────────────────────────┤
│               BUSINESS LOGIC LAYER                    │
│  Pattern Processing, Firmware Building, Validation   │
├──────────────────────────────────────────────────────┤
│                DATA ACCESS LAYER                      │
│  Parsers, Pattern Model, Configuration               │
├──────────────────────────────────────────────────────┤
│              HARDWARE INTERFACE LAYER                 │
│  Device-Specific Uploaders, Build Tools              │
├──────────────────────────────────────────────────────┤
│              EXTERNAL TOOLS & SERVICES                │
│  Arduino CLI, esptool, avrdude, ARM GCC              │
└──────────────────────────────────────────────────────┘
```

### Component Dependency Graph

```
                           main.py
                             │
                      ┌──────┴──────┐
                      │             │
                 main_window.py   launch.py
                      │
          ┌───────────┼───────────┐
          │           │           │
     preview_tab   flash_tab   config loading
          │           │           │
     ┌────┴───┐   ┌───┴────┐    │
     │        │   │        │    │
pattern   simulator builder uploader chip_database.yaml
model              │        │
     │   ┌─────────┴────────┘
     │   │
  parsers uploaders
     │        │
  registry  registry
```

---

## Data Flow Diagrams

### 1. Pattern Loading Flow

```
User selects file (GUI)
        │
        ▼
File Dialog ──filename──► parser_registry.parse_pattern_file()
                               │
                    ┌──────────┼──────────┐
                    │          │          │
              Auto-detect   Try each    Score
              file format   parser      confidence
                    │          │          │
                    └──────────┼──────────┘
                               │
                    Parser detects format
                               │
              ┌────────────────┼────────────────┐
              │                │                │
        standard_format    raw_rgb_parser   intel_hex_parser
        (with header)      (pure RGB data)   (hex encoded)
              │                │                │
              └────────────────┼────────────────┘
                               │
                        Frame extraction
                               │
                    ┌──────────┴──────────┐
                    │                     │
            RGB validation         Duration calc
                    │                     │
                    └──────────┬──────────┘
                               │
                    Pattern object created
                        (with metadata)
                               │
                    Update Preview Tab
                               │
                         Show LED matrix
                         Show frame count
                         Show FPS info
```

**Key Classes Involved**:
- `ParserRegistry` - Entry point, format detection
- Various Parser subclasses - Format-specific parsing
- `Pattern` - Result data structure
- `PreviewTab` - Display result

---

### 2. Pattern Preview & Playback Flow

```
User clicks "Play" in Preview Tab
        │
        ▼
PreviewTab.play_animation()
        │
  ┌─────┴─────┐
  │ Start      │
  │ Timer      │
  │ (60 FPS)   │
  │            │
  └─────┬─────┘
        │
        ▼
Timer event every ~16ms
        │
        ▼
Get current frame index
        │
  ┌─────┴─────────┐
  │ Apply FPS      │
  │ multiplier     │
  │ (speed control)│
  └─────┬─────────┘
        │
        ▼
EnhancedLEDSimulator.render_frame(frame)
        │
  ┌─────┴─────────────────────┐
  │ For each LED in frame:    │
  │ 1. Get RGB value          │
  │ 2. Apply brightness curve │
  │ 3. Apply per-channel mult │
  │ 4. Draw pixel on canvas   │
  └─────┬─────────────────────┘
        │
        ▼
Canvas repaint (GPU accelerated)
        │
        ▼
Visible update in UI
```

**Key Classes Involved**:
- `PreviewTab` - Playback control
- `EnhancedLEDSimulator` - Rendering
- `AdvancedBrightnessController` - Brightness curves
- Qt Canvas/Graphics - Display

---

### 3. Firmware Build & Upload Flow

```
User selects chip and clicks "FLASH"
        │
        ▼
FlashTab.on_flash_clicked()
        │
  ┌─────┴─────┐
  │Validate   │
  │ Pattern   │
  │ & Chip    │
  └─────┬─────┘
        │
        ▼
FirmwareBuilder.build()
        │
  ┌─────┴─────────────────────────┐
  │ Select Uploader based on chip │
  │ (UploaderRegistry)            │
  └─────┬─────────────────────────┘
        │
  ┌─────▼──────────────┐
  │ uploader.build()   │
  └─────┬──────────────┘
        │
  ┌─────┴──────────────────────────┐
  │ 1. Generate device-specific   │
  │    firmware code              │
  │ 2. Embed pattern in PROGMEM   │
  │ 3. Compile with toolchain     │
  │ 4. Generate binary (.bin/.elf)│
  └─────┬──────────────────────────┘
        │
    SUCCESS?
        │
   ┌────┴────┐
   NO        YES
   │         │
   │    ┌────▼─────────────┐
   │    │ uploader.upload()│
   │    └────┬─────────────┘
   │         │
   │  ┌──────┴──────┐
   │  │ Detect port │
   │  │ & settings  │
   │  └──────┬──────┘
   │         │
   │  ┌──────▼────────┐
   │  │ Flash binary  │
   │  │ to device     │
   │  └──────┬────────┘
   │         │
   │  ┌──────▼────────┐
   │  │ Verify &      │
   │  │ display result│
   │  └──────┬────────┘
   │         │
   │    Show error
   └────┬────────────────┐
        │                 │
   Show log            Success
        │               message
```

**Key Classes Involved**:
- `FlashTab` - User interaction
- `FirmwareBuilder` - Orchestration
- `UploaderRegistry` - Uploader selection
- Device-specific uploaders (ESP, AVR, etc.)
- External tools (Arduino CLI, esptool, avrdude)

---

## Component Interactions

### Parser System Interaction

```
ParserRegistry (singleton)
    │
    ├── Parser 1: StandardFormatParser
    │   └── Handles LED Studio format (header + data)
    │
    ├── Parser 2: RawRGBParser
    │   └── Handles pure RGB byte streams
    │
    ├── Parser 3: IntelHexParser
    │   └── Handles Intel HEX encoding
    │
    ├── Parser 4: EnhancedBinaryParser
    │   └── Auto-detects binary format with confidence
    │
    └── Registry Methods:
        ├── parse_pattern_file() - Main entry
        ├── detect_format() - Format detection
        ├── get_parser() - Get parser by name
        └── register_parser() - Register custom parser
```

**Usage Example**:
```python
# Automatic format detection
pattern = ParserRegistry.instance().parse_pattern_file(
    'pattern.bin',
    led_count=76,
    frame_count=400
)
# Returns Pattern object with frames and metadata
```

---

### Uploader System Interaction

```
UploaderRegistry (singleton)
    │
    ├── Uploader 1: ESPUploader
    │   ├── Supports: ESP8266, ESP32, ESP32-S2, ESP32-S3, ESP32-C3
    │   ├── Build: Arduino CLI
    │   └── Upload: esptool.py
    │
    ├── Uploader 2: ESP01Uploader
    │   ├── Supports: ESP-01 (specialized)
    │   ├── Features: Memory optimization, GPIO constraints
    │   └── Upload: esptool.py
    │
    ├── Uploader 3: AVRUploader
    │   ├── Supports: ATmega328P, ATmega2560, ATtiny85
    │   ├── Build: avr-gcc
    │   └── Upload: avrdude
    │
    ├── Uploader 4: STM32Uploader
    │   ├── Supports: STM32F103C8 and variants
    │   ├── Build: arm-none-eabi-gcc
    │   └── Upload: stm32flash
    │
    ├── Uploader 5: PICUploader
    │   ├── Supports: PIC16F876A and variants
    │   ├── Build: MPLAB X IDE
    │   └── Upload: MPLAB X
    │
    ├── Uploader 6: NumicroUploader
    │   ├── Supports: Nuvoton M031, M451
    │   ├── Build: ARM GCC
    │   └── Upload: Nu-Link tools
    │
    └── Registry Methods:
        ├── get_uploader() - Get by chip name
        ├── list_supported_chips() - List all chips
        ├── get_chip_spec() - Get chip specs
        └── register_uploader() - Register custom
```

**Uploader Interface**:
```python
class BaseUploader:
    def build(pattern, config) -> BuildResult
        # Generate and compile firmware
    
    def upload(firmware_path, upload_config) -> UploadResult
        # Flash to device
    
    def verify(device_config) -> VerificationResult
        # Verify successful upload
    
    def get_specs() -> Dict
        # Return chip specifications
```

---

### Pattern Model Hierarchy

```
Pattern (root)
    ├── id: UUID
    ├── name: str
    │
    ├── metadata: PatternMetadata
    │   ├── width: int (LEDs wide)
    │   ├── height: int (LEDs tall, 1 for strip)
    │   ├── color_order: str (RGB/GRB/etc)
    │   ├── fps: float (calculated)
    │   ├── brightness: float (0.0-1.0)
    │   ├── brightness_curve: str (linear/gamma/etc)
    │   ├── per_channel_brightness: bool
    │   ├── speed_curve: str (linear/ease/etc)
    │   ├── variable_speed: bool
    │   └── speed_keyframes: list
    │
    └── frames: List[Frame]
        ├── Frame[0]
        │   ├── pixels: [(R, G, B), ...]
        │   └── duration_ms: int
        │
        ├── Frame[1]
        │   ├── pixels: [(R, G, B), ...]
        │   └── duration_ms: int
        │
        └── Frame[N]
            ├── pixels: [(R, G, B), ...]
            └── duration_ms: int
```

**Pattern Properties**:
```python
pattern.led_count          # Total LEDs
pattern.frame_count        # Total frames
pattern.duration_ms        # Total animation time
pattern.average_fps        # Calculated FPS
pattern.estimate_memory_bytes()  # Memory needed
```

---

## Design Patterns

### 1. Registry Pattern (Parser & Uploader)

**Purpose**: Decouple creation and usage of parsers/uploaders

```python
# Parser Registry
parser_registry = ParserRegistry.instance()
pattern = parser_registry.parse_pattern_file('file.bin')

# Uploader Registry
uploader_registry = UploaderRegistry.instance()
uploader = uploader_registry.get_uploader('esp8266')
result = uploader.build(pattern, config)
```

**Benefits**:
- Easy to add new parsers/uploaders
- Single entry point
- Format/chip auto-detection
- Confidence scoring

---

### 2. Builder Pattern (Firmware)

**Purpose**: Construct complex firmware objects step-by-step

```python
builder = FirmwareBuilder()
builder.set_pattern(pattern)
builder.set_chip('esp8266')
builder.set_config({'gpio_pin': 3})
result = builder.build()
# Returns: FirmwareResult with paths and metadata
```

**Benefits**:
- Clear build process
- Easy validation
- Reusable for different configurations

---

### 3. Factory Pattern (Uploader Selection)

**Purpose**: Create appropriate uploader based on chip type

```python
# Automatic uploader selection
uploader = UploaderRegistry.instance().get_uploader('esp8266')
# Returns: ESPUploader instance

# Works for any supported chip
uploader = UploaderRegistry.instance().get_uploader('atmega328p')
# Returns: AVRUploader instance
```

---

### 4. Observer Pattern (UI Updates)

**Purpose**: Keep UI synchronized with pattern/config changes

```python
# Qt Signals for loose coupling
class PreviewTab:
    pattern_changed = pyqtSignal(Pattern)
    
    def on_load_pattern(self, pattern):
        self.pattern_changed.emit(pattern)

# Listener updates
def update_preview(pattern):
    simulator.set_pattern(pattern)
    simulator.repaint()

# Connect
preview_tab.pattern_changed.connect(update_preview)
```

---

### 5. Strategy Pattern (Brightness/Speed Curves)

**Purpose**: Switch algorithms for curve calculations

```python
# Different brightness curve strategies
curves = {
    'linear': LinearCurve(),
    'gamma_corrected': GammaCurve(gamma=2.2),
    'logarithmic': LogarithmicCurve(),
    'exponential': ExponentialCurve(),
    's_curve': SCurve()
}

# Apply strategy
curve = curves[pattern.metadata.brightness_curve]
adjusted_value = curve.apply(original_value)
```

---

## Extensibility Points

### Adding a New File Format Parser

```python
# 1. Create parser class
class MyFormatParser(BaseParser):
    def can_parse(self, file_path: str, file_content: bytes) -> bool:
        # Return True if this parser can handle the file
        return file_path.endswith('.myformat')
    
    def parse(self, file_path: str, led_count: Optional[int] = None,
              frame_count: Optional[int] = None) -> Pattern:
        # Parse file and return Pattern object
        pattern = Pattern(name=Path(file_path).stem)
        # ... parsing logic ...
        return pattern

# 2. Register with registry
registry = ParserRegistry.instance()
registry.register_parser('myformat', MyFormatParser())

# 3. Now it works automatically!
pattern = ParserRegistry.instance().parse_pattern_file('file.myformat')
```

---

### Adding Support for a New Microcontroller

```python
# 1. Create uploader class
class MyChipUploader(BaseUploader):
    def build(self, pattern: Pattern, config: Dict) -> BuildResult:
        # Generate firmware for your chip
        # Compile with your toolchain
        # Return BuildResult with paths
        pass
    
    def upload(self, firmware_path: str, upload_config: Dict) -> UploadResult:
        # Flash firmware to your chip
        # Return UploadResult with status
        pass
    
    def get_specs(self) -> Dict:
        return {
            'name': 'My Chip',
            'family': 'MyFamily',
            'flash_size': 65536,
            'ram_size': 8192,
            'max_leds': 500,
            'gpio_pins': 30
        }

# 2. Add to chip database (chip_database.yaml)
mychip:
    name: "My Chip"
    family: "MyFamily"
    flash_size: "64KB"
    ram_size: "8KB"
    uploader: "mychip_uploader"
    default_gpio: 3
    max_leds: 500

# 3. Register uploader
registry = UploaderRegistry.instance()
registry.register_uploader('mychip_uploader', MyChipUploader())

# 4. Now it works!
uploader = registry.get_uploader('mychip')
result = uploader.build(pattern, config)
```

---

### Adding Custom Brightness Curve

```python
# 1. Create curve class
class CustomCurve:
    def apply(self, value: float) -> float:
        # Apply custom transformation
        return value ** 1.5  # Example: square root-like curve
    
    def get_name(self) -> str:
        return 'custom'

# 2. Use in brightness controller
brightness_controller.add_curve('custom', CustomCurve())

# 3. Apply to pattern
pattern.metadata.brightness_curve = 'custom'
```

---

## Data Structures

### Pattern Binary Format

```
Raw RGB Format (used in p1.bin):
┌─────────────────────┐
│ Frame 0 - LED 0     │ [R, G, B]
│ Frame 0 - LED 1     │ [R, G, B]
│ ...                 │
│ Frame 0 - LED 75    │ [R, G, B]
│ Frame 1 - LED 0     │ [R, G, B]
│ ...                 │
│ Frame 399 - LED 75  │ [R, G, B]
└─────────────────────┘
Total: 76 LEDs × 400 frames × 3 bytes = 91,200 bytes

Standard Format:
┌─────────────────────┐
│ LED Count (2B)      │ 0x004C (76)
│ Frame Count (2B)    │ 0x0190 (400)
│ Config Bytes        │ (varies)
│ ... Pattern Data ... │ RGB bytes
└─────────────────────┘
```

---

## Configuration Files

### chip_database.yaml Structure

```yaml
chips:
  esp8266:
    name: "ESP8266"
    family: "ESP"
    flash_size: "4MB"
    ram_size: "80KB"
    uploader: "esp_uploader"
    requirements: ["python -m esptool", "arduino-cli"]
    bootloader_instructions: "..."
    default_gpio: 2
    max_leds: 1000
```

---

## Summary

The Upload Bridge architecture provides:

✅ **Modular Design**: Clear separation of concerns  
✅ **Extensibility**: Easy to add formats, chips, curves  
✅ **Maintainability**: Well-documented patterns and structure  
✅ **Performance**: Efficient data handling and caching  
✅ **Reliability**: Comprehensive error handling  
✅ **Flexibility**: Multiple access points (GUI, CLI, API)

This architecture scales from simple single-format parsers to complex multi-chip firmware generation!
