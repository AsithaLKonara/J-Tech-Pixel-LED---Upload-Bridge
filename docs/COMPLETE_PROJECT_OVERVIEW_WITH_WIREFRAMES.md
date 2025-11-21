# 📘 Upload Bridge - Complete 100% Overview Documentation
## Project Overview, Features, Tabs, and Wireframe Documentation

**Document Version**: 3.0  
**Last Updated**: 2025-01-XX  
**Status**: Production Ready  

---

## 📑 Table of Contents

1. [Executive Summary](#executive-summary)
2. [Project Architecture](#project-architecture)
3. [Complete Tab Documentation](#complete-tab-documentation)
4. [Wireframe Documentation](#wireframe-documentation)
5. [Feature Catalog](#feature-catalog)
6. [User Flows](#user-flows)
7. [Technical Specifications](#technical-specifications)

---

## 📋 Executive Summary

**Upload Bridge** is a professional-grade, cross-platform desktop application for creating, editing, previewing, and uploading LED animation patterns to microcontroller boards. It serves as a complete LED matrix design and deployment solution.

### Key Statistics
- **Total Tabs**: 9 main tabs
- **Supported Chips**: 14+ microcontroller types
- **File Formats**: 10+ import/export formats
- **Lines of Code**: 9,050+ production code
- **Test Coverage**: 54 E2E tests (all passing)

### Core Purpose
Upload Bridge solves the challenge of managing LED pattern workflows across diverse hardware platforms by providing:
1. **Universal Pattern Creation** - Interactive design tools with multi-layer support
2. **Multi-Format Support** - Import from 10+ formats, export to all major formats
3. **Real-time Preview** - 60 FPS LED matrix visualization
4. **Hardware Deployment** - USB flashing, WiFi upload, batch operations
5. **Professional Workflow** - Pattern library, automation, effects, scratchpads

---

## 🏗️ Project Architecture

### High-Level System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    Upload Bridge Application                     │
│                      (PySide6 Qt GUI Layer)                      │
├─────────────────────────────────────────────────────────────────┤
│                                                                   │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │          Main Window (QMainWindow)                       │   │
│  │  ┌───────────────────────────────────────────────────┐  │   │
│  │  │  Menu Bar: File | Edit | Tools | View | Help     │  │   │
│  │  └───────────────────────────────────────────────────┘  │   │
│  │  ┌───────────────────────────────────────────────────┐  │   │
│  │  │  Toolbar: Open | Save | Preview | Flash           │  │   │
│  │  └───────────────────────────────────────────────────┘  │   │
│  │  ┌───────────────────────────────────────────────────┐  │   │
│  │  │  Tab Widget (9 Tabs)                               │  │   │
│  │  │  ├─ 🎬 Media Upload                                │  │   │
│  │  │  ├─ 🎨 Design Tools                                │  │   │
│  │  │  ├─ 👁️ Preview                                     │  │   │
│  │  │  ├─ ⚡ Flash                                        │  │   │
│  │  │  ├─ 🚀 Batch Flash                                  │  │   │
│  │  │  ├─ 📚 Pattern Library                              │  │   │
│  │  │  ├─ 🎵 Audio Reactive                               │  │   │
│  │  │  ├─ 📡 WiFi Upload                                  │  │   │
│  │  │  └─ 🔧 Arduino IDE                                  │  │   │
│  │  └───────────────────────────────────────────────────┘  │   │
│  │  ┌───────────────────────────────────────────────────┐  │   │
│  │  │  Status Bar: Ready | Memory | Port Status         │  │   │
│  │  └───────────────────────────────────────────────────┘  │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                   │
├─────────────────────────────────────────────────────────────────┤
│                         Domain Layer                             │
│  ┌──────────────────┐  ┌──────────────────┐  ┌──────────────┐  │
│  │  PatternState    │  │  FrameManager    │  │ LayerManager │  │
│  └──────────────────┘  └──────────────────┘  └──────────────┘  │
│  ┌──────────────────┐  ┌──────────────────┐  ┌──────────────┐  │
│  │ AutomationQueue  │  │  ScratchpadMgr   │  │ HistoryMgr   │  │
│  └──────────────────┘  └──────────────────┘  └──────────────┘  │
├─────────────────────────────────────────────────────────────────┤
│                          Core Layer                              │
│  ┌──────────────────┐  ┌──────────────────┐  ┌──────────────┐  │
│  │ Pattern Model    │  │ Parser System    │  │ Image Import │  │
│  └──────────────────┘  └──────────────────┘  └──────────────┘  │
│  ┌──────────────────┐  ┌──────────────────┐  ┌──────────────┐  │
│  │ Pattern Export   │  │ Effect Library   │  │ Font Repo    │  │
│  └──────────────────┘  └──────────────────┘  └──────────────┘  │
├─────────────────────────────────────────────────────────────────┤
│                       Hardware Layer                             │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────────┐   │
│  │ ESP8266  │  │ ESP32    │  │ AVR      │  │ STM32/PIC    │   │
│  │ Uploader │  │ Uploader │  │ Uploader │  │ Uploader     │   │
│  └──────────┘  └──────────┘  └──────────┘  └──────────────┘   │
└─────────────────────────────────────────────────────────────────┘
```

### Data Flow Pattern

```
User Action → UI Event Handler → Domain Manager → PatternState
                ↓                                        ↓
           UI Update ← Signal Emission ← Pattern Update
```

---

## 🎨 Complete Tab Documentation

### Tab 1: 🎬 Media Upload Tab

**Purpose**: Convert images, GIFs, and videos into LED patterns

#### Features
- **Image Import**: PNG, JPG, BMP (single image or sequence)
- **GIF Import**: Animated GIF to frame sequence conversion
- **Video Import**: MP4, AVI, MOV frame extraction
- **Auto Dimension Detection**: Automatically detects matrix dimensions
- **Frame Extraction**: Configurable FPS for video/GIF
- **Color Reduction**: RGB to pattern color mapping
- **Preview**: Preview converted pattern before loading

#### Wireframe Layout

```
┌────────────────────────────────────────────────────────────┐
│ 🎬 Media Upload                                         [X]│
├────────────────────────────────────────────────────────────┤
│                                                              │
│  ┌────────────────────────────────────────────────────┐   │
│  │  Select Media File                                  │   │
│  │  ┌──────────────────────────────────────────────┐  │   │
│  │  │ [📁 Browse Files...]              [📁 Folder]│  │   │
│  │  └──────────────────────────────────────────────┘  │   │
│  │  Supported: PNG, JPG, GIF, MP4, AVI, MOV           │   │
│  └────────────────────────────────────────────────────┘   │
│                                                              │
│  ┌────────────────────────────────────────────────────┐   │
│  │  Conversion Settings                                │   │
│  │  ┌────────────────────────────────────────────────┐│   │
│  │  │ Matrix Size: [Width: 16 ▼] [Height: 16 ▼]     ││   │
│  │  │ Auto-detect: [✓] Enable                        ││   │
│  │  └────────────────────────────────────────────────┘│   │
│  │  ┌────────────────────────────────────────────────┐│   │
│  │  │ FPS: [24 ▼]   Duration: [100ms ▼]              ││   │
│  │  │ Color Mode: [RGB ▼]                            ││   │
│  │  └────────────────────────────────────────────────┘│   │
│  └────────────────────────────────────────────────────┘   │
│                                                              │
│  ┌────────────────────────────────────────────────────┐   │
│  │  Preview                                            │   │
│  │  ┌────────────────────────────────────────────────┐│   │
│  │  │                                                  ││   │
│  │  │          [LED Matrix Preview]                   ││   │
│  │  │                                                  ││   │
│  │  └────────────────────────────────────────────────┘│   │
│  │  Frame: 1/10   Duration: 100ms                     │   │
│  └────────────────────────────────────────────────────┘   │
│                                                              │
│  ┌────────────────────────────────────────────────────┐   │
│  │  Actions                                            │   │
│  │  [Cancel]                    [Convert & Load]       │   │
│  └────────────────────────────────────────────────────┘   │
│                                                              │
└────────────────────────────────────────────────────────────┘
```

#### Key Methods
- `load_media_file(file_path)`: Load and convert media
- `detect_dimensions(image)`: Auto-detect matrix size
- `convert_to_pattern(settings)`: Convert media to pattern
- `preview_pattern(pattern)`: Show preview before loading

---

### Tab 2: 🎨 Design Tools Tab

**Purpose**: Comprehensive LED matrix design studio for pattern authoring

#### Features (21 Core Features)

**Canvas & Drawing**:
- Interactive pixel-by-pixel painting canvas
- 6 drawing tools: Pixel, Rectangle, Circle, Line, Random Spray, Gradient Brush
- Zoom controls (50-300%)
- Grid overlay toggle
- Color picker with 16-color palette
- Custom color selection

**Frame Management**:
- Add, duplicate, delete frames
- Frame reordering (drag & drop)
- Frame duration control (50-5000ms)
- Frame selection and navigation
- Timeline visualization

**Layer Management**:
- Multi-layer support per frame
- Layer visibility toggle
- Layer opacity control (0-100%)
- Layer reordering
- Layer composition (blending)

**Automation**:
- Automation action queue
- Actions: Scroll, Rotate, Mirror, Flip, Invert, Wipe, Reveal, Bounce
- Action parameter configuration
- Preview automation before applying
- Apply actions to frame sequence

**Effects Library**:
- Visual effects library
- Effect categories
- Effect preview
- Apply effects to frames
- Custom effect parameters

**Scratchpads**:
- 8 temporary storage slots
- Copy pixels to scratchpad
- Paste from scratchpad
- Clear scratchpad slot

**Pattern Operations**:
- New pattern creation
- Open pattern files (DAT, BIN, HEX, LEDS, JSON)
- Save pattern files
- Export to multiple formats
- Import images/GIFs

**LMS Automation**:
- LED Matrix Studio compatibility
- LMS instruction sequence
- Preview LMS sequences
- Export to LMS format

#### Wireframe Layout

```
┌────────────────────────────────────────────────────────────────────────┐
│ 🎨 Design Tools                                                     [X]│
├────────────────────────────────────────────────────────────────────────┤
│ [New] [Open] [Save]  Matrix: 16×16  Frame: 1/5  Layer: 1  FPS: [24▼] │
├────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│  ┌─────────────────────────┐  ┌──────────────────────────────────────┐ │
│  │                         │  │  Toolbox Tabs                        │ │
│  │                         │  │  ┌────────────────────────────────┐  │ │
│  │                         │  │  │[Brushes][Scratch][Layers]      │  │ │
│  │                         │  │  │[Effects][Automation][Export]   │  │ │
│  │                         │  │  └────────────────────────────────┘  │ │
│  │                         │  │                                       │ │
│  │                         │  │  ┌────────────────────────────────┐  │ │
│  │                         │  │  │ Drawing Tools                  │  │ │
│  │                         │  │  │ [●] Pixel [▭] Rectangle        │  │ │
│  │                         │  │  │ [○] Circle [─] Line            │  │ │
│  │       CANVAS            │  │  │ [✨] Random [🌈] Gradient      │  │ │
│  │                         │  │  └────────────────────────────────┘  │ │
│  │   [LED Matrix           │  │                                       │ │
│  │   16×16 Grid]           │  │  ┌────────────────────────────────┐  │ │
│  │                         │  │  │ Color Palette                  │  │ │
│  │                         │  │  │ [■][■][■][■]                   │  │ │
│  │                         │  │  │ [■][■][■][■]                   │  │ │
│  │                         │  │  │ [🎨 Custom Color]               │  │ │
│  │                         │  │  └────────────────────────────────┘  │ │
│  │                         │  │                                       │ │
│  │                         │  │  ┌────────────────────────────────┐  │ │
│  │                         │  │  │ Frame Operations               │  │ │
│  │                         │  │  │ [+ Add] [📋 Duplicate] [🗑 Del] │  │ │
│  │                         │  │  │ Duration: [100ms ▼]            │  │ │
│  │                         │  │  └────────────────────────────────┘  │ │
│  │                         │  │                                       │ │
│  │                         │  │  ┌────────────────────────────────┐  │ │
│  │                         │  │  │ Automation Queue               │  │ │
│  │                         │  │  │ 1. Scroll Right                │  │ │
│  │                         │  │  │ 2. Rotate 90°                  │  │ │
│  │                         │  │  │ [+ Add Action] [Apply]         │  │ │
│  │                         │  │  └────────────────────────────────┘  │ │
│  └─────────────────────────┘  └──────────────────────────────────────┘ │
│                                                                          │
│  ┌──────────────────────────────────────────────────────────────────┐ │
│  │ Timeline                                                          │ │
│  │ ┌──┐ ┌──┐ ┌──┐ ┌──┐ ┌──┐                                        │ │
│  │ │1 │ │2 │ │3 │ │4 │ │5 │  [▶ Play] [⏸ Pause] [⏹ Stop]         │ │
│  │ │100│ │100│ │100│ │100│ │100│  Frame: 1  Duration: 500ms        │ │
│  │ └──┘ └──┘ └──┘ └──┘ └──┘                                        │ │
│  └──────────────────────────────────────────────────────────────────┘ │
│                                                                          │
└────────────────────────────────────────────────────────────────────────┘
```

#### Key Components

**Brushes Tab**:
- Drawing tool selection
- Brush size control
- Tool-specific options

**Scratchpads Tab**:
- 8 scratchpad slots (1-8)
- Copy/Paste buttons per slot
- Status indicator

**Layers Tab**:
- Layer list for current frame
- Add/Remove layer buttons
- Visibility and opacity controls
- Layer reordering

**Effects Tab**:
- Effects library browser
- Category filter
- Effect preview
- Apply button

**Automation Tab**:
- Action queue list
- Add action dialog
- Parameter configuration
- Preview and apply buttons

**Export Tab**:
- Export format selection (DAT, BIN, HEX, LEDS, JSON, Project)
- Export options
- Code template export

---

### Tab 3: 👁️ Preview Tab

**Purpose**: Real-time LED matrix visualization and playback

#### Features
- **LED Simulator**: 60 FPS real-time LED matrix preview
- **Playback Controls**: Play, Pause, Stop, Frame-by-frame navigation
- **Speed Control**: Adjustable FPS (1-60)
- **Brightness Control**: Software brightness adjustment (0-100%)
- **Frame Scrubber**: Timeline scrubbing for frame navigation
- **Zoom Controls**: Zoom in/out for detailed viewing
- **Fullscreen Mode**: Fullscreen preview
- **Color Order**: RGB, BGR, GRB configuration
- **Matrix Layout**: Configure matrix orientation and wiring

#### Wireframe Layout

```
┌────────────────────────────────────────────────────────────┐
│ 👁️ Preview                                              [X]│
├────────────────────────────────────────────────────────────┤
│                                                              │
│  ┌────────────────────────────────────────────────────┐   │
│  │  LED Matrix Simulator                                │   │
│  │  ┌──────────────────────────────────────────────┐  │   │
│  │  │                                              │  │   │
│  │  │                                              │  │   │
│  │  │         [16×16 LED Matrix Display]          │  │   │
│  │  │         (Real-time Animation)                │  │   │
│  │  │                                              │  │   │
│  │  │                                              │  │   │
│  │  └──────────────────────────────────────────────┘  │   │
│  │  Zoom: [🔍-] [100%] [🔍+]                          │   │
│  └────────────────────────────────────────────────────┘   │
│                                                              │
│  ┌────────────────────────────────────────────────────┐   │
│  │  Playback Controls                                   │   │
│  │  [⏮ First] [⏪ Prev] [▶ Play] [⏸ Pause] [⏹ Stop] │   │
│  │  [⏩ Next] [⏭ Last]                                │   │
│  └────────────────────────────────────────────────────┘   │
│                                                              │
│  ┌────────────────────────────────────────────────────┐   │
│  │  Settings                                            │   │
│  │  FPS: [24 ▼]  Brightness: [████████░░] 100%       │   │
│  │  Color Order: [RGB ▼]  Matrix: [16×16 ▼]          │   │
│  └────────────────────────────────────────────────────┘   │
│                                                              │
│  ┌────────────────────────────────────────────────────┐   │
│  │  Timeline                                           │   │
│  │  ┌──────────────────────────────────────────────┐  │   │
│  │  │◄───●─────────────────────────────────────────┤  │   │
│  │  └──────────────────────────────────────────────┘  │   │
│  │  Frame: 3/10   Position: 300ms / 1000ms          │   │
│  └────────────────────────────────────────────────────┘   │
│                                                              │
└────────────────────────────────────────────────────────────┘
```

#### Key Methods
- `load_pattern(pattern)`: Load pattern for preview
- `play()`: Start playback
- `pause()`: Pause playback
- `stop()`: Stop and reset playback
- `set_fps(fps)`: Set playback speed
- `set_brightness(level)`: Adjust brightness

---

### Tab 4: ⚡ Flash Tab

**Purpose**: Build firmware and upload patterns to microcontroller boards via USB

#### Features
- **Chip Selection**: 14+ microcontroller types
  - ESP8266, ESP32, ESP32-S3
  - ATmega328P, ATmega2560, ATtiny85
  - STM32F103C8, STM32F407
  - PIC16F876A, PIC18F4550
  - Nuvoton M031, M051
- **Port Detection**: Auto-detect serial ports
- **GPIO Configuration**: Configure data pin
- **Firmware Building**: Compile pattern into firmware
- **Progress Tracking**: Real-time build/flash progress
- **Logging**: Detailed operation logs
- **Verify Option**: Verify uploaded firmware
- **Board Configuration**: Memory, flash size, upload speed

#### Wireframe Layout

```
┌────────────────────────────────────────────────────────────┐
│ ⚡ Flash                                                 [X]│
├────────────────────────────────────────────────────────────┤
│                                                              │
│  ┌────────────────────────────────────────────────────┐   │
│  │  Hardware Selection                                  │   │
│  │  Chip: [ESP8266 ▼]                                  │   │
│  │  Port: [COM3 ▼] [🔄 Refresh]                        │   │
│  │  GPIO Pin: [2 ▼]                                    │   │
│  └────────────────────────────────────────────────────┘   │
│                                                              │
│  ┌────────────────────────────────────────────────────┐   │
│  │  Pattern Info                                        │   │
│  │  Size: 16×16  Frames: 5  Duration: 500ms          │   │
│  │  Memory: ~2.5KB  Flash: ~15KB                      │   │
│  └────────────────────────────────────────────────────┘   │
│                                                              │
│  ┌────────────────────────────────────────────────────┐   │
│  │  Firmware Options                                    │   │
│  │  [✓] Verify after flash                              │   │
│  │  [✓] Clear EEPROM                                    │   │
│  │  Upload Speed: [115200 ▼]                          │   │
│  └────────────────────────────────────────────────────┘   │
│                                                              │
│  ┌────────────────────────────────────────────────────┐   │
│  │  Actions                                            │   │
│  │  [Build Firmware]  [Flash to Device]  [Save Firmware]│  │
│  └────────────────────────────────────────────────────┘   │
│                                                              │
│  ┌────────────────────────────────────────────────────┐   │
│  │  Progress & Logs                                     │   │
│  │  Building firmware...                                │   │
│  │  ┌──────────────────────────────────────────────┐  │   │
│  │  │████████████░░░░░░░░░░░░░░░░░░░░ 50%          │  │   │
│  │  └──────────────────────────────────────────────┘  │   │
│  │  [Compile] Generating code...                      │   │
│  │  [Compile] Compiling with Arduino CLI...          │   │
│  │  [Flash] Uploading to COM3...                     │   │
│  │  [Success] Flash complete!                        │   │
│  └────────────────────────────────────────────────────┘   │
│                                                              │
└────────────────────────────────────────────────────────────┘
```

#### Supported Chips

| Chip Family | Models | Flash | RAM | GPIO |
|------------|--------|-------|-----|------|
| **ESP** | ESP8266, ESP32, ESP32-S3 | 4MB | 80KB-520KB | 11-34 |
| **AVR** | ATmega328P, ATmega2560, ATtiny85 | 8-256KB | 512B-8KB | 6-70 |
| **STM32** | STM32F103C8, STM32F407 | 64-512KB | 20-192KB | 37-82 |
| **PIC** | PIC16F876A, PIC18F4550 | 14-32KB | 368B-2KB | 22-35 |
| **Nuvoton** | M031, M051 | 32-64KB | 8-16KB | 26-51 |

---

### Tab 5: 🚀 Batch Flash Tab

**Purpose**: Flash patterns to multiple devices simultaneously

#### Features
- **Multi-Device Selection**: Select multiple ports/devices
- **Concurrent Flashing**: Configurable concurrent operations
- **Progress Tracking**: Per-device progress indicators
- **Results Table**: Success/failure status per device
- **Queue Management**: Add/remove devices from queue
- **Error Handling**: Individual device error reporting
- **Summary Report**: Overall operation statistics

#### Wireframe Layout

```
┌────────────────────────────────────────────────────────────┐
│ 🚀 Batch Flash                                           [X]│
├────────────────────────────────────────────────────────────┤
│                                                              │
│  ┌────────────────────────────────────────────────────┐   │
│  │  Device Selection                                    │   │
│  │  Available Ports:                                    │   │
│  │  [✓] COM3 - ESP8266                                  │   │
│  │  [✓] COM5 - ESP8266                                  │   │
│  │  [ ] COM7 - ATmega328P                               │   │
│  │  [✓] COM9 - ESP32                                    │   │
│  │  [🔄 Refresh Ports]  [Select All] [Clear All]       │   │
│  └────────────────────────────────────────────────────┘   │
│                                                              │
│  ┌────────────────────────────────────────────────────┐   │
│  │  Settings                                            │   │
│  │  Chip Type: [ESP8266 ▼]                            │   │
│  │  Max Concurrent: [2 ▼]                             │   │
│  │  GPIO Pin: [2 ▼]                                    │   │
│  └────────────────────────────────────────────────────┘   │
│                                                              │
│  ┌────────────────────────────────────────────────────┐   │
│  │  Progress                                            │   │
│  │  ┌────────────────────────────────────────────────┐│   │
│  │  │ Device        Status      Progress              ││   │
│  │  ├────────────────────────────────────────────────┤│   │
│  │  │ COM3          ████████░░  80%  Building...     ││   │
│  │  │ COM5          ██████████  100%  ✓ Complete     ││   │
│  │  │ COM9          ████░░░░░░  40%  Flashing...     ││   │
│  │  └────────────────────────────────────────────────┘│   │
│  │  Overall: 2/3 complete (66%)                       │   │
│  └────────────────────────────────────────────────────┘   │
│                                                              │
│  ┌────────────────────────────────────────────────────┐   │
│  │  Actions                                            │   │
│  │  [Start Batch Flash]  [Cancel]  [Export Report]    │   │
│  └────────────────────────────────────────────────────┘   │
│                                                              │
└────────────────────────────────────────────────────────────┘
```

---

### Tab 6: 📚 Pattern Library Tab

**Purpose**: Browse, search, and manage local pattern library

#### Features
- **Pattern Browser**: Grid/list view of patterns
- **Thumbnails**: Visual pattern previews
- **Search**: Text search across pattern names/descriptions
- **Filtering**: Filter by category, tags, size
- **Pattern Details**: View pattern metadata
- **Add/Remove**: Add patterns to library, remove patterns
- **Category Management**: Organize by categories
- **Tag System**: Tag patterns for easy finding

#### Wireframe Layout

```
┌────────────────────────────────────────────────────────────┐
│ 📚 Pattern Library                                       [X]│
├────────────────────────────────────────────────────────────┤
│                                                              │
│  ┌────────────────────────────────────────────────────┐   │
│  │  Search & Filter                                    │   │
│  │  [🔍 Search patterns...]  Category: [All ▼]        │   │
│  │  Tags: [All] [RGB] [Animation] [Text]              │   │
│  └────────────────────────────────────────────────────┘   │
│                                                              │
│  ┌────────────────────────────────────────────────────┐   │
│  │  Pattern Grid                                        │   │
│  │  ┌──────┐ ┌──────┐ ┌──────┐ ┌──────┐              │   │
│  │  │[Img] │ │[Img] │ │[Img] │ │[Img] │              │   │
│  │  │Name  │ │Name  │ │Name  │ │Name  │              │   │
│  │  │16×16 │ │32×32 │ │16×16 │ │8×8   │              │   │
│  │  └──────┘ └──────┘ └──────┘ └──────┘              │   │
│  │  ┌──────┐ ┌──────┐ ┌──────┐ ┌──────┐              │   │
│  │  │[Img] │ │[Img] │ │[Img] │ │[Img] │              │   │
│  │  │Name  │ │Name  │ │Name  │ │Name  │              │   │
│  │  │16×32 │ │32×32 │ │16×16 │ │8×8   │              │   │
│  │  └──────┘ └──────┘ └──────┘ └──────┘              │   │
│  └────────────────────────────────────────────────────┘   │
│                                                              │
│  ┌────────────────────────────────────────────────────┐   │
│  │  Selected Pattern Details                           │   │
│  │  Name: Example Pattern                              │   │
│  │  Size: 16×16  Frames: 10  Duration: 1000ms        │   │
│  │  Category: Animation  Tags: RGB, Text              │   │
│  │  Created: 2025-01-15  Modified: 2025-01-15        │   │
│  │  File: C:\Patterns\example.dat                     │   │
│  └────────────────────────────────────────────────────┘   │
│                                                              │
│  ┌────────────────────────────────────────────────────┐   │
│  │  Actions                                            │   │
│  │  [Add Pattern] [Remove] [Edit] [Load Pattern]      │   │
│  └────────────────────────────────────────────────────┘   │
│                                                              │
└────────────────────────────────────────────────────────────┘
```

---

### Tab 7: 🎵 Audio Reactive Tab

**Purpose**: Generate audio-reactive LED patterns from audio input

#### Features
- **Audio Input Selection**: Select audio device/microphone
- **Real-time Visualization**: Live audio visualization
- **Visualization Modes**: 
  - VU Meter (Volume Unit meter)
  - Frequency Spectrum
  - Waveform
  - Beat Detection
- **Pattern Generation**: Generate patterns from audio
- **Sensitivity Control**: Adjust audio sensitivity
- **Frequency Bands**: Configure frequency band mapping
- **Recording**: Record audio-reactive patterns

#### Wireframe Layout

```
┌────────────────────────────────────────────────────────────┐
│ 🎵 Audio Reactive                                        [X]│
├────────────────────────────────────────────────────────────┤
│                                                              │
│  ┌────────────────────────────────────────────────────┐   │
│  │  Audio Input                                         │   │
│  │  Device: [Microphone ▼] [🔴 Test]                  │   │
│  │  Sensitivity: [████████░░] 80%                     │   │
│  │  Status: ● Listening                                │   │
│  └────────────────────────────────────────────────────┘   │
│                                                              │
│  ┌────────────────────────────────────────────────────┐   │
│  │  Visualization Mode                                  │   │
│  │  (●) VU Meter  ( ) Spectrum  ( ) Waveform          │   │
│  │  ( ) Beat Detection                                 │   │
│  └────────────────────────────────────────────────────┘   │
│                                                              │
│  ┌────────────────────────────────────────────────────┐   │
│  │  Live Preview                                        │   │
│  │  ┌──────────────────────────────────────────────┐  │   │
│  │  │                                              │  │   │
│  │  │         [Audio-Reactive LED Display]        │  │   │
│  │  │         (Real-time Audio Visualization)      │  │   │
│  │  │                                              │  │   │
│  │  └──────────────────────────────────────────────┘  │   │
│  │  Volume: ████████░░░░░░  Frequency: 440Hz        │   │
│  └────────────────────────────────────────────────────┘   │
│                                                              │
│  ┌────────────────────────────────────────────────────┐   │
│  │  Pattern Settings                                    │   │
│  │  Matrix Size: [16×16 ▼]  Color Mode: [RGB ▼]      │   │
│  │  Duration: [5000ms ▼]  FPS: [30 ▼]                │   │
│  └────────────────────────────────────────────────────┘   │
│                                                              │
│  ┌────────────────────────────────────────────────────┐   │
│  │  Actions                                            │   │
│  │  [▶ Start] [⏸ Pause] [⏹ Stop] [💾 Generate Pattern]│  │
│  └────────────────────────────────────────────────────┘   │
│                                                              │
└────────────────────────────────────────────────────────────┘
```

---

### Tab 8: 📡 WiFi Upload Tab

**Purpose**: Upload patterns wirelessly to ESP8266/ESP32 devices over WiFi

#### Features
- **WiFi Configuration**: ESP device IP address and port
- **Pattern Selection**: Select pattern file to upload
- **Connection Status**: Real-time connection status indicator
- **Upload Progress**: Progress bar for upload operations
- **Web Interface**: Access ESP web interface
- **Schedule Management**: Configure pattern schedules
- **Brightness Control**: Remote brightness adjustment
- **Status Monitoring**: Monitor device status

#### Wireframe Layout

```
┌────────────────────────────────────────────────────────────┐
│ 📡 WiFi Upload                                           [X]│
├────────────────────────────────────────────────────────────┤
│                                                              │
│  ┌────────────────────────────────────────────────────┐   │
│  │  Device Connection                                  │   │
│  │  IP Address: [192.168.1.100]                       │   │
│  │  Port: [80 ▼]  [Connect]  Status: ● Connected     │   │
│  │  Device: ESP8266  Firmware: v2.1                   │   │
│  └────────────────────────────────────────────────────┘   │
│                                                              │
│  ┌────────────────────────────────────────────────────┐   │
│  │  Pattern Selection                                   │   │
│  │  Pattern File: [📁 Browse...]                       │   │
│  │  Size: 16×16  Frames: 10  Duration: 1000ms        │   │
│  │  Memory: ~2.5KB                                     │   │
│  └────────────────────────────────────────────────────┘   │
│                                                              │
│  ┌────────────────────────────────────────────────────┐   │
│  │  Upload Settings                                     │   │
│  │  Brightness: [████████░░] 100%                     │   │
│  │  Auto-play: [✓] Enable                              │   │
│  │  Loop: [✓] Enable                                   │   │
│  └────────────────────────────────────────────────────┘   │
│                                                              │
│  ┌────────────────────────────────────────────────────┐   │
│  │  Upload Progress                                     │   │
│  │  Uploading pattern...                                │   │
│  │  ┌──────────────────────────────────────────────┐  │   │
│  │  │████████████░░░░░░░░░░░░░░░░░░░░ 60%          │  │   │
│  │  └──────────────────────────────────────────────┘  │   │
│  │  [2.5KB / 4.2KB]                                   │   │
│  └────────────────────────────────────────────────────┘   │
│                                                              │
│  ┌────────────────────────────────────────────────────┐   │
│  │  Actions                                            │   │
│  │  [Upload Pattern] [Open Web UI] [Cancel]           │   │
│  └────────────────────────────────────────────────────┘   │
│                                                              │
└────────────────────────────────────────────────────────────┘
```

---

### Tab 9: 🔧 Arduino IDE Tab

**Purpose**: Integrated Arduino IDE-like environment for code editing and compilation

#### Features
- **Code Editor**: Syntax-highlighted code editor
- **Arduino CLI Integration**: Full Arduino CLI support
- **Board Selection**: Select Arduino board type
- **Port Selection**: Select serial port
- **Compile**: Compile Arduino sketches
- **Upload**: Upload compiled code to board
- **Verify**: Verify code compilation
- **Serial Monitor**: Real-time serial communication
- **File Management**: Open, save, new sketch files
- **Library Management**: Install/manage Arduino libraries

#### Wireframe Layout

```
┌────────────────────────────────────────────────────────────┐
│ 🔧 Arduino IDE                                           [X]│
├────────────────────────────────────────────────────────────┤
│ [File] [Edit] [Sketch] [Tools] [Help]                      │
│ [New] [Open] [Save]                                        │
├────────────────────────────────────────────────────────────┤
│                                                              │
│  ┌────────────────────────────────────────────────────┐   │
│  │  Toolbar                                            │   │
│  │  Board: [Arduino Uno ▼]  Port: [COM3 ▼]          │   │
│  │  [✓ Verify] [➡ Upload] [Serial Monitor]           │   │
│  └────────────────────────────────────────────────────┘   │
│                                                              │
│  ┌────────────────────────────────────────────────────┐   │
│  │  Code Editor                                        │   │
│  │  ┌──────────────────────────────────────────────┐  │   │
│  │  │ 1 │ void setup() {                           │  │   │
│  │  │ 2 │   Serial.begin(115200);                  │  │   │
│  │  │ 3 │   // LED Pattern Code                    │  │   │
│  │  │ 4 │   initLEDMatrix();                       │  │   │
│  │  │ 5 │ }                                        │  │   │
│  │  │ 6 │                                          │  │   │
│  │  │ 7 │ void loop() {                            │  │   │
│  │  │ 8 │   displayPattern();                      │  │   │
│  │  │ 9 │   delay(100);                            │  │   │
│  │  │10 │ }                                        │  │   │
│  │  │   │                                          │  │   │
│  │  └──────────────────────────────────────────────┘  │   │
│  │  sketch.ino                              Line 8, Col 20│
│  └────────────────────────────────────────────────────┘   │
│                                                              │
│  ┌────────────────────────────────────────────────────┐   │
│  │  Status & Output                                    │   │
│  │  [Compile Output ▼]                                 │   │
│  │  ┌──────────────────────────────────────────────┐  │   │
│  │  │ Compiling sketch...                           │  │   │
│  │  │ Sketch uses 1234 bytes (4%) of program storage│  │   │
│  │  │ Upload complete!                               │  │   │
│  │  └──────────────────────────────────────────────┘  │   │
│  └────────────────────────────────────────────────────┘   │
│                                                              │
└────────────────────────────────────────────────────────────┘
```

---

## 📐 Wireframe Documentation

### Main Window Layout

```
┌──────────────────────────────────────────────────────────────────────────────┐
│ Upload Bridge - Universal LED Pattern Flasher                      [_][□][X] │
├──────────────────────────────────────────────────────────────────────────────┤
│ File  Edit  Tools  View  Help                                                │
│ [📂] [💾] [👁️] [⚡]                                                          │
├──────────────────────────────────────────────────────────────────────────────┤
│                                                                                │
│  ┌────────────────────────────────────────────────────────────────────────┐ │
│  │  Tab Widget                                                             │ │
│  │  ┌──────────────────────────────────────────────────────────────────┐  │ │
│  │  │ 🎬 Media Upload | 🎨 Design Tools | 👁️ Preview | ⚡ Flash | ...│  │ │
│  │  └──────────────────────────────────────────────────────────────────┘  │ │
│  │                                                                          │ │
│  │  ┌──────────────────────────────────────────────────────────────────┐  │ │
│  │  │                                                                   │  │ │
│  │  │                                                                   │  │ │
│  │  │              [Active Tab Content Area]                           │  │ │
│  │  │                                                                   │  │ │
│  │  │                                                                   │  │ │
│  │  └──────────────────────────────────────────────────────────────────┘  │ │
│  └────────────────────────────────────────────────────────────────────────┘ │
│                                                                                │
├──────────────────────────────────────────────────────────────────────────────┤
│ Ready - Load a pattern to get started                          Memory: 0KB  │
└──────────────────────────────────────────────────────────────────────────────┘
```

### Design Tools Tab - Complete Wireframe

```
┌──────────────────────────────────────────────────────────────────────────────┐
│ 🎨 Design Tools                                                              │
├──────────────────────────────────────────────────────────────────────────────┤
│ [New] [Open] [Save]  Matrix: 16×16  Frame: 1/5  Layer: 1  FPS: [24▼]       │
├──────────────────────────────────────────────────────────────────────────────┤
│                                                                                │
│ ┌────────────────────────────────┐  ┌──────────────────────────────────────┐│
│ │                                │  │  [Brushes] [Scratch] [Layers]        ││
│ │                                │  │  [Effects] [Automation] [Export]     ││
│ │                                │  │                                      ││
│ │                                │  │  ┌────────────────────────────────┐ ││
│ │                                │  │  │ Drawing Tools                   │ ││
│ │                                │  │  │ ┌──┐ ┌──┐ ┌──┐ ┌──┐            │ ││
│ │                                │  │  │ │● │ │▭ │ │○ │ │─ │            │ ││
│ │                                │  │  │ └──┘ └──┘ └──┘ └──┘            │ ││
│ │                                │  │  │ ┌──┐ ┌──┐                       │ ││
│ │                                │  │  │ │✨│ │🌈│                       │ ││
│ │                                │  │  │ └──┘ └──┘                       │ ││
│ │       CANVAS                   │  │  └────────────────────────────────┘ ││
│ │                                │  │                                      ││
│ │   [LED Matrix Grid]            │  │  ┌────────────────────────────────┐ ││
│ │                                │  │  │ Color Palette                   │ ││
│ │                                │  │  │ ┌─┐ ┌─┐ ┌─┐ ┌─┐                │ ││
│ │                                │  │  │ │■│ │■│ │■│ │■│                │ ││
│ │                                │  │  │ └─┘ └─┘ └─┘ └─┘                │ ││
│ │                                │  │  │ ┌─┐ ┌─┐ ┌─┐ ┌─┐                │ ││
│ │                                │  │  │ │■│ │■│ │■│ │■│                │ ││
│ │                                │  │  │ └─┘ └─┘ └─┘ └─┘                │ ││
│ │                                │  │  │ [🎨 Custom]                     │ ││
│ │                                │  │  └────────────────────────────────┘ ││
│ │                                │  │                                      ││
│ │                                │  │  ┌────────────────────────────────┐ ││
│ │                                │  │  │ Frame Ops                       │ ││
│ │                                │  │  │ [+ Add] [📋] [🗑]              │ ││
│ │                                │  │  │ Duration: [100ms ▼]            │ ││
│ │                                │  │  └────────────────────────────────┘ ││
│ └────────────────────────────────┘  └──────────────────────────────────────┘│
│                                                                                │
│ ┌──────────────────────────────────────────────────────────────────────────┐│
│ │ Timeline                                                                  ││
│ │ ┌────┐ ┌────┐ ┌────┐ ┌────┐ ┌────┐                                      ││
│ │ │ 1  │ │ 2  │ │ 3  │ │ 4  │ │ 5  │   [▶] [⏸] [⏹]  Frame: 1           ││
│ │ │100ms│ │100ms│ │100ms│ │100ms│ │100ms│                                      ││
│ │ └────┘ └────┘ └────┘ └────┘ └────┘                                      ││
│ │ ◄───●────────────────────────────────                                    ││
│ └──────────────────────────────────────────────────────────────────────────┘│
│                                                                                │
└──────────────────────────────────────────────────────────────────────────────┘
```

---

## 📋 Feature Catalog

### Core Features by Category

#### 1. Pattern Creation & Editing
- ✅ Interactive canvas painting
- ✅ 6 drawing tools
- ✅ Multi-layer support
- ✅ Frame management
- ✅ Timeline editing
- ✅ Color palette
- ✅ Scratchpads

#### 2. Automation & Effects
- ✅ Automation action queue
- ✅ 8+ automation actions
- ✅ Effects library
- ✅ Preview automation
- ✅ Apply automation to frames

#### 3. Import/Export
- ✅ 10+ import formats (DAT, BIN, HEX, LEDS, JSON, images, GIF, video)
- ✅ 7+ export formats (DAT, BIN, HEX, LEDS, JSON, Project, Code templates)
- ✅ Auto dimension detection
- ✅ Format conversion

#### 4. Preview & Visualization
- ✅ Real-time LED simulator
- ✅ 60 FPS playback
- ✅ Frame-by-frame navigation
- ✅ Brightness control
- ✅ Speed control
- ✅ Zoom controls

#### 5. Hardware Deployment
- ✅ USB flashing (14+ chips)
- ✅ WiFi upload (ESP8266/ESP32)
- ✅ Batch flashing
- ✅ Firmware building
- ✅ Progress tracking

#### 6. Pattern Management
- ✅ Pattern library
- ✅ Search and filter
- ✅ Categories and tags
- ✅ Pattern metadata

#### 7. Audio Features
- ✅ Audio-reactive patterns
- ✅ Real-time audio visualization
- ✅ Multiple visualization modes
- ✅ Pattern generation from audio

#### 8. Development Tools
- ✅ Arduino IDE integration
- ✅ Code editor
- ✅ Compile and upload
- ✅ Serial monitor

---

## 🔄 User Flows

### Flow 1: Create Pattern from Scratch

```
1. Launch Application
   ↓
2. Click "Design Tools" Tab
   ↓
3. Click "New" Button
   ↓
4. Configure Matrix Size (16×16)
   ↓
5. Select Drawing Tool (Pixel)
   ↓
6. Select Color from Palette
   ↓
7. Draw on Canvas
   ↓
8. Add Frame (Ctrl+Shift+A)
   ↓
9. Draw Next Frame
   ↓
10. Preview (Click Preview Tab)
    ↓
11. Export (Design Tools → Export Tab)
```

### Flow 2: Convert Media to Pattern

```
1. Launch Application
   ↓
2. Click "Media Upload" Tab
   ↓
3. Click "Browse Files"
   ↓
4. Select Image/GIF/Video File
   ↓
5. Configure Settings (Size, FPS, Color)
   ↓
6. Preview Conversion
   ↓
7. Click "Convert & Load"
   ↓
8. Pattern Loaded → Available in All Tabs
   ↓
9. Click "Preview" Tab to View
   ↓
10. Click "Flash" Tab to Upload
```

### Flow 3: Flash Pattern to Device

```
1. Load Pattern (any method)
   ↓
2. Click "Flash" Tab
   ↓
3. Select Chip Type (ESP8266)
   ↓
4. Select Port (COM3)
   ↓
5. Configure GPIO Pin (2)
   ↓
6. Click "Build Firmware"
   ↓
7. Wait for Build Complete
   ↓
8. Click "Flash to Device"
   ↓
9. Monitor Progress
   ↓
10. Flash Complete!
```

### Flow 4: Batch Flash Multiple Devices

```
1. Load Pattern
   ↓
2. Click "Batch Flash" Tab
   ↓
3. Select Multiple Ports (COM3, COM5, COM9)
   ↓
4. Configure Chip Type & GPIO
   ↓
5. Set Max Concurrent (2)
   ↓
6. Click "Start Batch Flash"
   ↓
7. Monitor Progress per Device
   ↓
8. View Results Table
   ↓
9. Export Report (optional)
```

### Flow 5: WiFi Upload Pattern

```
1. Load Pattern
   ↓
2. Click "WiFi Upload" Tab
   ↓
3. Enter ESP Device IP (192.168.1.100)
   ↓
4. Click "Connect"
   ↓
5. Select Pattern File
   ↓
6. Configure Settings (Brightness, Auto-play)
   ↓
7. Click "Upload Pattern"
   ↓
8. Monitor Upload Progress
   ↓
9. Upload Complete!
```

---

## 🔧 Technical Specifications

### Supported File Formats

| Format | Extension | Import | Export | Notes |
|--------|-----------|--------|--------|-------|
| **Binary** | .bin | ✅ | ✅ | Raw binary pattern data |
| **Intel HEX** | .hex | ✅ | ✅ | Standard HEX format |
| **DAT** | .dat | ✅ | ✅ | Text-based format |
| **LEDS** | .leds | ✅ | ✅ | LED Matrix Studio format |
| **JSON** | .json | ✅ | ✅ | JSON pattern format |
| **Project** | .ledproj | ✅ | ✅ | Upload Bridge project |
| **PNG/JPEG** | .png, .jpg | ✅ | ❌ | Single image import |
| **GIF** | .gif | ✅ | ❌ | Animated GIF import |
| **Video** | .mp4, .avi | ✅ | ❌ | Video frame extraction |
| **C Header** | .h | ❌ | ✅ | Code template export |

### Supported Microcontrollers

| Family | Models | Flash | RAM | GPIO |
|--------|--------|-------|-----|------|
| **ESP8266** | ESP-01, NodeMCU, Wemos D1 | 4MB | 80KB | 11 |
| **ESP32** | ESP32, ESP32-S, ESP32-C3 | 4MB | 520KB | 34 |
| **ATmega328P** | Arduino Uno, Nano | 32KB | 2KB | 20 |
| **ATmega2560** | Arduino Mega | 256KB | 8KB | 70 |
| **ATtiny85** | ATtiny85 | 8KB | 512B | 6 |
| **STM32F103C8** | Blue Pill | 64KB | 20KB | 37 |
| **STM32F407** | STM32F407 | 512KB | 192KB | 82 |
| **PIC16F876A** | PIC16F876A | 14KB | 368B | 22 |
| **PIC18F4550** | PIC18F4550 | 32KB | 2KB | 35 |
| **Nuvoton M031** | M031 | 32KB | 8KB | 26 |
| **Nuvoton M051** | M051 | 64KB | 16KB | 51 |

### System Requirements

- **OS**: Windows 10+, Linux, macOS
- **Python**: 3.8+
- **Qt**: PySide6 6.0+
- **RAM**: 512MB minimum, 1GB recommended
- **Storage**: 100MB for application, additional for patterns
- **USB**: For hardware flashing
- **Network**: Optional (for WiFi upload)

---

## 📊 Statistics Summary

- **Total Tabs**: 9
- **Core Features**: 50+
- **Drawing Tools**: 6
- **Automation Actions**: 8+
- **Supported Chips**: 14+
- **File Formats**: 10+
- **Lines of Code**: 9,050+
- **Test Coverage**: 54 E2E tests (all passing)
- **Documentation**: Comprehensive

---

## 🎯 Conclusion

Upload Bridge provides a complete, professional-grade solution for LED pattern design, editing, preview, and deployment. With 9 feature-rich tabs, support for 14+ microcontrollers, and 10+ file formats, it serves as a comprehensive platform for LED matrix projects.

The application follows modern software architecture principles with clean separation of concerns, comprehensive error handling, and extensive test coverage. All features are production-ready and fully tested.

---

**Document Version**: 3.0  
**Last Updated**: 2025-01-XX  
**Status**: Production Ready ✅

