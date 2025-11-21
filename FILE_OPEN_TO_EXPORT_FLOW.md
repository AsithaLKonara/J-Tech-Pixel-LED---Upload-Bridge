# 📂 File Open → Export Flow & Tab Synchronization Overview

**Version:** 1.1 | **Last Updated:** 2025-10-29  
**Status:** Production Ready | **Related Docs:** USER_FLOWS.md, ARCHITECTURE_GUIDE.md

---

## 📋 Table of Contents
1. [Application State Machine](#application-state-machine)
2. [Complete Flow Diagram](#complete-flow-diagram)
3. [Tab Synchronization Details](#tab-synchronization-details)
4. [Export Flow](#export-flow)
5. [Event-Driven Communication](#event-driven-communication)
6. [Edge Cases & Error Handling](#edge-cases--error-handling)
7. [Related Documentation](#related-documentation)

---

## 🎯 Application State Machine

```
┌─────────────────────────────────────────────────────────────────┐
│                    APPLICATION STATE FLOW                        │
└─────────────────────────────────────────────────────────────────┘

                    ┌─────────┐
                    │  CLOSED │ (No pattern loaded)
                    └────┬────┘
                         │
                         │ User: File > Open
                         │ Event: file_open_requested
                         ▼
                  ┌──────────────┐
                  │   LOADING    │ (File being processed)
                  │  Event:      │
                  │  file_loading│
                  └──────┬───────┘
                         │
         ┌───────────────┴───────────────┐
         │                               │
         ▼                               ▼
┌─────────────────┐           ┌─────────────────┐
│  LOAD_SUCCESS   │           │  LOAD_FAILURE   │
│  Pattern created│           │  Error dialog   │
│  Event:         │           │  Event:         │
│  pattern_loaded │           │  load_error     │
└────────┬────────┘           └─────────────────┘
         │
         │ load_pattern_to_all_tabs()
         │ Event: sync_initiated
         ▼
┌─────────────────┐
│   SYNCHRONIZED  │ (Pattern loaded in all tabs)
│  Event:         │
│  all_tabs_synced│
└────────┬────────┘
         │
         │ Optional: User edits in Preview Tab
         │ Event: pattern_modified
         ▼
┌─────────────────┐
│    MODIFIED     │ (Pattern changed, unsaved)
│  is_dirty = True│
└────────┬────────┘
         │
         ├─→ User: File > Save Project
         │   Event: save_requested
         │   └─→ Back to SYNCHRONIZED
         │
         └─→ User: Export/Flash/Upload
             Event: export_requested
             ▼
┌─────────────────┐
│    EXPORTED     │ (Pattern saved/uploaded)
└─────────────────┘

State Transitions Summary:
• CLOSED → LOADING: File open initiated
• LOADING → LOAD_SUCCESS: Pattern created
• LOADING → LOAD_FAILURE: Error occurred
• LOAD_SUCCESS → SYNCHRONIZED: Tabs updated
• SYNCHRONIZED → MODIFIED: User edits pattern
• MODIFIED → SYNCHRONIZED: Pattern saved
• SYNCHRONIZED → EXPORTED: Pattern exported
• MODIFIED → EXPORTED: Modified pattern exported
```

## 🎯 Complete Flow Diagram: Media/Pattern File → All Tabs → Export

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    FILE OPEN PROCESS                                     │
└─────────────────────────────────────────────────────────────────────────┘

USER ACTION: File > Open OR Toolbar "Open" Button
         │
         ▼
┌─────────────────────────────────────────────────────────────────────────┐
│  STEP 1: File Dialog Opens                                               │
│  ─────────────────────────────────────────────────────────────────────  │
│  File Filters Shown:                                                      │
│  • All Supported (*.bin *.hex *.dat *.leds *.ledadmin *.ledproj          │
│                   *.mp4 *.avi *.mov *.mkv *.webm *.gif                   │
│                   *.jpg *.jpeg *.png *.bmp)                               │
│  • Pattern Files (*.bin *.hex *.dat *.leds)                              │
│  • Media Files (*.mp4 *.avi *.mov *.mkv *.webm *.gif *.jpg *.jpeg *.png)│
│  • Project Files (*.ledproj)                                             │
│  • All Files (*.*)                                                       │
└─────────────────────────────────────────────────────────────────────────┘
         │
         ▼
┌─────────────────────────────────────────────────────────────────────────┐
│  STEP 2: File Type Detection                                             │
│  ─────────────────────────────────────────────────────────────────────  │
│  function: open_pattern()                                                 │
│  Event: file_open_requested                                              │
│  Status Bar: "Loading [filename]..."                                     │
│                                                                           │
│  Media Extensions Check:                                                  │
│  ['.mp4', '.avi', '.mov', '.mkv', '.webm',                               │
│   '.gif', '.jpg', '.jpeg', '.png', '.bmp']                               │
│                                                                           │
│         ├─→ IS MEDIA FILE?                                                │
│         │   │                                                             │
│         │   ├─→ YES ──────────────────────────────────────────┐         │
│         │   │                                                   │         │
│         │   └─→ NO                                              │         │
│         │       ├─→ IS .ledproj FILE?                          │         │
│         │       │   │                                           │         │
│         │       │   ├─→ YES ──────────────────────────┐       │         │
│         │       │   │                                   │       │         │
│         │       │   └─→ NO                              │       │         │
│         │       │       └─→ PATTERN FILE (.bin/.hex/etc)│       │         │
│         │       │                                           │       │     │
│         │       └───────────────────────────────────────────────┘       │
│         │                                                               │ │
│         │                                                               │ │
│         ▼                                                               │ │
│  ┌─────────────────────────────────────────────────────────────┐     │ │
│  │ PATH A: PATTERN FILE (.bin/.hex/.dat/.leds)                  │     │ │
│  └─────────────────────────────────────────────────────────────┘     │ │
│         │                                                               │ │
│         ▼                                                               │ │
│  ParserRegistry.validate_file(file_path)                                │ │
│         │                                                               │ │
│         ├─→ Auto-Detection Success?                                    │ │
│         │   │                                                           │ │
│         │   ├─→ YES ───────────────────────────────────┐              │ │
│         │   │   ↓                                        │              │ │
│         │   │   parse_pattern_file(file_path)           │              │ │
│         │   │   • Auto-detects LEDs/frames              │              │ │
│         │   │   • Creates Pattern object                │              │ │
│         │   │                                           │              │ │
│         │   └─→ NO                                       │              │ │
│         │       ↓                                        │              │ │
│         │       Manual Input Dialog                     │              │ │
│         │       • LED Count                             │              │ │
│         │       • Frame Count                           │              │ │
│         │       ↓                                        │              │ │
│         │       parse_pattern_file(file_path,           │              │ │
│         │                          led_count,           │              │ │
│         │                          frame_count)         │              │ │
│         │       • Creates Pattern object                │              │ │
│         │                                               │              │ │
│         └───────────────────────────────────────────────┘              │ │
│                                                                         │ │
│  ┌─────────────────────────────────────────────────────────────┐       │ │
│  │ PATH B: PROJECT FILE (.ledproj)                             │       │ │
│  └─────────────────────────────────────────────────────────────┘       │ │
│         │                                                               │ │
│         ▼                                                               │ │
│  Pattern.load_from_file(file_path)                                    │ │
│  • Deserializes JSON format                                            │ │
│  • Creates Pattern object with all metadata                            │ │
│                                                                         │ │
│  ┌─────────────────────────────────────────────────────────────┐       │ │
│  │ PATH C: MEDIA FILE (video/image/gif)                         │       │ │
│  └─────────────────────────────────────────────────────────────┘       │ │
│         │                                                               │ │
│         ▼                                                               │ │
│  MediaConverter.convert_to_pattern(file_path, metadata)              │ │
│  • Detects media type                                                  │ │
│  • Extracts frames (if video/GIF)                                      │ │
│  • Resizes to target dimensions (default 64x32)                       │ │
│  • Converts RGB pixels                                                 │ │
│  • Creates Pattern object                                              │ │
│                                                                         │ │
│         └───────────────────────────────────────────────────────────────┘
│
┌─────────────────────────────────────────────────────────────────────────┐
│  STEP 3: Pattern Object Created                                         │
│  ─────────────────────────────────────────────────────────────────────  │
│  Pattern object contains:                                                │
│  • id: Unique identifier                                                 │
│  • name: Pattern name                                                    │
│  • metadata: PatternMetadata (width, height, fps, etc.)                 │
│  • frames: List of Frame objects (each with pixels + duration)          │
│                                                                           │
│  Event: pattern_created                                                  │
│  Status Bar: "Loaded: X LEDs, Y frames" or "Converted media: [name]"    │
└─────────────────────────────────────────────────────────────────────────┘
         │
         ▼
┌─────────────────────────────────────────────────────────────────────────┐
│  STEP 4: Load to ALL TABS (Core Synchronization)                       │
│  ─────────────────────────────────────────────────────────────────────  │
│  function: load_pattern_to_all_tabs(pattern, file_path)                  │
│  Event: sync_initiated                                                   │
│                                                                           │
│  ┌──────────────────────────────────────────────────────────────────┐   │
│  │ 1. Store Pattern in Main Window                                  │   │
│  │    self.pattern = pattern                                        │   │
│  │    self.current_file = file_path (if provided)                    │   │
│  │    self.is_dirty = False                                         │   │
│  │    Event: pattern_stored                                         │   │
│  └──────────────────────────────────────────────────────────────────┘   │
│                                                                           │
│  ┌──────────────────────────────────────────────────────────────────┐   │
│  │ 2. Synchronize to Preview Tab                                      │   │
│  │    self.preview_tab.load_pattern(pattern)                         │   │
│  │    ↓                                                               │   │
│  │    PreviewTab.load_pattern() does:                                │   │
│  │    • Stores pattern reference                                     │   │
│  │    • Updates LED simulator widget                                 │   │
│  │    • Updates frame count display                                  │   │
│  │    • Resets playback to frame 0                                   │   │
│  │    • Enables preview controls                                      │   │
│  └──────────────────────────────────────────────────────────────────┘   │
│                                                                           │
│  ┌──────────────────────────────────────────────────────────────────┐   │
│  │ 3. Synchronize to Flash Tab                                       │   │
│  │    self.flash_tab.load_pattern(pattern)                           │   │
│  │    ↓                                                               │   │
│  │    FlashTab.load_pattern() does:                                  │   │
│  │    • Stores pattern reference                                     │   │
│  │    • Updates pattern info display                                 │   │
│  │    • Shows: LEDs, Frames, Size                                    │   │
│  │    • Enables "Build & Flash" button                               │   │
│  │    • Pattern ready for firmware generation                        │   │
│  └──────────────────────────────────────────────────────────────────┘   │
│                                                                           │
│  ┌──────────────────────────────────────────────────────────────────┐   │
│  │ 4. Synchronize to WiFi Upload Tab                                  │   │
│  │    self.wifi_upload_tab.set_pattern(pattern)                      │   │
│  │    ↓                                                               │   │
│  │    WiFiUploadTab.set_pattern() does:                              │   │
│  │    • Stores pattern reference                                     │   │
│  │    • Updates pattern file path display                           │   │
│  │    • Updates pattern info (dimensions, frames)                   │   │
│  │    • Enables "Upload Pattern" button                              │   │
│  │    • Pattern ready for wireless upload                            │   │
│  └──────────────────────────────────────────────────────────────────┘   │
│                                                                           │
│  ┌──────────────────────────────────────────────────────────────────┐   │
│  │ 5. UI Updates                                                     │   │
│  │    • Switch to Preview tab: self.tabs.setCurrentWidget(preview) │   │
│  │    • Update window title: "Upload Bridge - [filename]"           │   │
│  │    • Show success dialog with pattern info                        │   │
│  │    • Update status bar: "Loaded: [info]"                          │   │
│  └──────────────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────┐
│                    TAB STATE AFTER SYNCHRONIZATION                       │
└─────────────────────────────────────────────────────────────────────────┘

┌──────────────────┐  ┌──────────────────┐  ┌──────────────────┐
│  PREVIEW TAB     │  │  FLASH TAB       │  │  WIFI UPLOAD TAB │
├──────────────────┤  ├──────────────────┤  ├──────────────────┤
│ Pattern: ✓       │  │ Pattern: ✓       │  │ Pattern: ✓       │
│ Preview: Active   │  │ Ready to Flash   │  │ Ready to Upload  │
│ Controls: Enabled │  │ Build: Enabled   │  │ Upload: Enabled  │
│                  │  │                  │  │                  │
│ Can:             │  │ Can:             │  │ Can:             │
│ • Play/Preview    │  │ • Select chip    │  │ • Enter ESP IP   │
│ • Adjust bright  │  │ • Select port    │  │ • Test connect   │
│ • Modify speed   │  │ • Configure GPIO │  │ • Upload pattern │
│ • Export         │  │ • Build firmware │  │ • Monitor status │
│ • Save project   │  │ • Flash device   │  │                  │
└──────────────────┘  └──────────────────┘  └──────────────────┘
         │                      │                      │
         └──────────────────────┴──────────────────────┘
                    All tabs synchronized
                    Same Pattern object reference
```

## 🔄 Tab Synchronization Details

### **Synchronization Method: `load_pattern_to_all_tabs()`**

```python
def load_pattern_to_all_tabs(self, pattern: Pattern, file_path: str = None):
    """Central synchronization method - distributes pattern to all tabs"""
    
    # 1. MAIN WINDOW STORAGE
    self.pattern = pattern              # Store in main window
    if file_path:
        self.current_file = file_path   # Remember source file
    self.is_dirty = False              # Mark as clean (not modified)
    
    # 2. PREVIEW TAB SYNCHRONIZATION
    self.preview_tab.load_pattern(pattern)
    # → Calls PreviewTab.load_pattern()
    # → Updates LED simulator
    # → Resets playback state
    # → Enables controls
    
    # 3. FLASH TAB SYNCHRONIZATION
    self.flash_tab.load_pattern(pattern)
    # → Calls FlashTab.load_pattern()
    # → Updates pattern info display
    # → Enables flash button
    # → Pattern ready for firmware generation
    
    # 4. WIFI UPLOAD TAB SYNCHRONIZATION
    self.wifi_upload_tab.set_pattern(pattern)
    # → Calls WiFiUploadTab.set_pattern()
    # → Updates pattern path display
    # → Enables upload button
    # → Pattern ready for wireless upload
    
    # 5. UI STATE UPDATES
    self.tabs.setCurrentWidget(self.preview_tab)  # Show preview
    self.setWindowTitle(f"Upload Bridge - {pattern.name}")
    # Show success message with pattern details
```

### **Pattern Object Structure (Shared Across All Tabs)**

```python
Pattern:
    ├── id: str                    # Unique identifier
    ├── name: str                  # Pattern name
    ├── metadata: PatternMetadata
    │   ├── width: int             # LED matrix width
    │   ├── height: int            # LED matrix height
    │   ├── color_order: str       # RGB/GRB/etc
    │   ├── fps: float             # Frames per second
    │   ├── total_ms: int          # Total duration
    │   └── brightness: float       # Brightness level
    │
    └── frames: List[Frame]
        └── Frame:
            ├── pixels: List[Tuple[r,g,b]]  # RGB values per LED
            └── duration_ms: int             # Frame duration
```

## 📤 Export Flow

### **Export Paths from Different Tabs**

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    EXPORT OPTIONS                                        │
└─────────────────────────────────────────────────────────────────────────┘

USER ACTION: Export Pattern
         │
         ▼
┌─────────────────────────────────────────────────────────────────────────┐
│  ENTRY POINT 1: File > Save Project / Save Project As                   │
│  ─────────────────────────────────────────────────────────────────────  │
│  function: save_project() or save_project_as()                           │
│                                                                           │
│  ┌──────────────────────────────────────────────────────────────────┐   │
│  │ Pattern.save_to_file(file_path)                                 │   │
│  │                                                                   │   │
│  │ Format: .ledproj (JSON-based)                                     │   │
│  │ Contains:                                                         │   │
│  │ • Pattern metadata (width, height, fps, etc.)                     │   │
│  │ • All frame data (pixels + durations)                            │   │
│  │ • Pattern name and ID                                            │   │
│  │                                                                   │   │
│  │ Output: Complete project file that can be reopened later         │   │
│  └──────────────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────────┘
         │
         ▼
┌─────────────────────────────────────────────────────────────────────────┐
│  ENTRY POINT 2: Preview Tab Export                                      │
│  ─────────────────────────────────────────────────────────────────────  │
│  User can export from Preview Tab via:                                  │
│  • File menu > Export                                                    │
│  • Export button (if available in Preview Tab)                           │
│                                                                           │
│  Format Options:                                                          │
│  • .bin - Binary format                                                  │
│  • .hex - Intel HEX format                                               │
│  • .leds - LEDS format                                                   │
│  • .ledproj - Project format                                             │
│  • .json - JSON format                                                   │
└─────────────────────────────────────────────────────────────────────────┘
         │
         ▼
┌─────────────────────────────────────────────────────────────────────────┐
│  ENTRY POINT 3: Flash Tab (Firmware Generation)                        │
│  ─────────────────────────────────────────────────────────────────────  │
│  User clicks "Build & Flash"                                             │
│                                                                           │
│  ┌──────────────────────────────────────────────────────────────────┐   │
│  │ Firmware Generation Process:                                     │   │
│  │                                                                   │   │
│  │ 1. FirmwareBuilder.build_firmware(pattern, chip_id, config)     │   │
│  │    ↓                                                               │   │
│  │ 2. Select firmware template for chip                              │   │
│  │    ↓                                                               │   │
│  │ 3. Generate pattern_data.h                                        │   │
│  │    • Embeds pattern data as C array                               │   │
│  │    • Includes metadata                                            │   │
│  │    ↓                                                               │   │
│  │ 4. Compile firmware                                               │   │
│  │    • Uses Arduino CLI (ESP chips)                                │   │
│  │    • Uses GCC toolchain (AVR/STM32/PIC)                          │   │
│  │    ↓                                                               │   │
│  │ 5. Generate firmware binary                                       │   │
│  │    • .bin file (ESP8266/ESP32)                                   │   │
│  │    • .hex file (AVR/STM32)                                       │   │
│  │                                                                   │   │
│  │ Output: Compiled firmware with embedded pattern                  │   │
│  └──────────────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────────┘
         │
         ▼
┌─────────────────────────────────────────────────────────────────────────┐
│  ENTRY POINT 4: WiFi Upload Tab (Pattern Upload)                       │
│  ─────────────────────────────────────────────────────────────────────  │
│  User clicks "Upload Pattern"                                           │
│                                                                           │
│  ┌──────────────────────────────────────────────────────────────────┐   │
│  │ WiFi Upload Process:                                              │   │
│  │                                                                   │   │
│  │ 1. Convert pattern to upload format                               │   │
│  │    • Serialize pattern data                                       │   │
│  │    ↓                                                               │   │
│  │ 2. HTTP POST to ESP device                                        │   │
│  │    • POST /api/upload                                             │   │
│  │    • Sends pattern file                                           │   │
│  │    ↓                                                               │   │
│  │ 3. ESP device stores pattern                                      │   │
│  │    • Saves to flash memory                                        │   │
│  │    • Ready for playback                                           │   │
│  │                                                                   │   │
│  │ Output: Pattern stored on ESP device (wireless export)           │   │
│  └──────────────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────────┘
```

## 🔄 Complete Flow: Open → Edit → Export

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    COMPLETE FLOW OVERVIEW                               │
└─────────────────────────────────────────────────────────────────────────┘

1️⃣ FILE OPEN
   │
   ├─→ Media File (.mp4/.jpg/.gif)
   │   ↓
   │   Convert to Pattern
   │   ↓
   │   Pattern Object Created
   │   ↓
   │   └─→ SYNC to all 3 tabs
   │
   ├─→ Pattern File (.bin/.hex/.dat/.leds)
   │   ↓
   │   Parse & Auto-detect dimensions
   │   ↓
   │   Pattern Object Created
   │   ↓
   │   └─→ SYNC to all 3 tabs
   │
   └─→ Project File (.ledproj)
       ↓
       Load from JSON
       ↓
       Pattern Object Created
       ↓
       └─→ SYNC to all 3 tabs

2️⃣ TAB SYNCHRONIZATION (Automatic)
   │
   ├─→ Preview Tab
   │   • Pattern loaded
   │   • Preview active
   │   • Controls enabled
   │
   ├─→ Flash Tab
   │   • Pattern loaded
   │   • Ready for flashing
   │   • Build button enabled
   │
   └─→ WiFi Upload Tab
       • Pattern loaded
       • Ready for upload
       • Upload button enabled

3️⃣ EDITING (Optional - in Preview Tab)
   │
   ├─→ Adjust brightness
   │   • Changes apply to pattern object
   │   • Pattern modified flag set
   │
   ├─→ Adjust speed/FPS
   │   • Changes apply to pattern object
   │   • Pattern modified flag set
   │
   └─→ Other modifications
       • Changes apply to pattern object
       • Pattern modified flag set

4️⃣ EXPORT OPTIONS
   │
   ├─→ Save Project (.ledproj)
   │   • File > Save Project
   │   • Saves complete pattern with all edits
   │   • Can reopen later
   │
   ├─→ Export Pattern File
   │   • Preview Tab > Export
   │   • Formats: .bin, .hex, .leds, .json
   │   • Exports current pattern state
   │
   ├─→ Flash to Device (USB)
   │   • Flash Tab > Build & Flash
   │   • Generates firmware with embedded pattern
   │   • Uploads to microcontroller
   │
   └─→ Upload via WiFi
       • WiFi Upload Tab > Upload Pattern
       • Sends pattern to ESP device
       • Stores on device flash
```

## 🎯 Key Synchronization Points

### **1. Pattern Object Reference**
All tabs share the **same Pattern object** stored in `MainWindow.pattern`. Changes in one tab can affect others if the pattern is modified.

### **2. Real-time Updates**
When pattern is loaded:
- **Preview Tab**: Immediately shows visual preview
- **Flash Tab**: Immediately shows pattern info and enables flash
- **WiFi Upload Tab**: Immediately shows pattern ready for upload

### **3. State Consistency**
- All tabs know about the current pattern
- All tabs can access pattern metadata and frames
- Window title reflects current pattern name
- Status bar shows pattern loading status

### **4. Export Consistency**
All export methods use the **same Pattern object**:
- `save_project()` → Uses `self.pattern`
- `export_binary()` → Uses `self.pattern`
- Firmware build → Uses `self.pattern`
- WiFi upload → Uses `self.pattern`

## 📊 Tab Communication Signals

```
MediaUploadTab
    │
    └─→ pattern_loaded Signal
            │
            └─→ MainWindow.load_pattern_from_media()
                    │
                    └─→ load_pattern_to_all_tabs()
                            │
                            ├─→ PreviewTab.load_pattern()
                            ├─→ FlashTab.load_pattern()
                            └─→ WiFiUploadTab.set_pattern()

PreviewTab
    │
    └─→ pattern_modified Signal
            │
            └─→ MainWindow.on_pattern_modified()
                    │
                    └─→ Updates self.pattern
                          (Other tabs can see changes)

FlashTab
    │
    └─→ flash_complete Signal
            │
            └─→ MainWindow.on_flash_complete()
                    │
                    └─→ Updates status bar
```

## 🔑 Important Notes

1. **Single Source of Truth**: `MainWindow.pattern` is the single source of truth for the current pattern

2. **Automatic Synchronization**: When a file is opened, `load_pattern_to_all_tabs()` automatically distributes it to all tabs

3. **No Manual Sync Needed**: Users don't need to manually sync - it happens automatically on file open

4. **Export Uses Current State**: All export operations use `self.pattern`, which reflects any edits made

5. **Tab Independence**: Each tab maintains its own UI state, but shares the pattern data

6. **Pattern Modification**: If a tab modifies the pattern (e.g., brightness in Preview), it modifies `self.pattern`, which affects all tabs

---

## 🔔 Event-Driven Communication

### **Signal Flow & Event Sequence**

The application uses PySide6's Signal/Slot mechanism for event-driven communication. Below is a complete event sequence diagram:

```
┌─────────────────────────────────────────────────────────────────────┐
│                    COMPLETE EVENT SEQUENCE                          │
└─────────────────────────────────────────────────────────────────────┘

FILE OPEN FLOW EVENTS:

1. User Action: File > Open
   └─→ Event: file_open_requested (implicit)
       └─→ Handler: MainWindow.open_pattern()

2. File Selected
   └─→ Event: file_selected (implicit)
       └─→ Status Bar: "Loading [filename]..."

3. Pattern Created
   └─→ Event: pattern_created (implicit)
       ├─→ Status Bar: "Loaded: X LEDs, Y frames"
       └─→ Trigger: load_pattern_to_all_tabs()

4. Tab Synchronization
   └─→ Event: sync_initiated (implicit)
       ├─→ preview_tab.load_pattern() emits: (internal)
       │   └─→ preview_updated (internal tab event)
       ├─→ flash_tab.load_pattern() emits: (internal)
       │   └─→ flash_ready (internal tab event)
       └─→ wifi_upload_tab.set_pattern() emits: (internal)
           └─→ upload_ready (internal tab event)

5. Synchronization Complete
   └─→ Event: all_tabs_synced (implicit)
       ├─→ UI: Switch to Preview tab
       ├─→ Window Title: "Upload Bridge - [filename]"
       └─→ Dialog: Show success message


MEDIA CONVERSION FLOW EVENTS:

1. MediaUploadTab: User converts media
   └─→ Signal: MediaUploadTab.pattern_loaded
       └─→ Handler: MainWindow.load_pattern_from_media()
           └─→ Calls: load_pattern_to_all_tabs()
               └─→ All tabs updated


PATTERN MODIFICATION EVENTS:

1. PreviewTab: User edits pattern (brightness/speed)
   └─→ Signal: PreviewTab.pattern_modified
       └─→ Handler: MainWindow.on_pattern_modified()
           ├─→ Updates: self.pattern (shared reference)
           └─→ Sets: self.is_dirty = True


EXPORT EVENTS:

1. File > Save Project
   └─→ Event: save_requested (implicit)
       └─→ Handler: MainWindow.save_project()
           ├─→ Pattern.save_to_file()
           └─→ Event: save_complete (implicit)
               └─→ self.is_dirty = False

2. FlashTab: Build & Flash
   └─→ Signal: FlashTab.flash_complete(bool, str)
       └─→ Handler: MainWindow.on_flash_complete()
           ├─→ Status Bar: Success/Failure message
           └─→ Event: flash_complete (implicit)
```

### **Key Signals Defined**

| Signal | Source | Arguments | Destination | Purpose |
|--------|--------|-----------|-------------|---------|
| `pattern_loaded` | MediaUploadTab | `Pattern` | MainWindow | Pattern converted from media |
| `pattern_modified` | PreviewTab | - | MainWindow | Pattern edited in Preview tab |
| `flash_complete` | FlashTab | `bool, str` | MainWindow | Flash operation completed |
| `upload_complete` | WiFiUploadTab | `bool, str` | MainWindow | WiFi upload completed |

### **Event Listeners**

Each tab listens to pattern changes through the shared `MainWindow.pattern` reference:

- **PreviewTab**: Direct access to `self.pattern` (passed via `load_pattern()`)
- **FlashTab**: Direct access to `self.pattern` (passed via `load_pattern()`)
- **WiFiUploadTab**: Direct access to `self.pattern` (passed via `set_pattern()`)

---

## ⚠️ Edge Cases & Error Handling

### **Edge Case 1: Tab Closed/Reloaded Mid-Sync**

**Scenario**: User closes a tab or application crashes during synchronization.

**Current Behavior**:
- Pattern is stored in `MainWindow.pattern` before tab synchronization
- If a tab fails to load, `MainWindow.pattern` remains valid
- Other tabs that successfully loaded will continue to work
- Failed tab can be reinitialized by calling `load_pattern()` again

**Recovery**:
```python
# If PreviewTab fails:
try:
    self.preview_tab.load_pattern(pattern)
except Exception as e:
    # Log error, but continue with other tabs
    print(f"Preview tab failed: {e}")
    # Pattern still available in MainWindow.pattern
```

**Recommendation**: Add try-except around each tab's `load_pattern()` call to ensure partial failures don't break the entire flow.

---

### **Edge Case 2: WiFi Tab Fails to Load Pattern**

**Scenario**: WiFi Upload tab fails to set pattern (network error, UI initialization issue).

**Current Behavior**:
- `MainWindow.pattern` is unaffected
- Preview and Flash tabs continue to work normally
- WiFi Upload tab may show empty/disabled state
- User can retry by manually calling the upload operation

**Impact**: Low - WiFi upload is optional and doesn't block other operations.

---

### **Edge Case 3: Pattern Modified During Flash Operation**

**Scenario**: User edits pattern in Preview tab while Flash tab is building firmware.

**Current Behavior**:
- Flash tab receives pattern reference at start of operation
- Flash tab caches pattern data during build process
- Changes in Preview tab modify `self.pattern`, but flash uses cached data
- Result: Flash completes with original pattern, not modified version

**Recommendation**: 
- Consider locking pattern during flash operations
- Or show warning: "Pattern modified during flash - using original version"
- Or use pattern copy instead of reference for flash operation

---

### **Edge Case 4: Multiple Files Opened Rapidly**

**Scenario**: User clicks "Open" multiple times before first file finishes loading.

**Current Behavior**:
- Each file dialog opens independently
- First load completes, then second load starts
- Previous pattern is replaced by new pattern
- No queuing or cancellation mechanism

**Impact**: Medium - User may lose previous pattern if they accidentally open another file.

**Recommendation**: 
- Disable "Open" button during file loading
- Show "Loading..." indicator
- Optionally: Show confirmation if pattern is modified

---

### **Edge Case 5: Large Pattern Files (>50MB)**

**Scenario**: Very large pattern files (thousands of frames, high resolution).

**Current Behavior**:
- Pattern is loaded entirely into memory
- All tabs receive the full pattern object
- UI may freeze during loading
- Memory usage increases significantly

**Impact**: High - Can cause memory issues on low-end systems.

**Recommendation**:
- Add file size warning for patterns >10MB
- Consider lazy loading for preview tab
- Implement progress indicator for large files

---

### **Edge Case 6: Corrupted Pattern File**

**Scenario**: Pattern file exists but contains invalid data or is corrupted.

**Current Behavior**:
- Parser attempts to read file
- If parsing fails, error dialog shown
- `MainWindow.pattern` remains as previous pattern (if any)
- Status bar shows "Load failed"

**Recovery**:
```python
try:
    pattern = parse_pattern_file(file_path)
except Exception as e:
    QMessageBox.critical(self, "Load Error", str(e))
    # Previous pattern remains in self.pattern
    return
```

---

### **Edge Case 7: Media Conversion Failure**

**Scenario**: Media file is corrupted, unsupported format, or conversion library fails.

**Current Behavior**:
- MediaConverter attempts conversion
- On failure: Error dialog shown
- `MainWindow.pattern` remains as previous pattern (if any)
- Status bar shows conversion error

**Impact**: Medium - User needs to select different file or fix media file.

---

### **Edge Case 8: Tab Not Initialized**

**Scenario**: Pattern loaded before all tabs are fully initialized (rare timing issue).

**Current Behavior**:
- `load_pattern_to_all_tabs()` is called after `setup_ui()`
- Tabs should be initialized before first file load
- If tab doesn't exist: AttributeError

**Prevention**: Ensure all tabs are created in `setup_ui()` before allowing file operations.

---

### **Error Handling Best Practices**

1. **Always wrap pattern loading in try-except**
2. **Log errors for debugging**
3. **Show user-friendly error messages**
4. **Preserve previous pattern state on failure**
5. **Update status bar with error information**
6. **Allow user to retry or select different file**

---

## 📚 Related Documentation

### **Core Documentation**

- **[USER_FLOWS.md](./USER_FLOWS.md)** - Complete user journey documentation
  - User workflows for all tabs
  - Step-by-step user guides
  - Common use cases and scenarios

- **[ARCHITECTURE_GUIDE.md](./ARCHITECTURE_GUIDE.md)** - System architecture
  - Component structure
  - Design patterns
  - Module relationships

### **Pattern Object Documentation**

- **Pattern Class** (`core/pattern.py`) - Pattern data structure
  - PatternMetadata schema
  - Frame structure
  - Serialization methods

- **Parser System** (`parsers/`) - File format parsing
  - Supported formats
  - Auto-detection algorithms
  - Parser registry

### **Media Conversion Documentation**

- **MediaConverter** (`core/media_converter.py`) - Media to pattern conversion
  - Supported formats
  - Conversion parameters
  - Frame extraction logic

### **Tab-Specific Documentation**

- **Preview Tab** (`ui/tabs/preview_tab.py`) - Pattern preview and editing
- **Flash Tab** (`ui/tabs/flash_tab.py`) - Firmware generation and upload
- **WiFi Upload Tab** (`ui/tabs/wifi_upload_tab.py`) - Wireless pattern upload
- **Media Upload Tab** (`ui/tabs/media_upload_tab.py`) - Media conversion UI

### **Development Resources**

- **Firmware Templates** (`firmware/templates/`) - Device-specific firmware
- **Uploaders** (`uploaders/`) - Hardware upload implementations
- **Config** (`config/`) - Application configuration and chip database

### **Quick Links**

- [Project Overview](./PROJECT_OVERVIEW.md)
- [Installation Guide](./INSTALLER_README.md)
- [Troubleshooting](./TROUBLESHOOTING_GUIDE.md)
- [Developer Quick Reference](./DEVELOPER_QUICK_REF.md)

---

**Document Version History:**
- **v1.0** (2025-10-29): Initial version - Complete flow documentation
- **v1.1** (2025-10-29): Added event-driven notes, state machine, edge cases, related docs

---

**End of File Open → Export Flow Documentation**

