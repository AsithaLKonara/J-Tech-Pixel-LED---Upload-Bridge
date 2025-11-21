# Feature Linkage Diagram & Architecture

**Complete Visual Guide to Feature Interconnections**

---

## 🎯 Overview

This document provides a comprehensive visual diagram of all features in Upload Bridge and how they should be linked together. It shows current connections and recommended improvements for better feature integration.

---

## 📊 Complete Feature Linkage Diagram

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                          UPLOAD BRIDGE APPLICATION                          │
│                              MainWindow (Hub)                                │
└─────────────────────────────────────────────────────────────────────────────┘
                                    │
                    ┌───────────────┼───────────────┐
                    │               │               │
                    ▼               ▼               ▼
        ┌───────────────────┐  ┌──────────┐  ┌──────────────┐
        │  Pattern State    │  │ Settings │  │ Status Bar   │
        │  (Single Source)  │  │ (QSettings)│ │ (Feedback)   │
        └───────────────────┘  └──────────┘  └──────────────┘
                    │
        ┌───────────┼───────────┐
        │           │           │
        ▼           ▼           ▼
┌─────────────┐ ┌─────────────┐ ┌─────────────┐
│ Pattern     │ │ File Path   │ │ Dirty Flag  │
│ Object      │ │ (current)   │ │ (is_dirty)  │
└─────────────┘ └─────────────┘ └─────────────┘


═══════════════════════════════════════════════════════════════════════════════
                            TAB FEATURES (9 Tabs)
═══════════════════════════════════════════════════════════════════════════════

┌─────────────────────────────────────────────────────────────────────────────┐
│ 1. 🎬 MEDIA UPLOAD TAB                                                      │
│    ──────────────────────────────────────────────────────────────────────── │
│    Purpose: Import images/GIFs → Convert to LED patterns                   │
│    ──────────────────────────────────────────────────────────────────────── │
│                                                                             │
│    Input: Image/GIF files                                                  │
│    Output: Pattern object                                                  │
│                                                                             │
│    Signals:                                                                │
│    ├─→ pattern_loaded(Pattern) ──┐                                        │
│    │                              │                                        │
│    └──────────────────────────────┼──→ MainWindow.load_pattern_from_media()│
│                                    │         │                              │
│                                    │         └─→ load_pattern_to_all_tabs() │
│                                    │                                        │
│    Should Also Link:                                                       │
│    ├─→ DesignToolsTab (for editing imported pattern)                      │
│    ├─→ PatternLibraryTab (auto-add to library?)                           │
│    └─→ PreviewTab (immediate preview)                                      │
└─────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────┐
│ 2. 🎨 DESIGN TOOLS TAB                                                      │
│    ──────────────────────────────────────────────────────────────────────── │
│    Purpose: Create/edit patterns with layers, frames, automation           │
│    ──────────────────────────────────────────────────────────────────────── │
│                                                                             │
│    Core Components:                                                        │
│    ├─→ Canvas (MatrixDesignCanvas)                                         │
│    ├─→ Timeline (TimelineWidget)                                           │
│    ├─→ Layer Panel (LayerPanelWidget)                                      │
│    ├─→ Frame Manager (FrameManager)                                        │
│    ├─→ Layer Manager (LayerManager)                                        │
│    ├─→ Automation Queue (AutomationQueueManager)                           │
│    └─→ History Manager (HistoryManager)                                    │
│                                                                             │
│    Signals:                                                                │
│    ├─→ pattern_modified() ──┐                                             │
│    ├─→ pattern_created(Pattern) ──┐                                       │
│    │                              │                                        │
│    └──────────────────────────────┼──→ MainWindow.on_pattern_modified()    │
│                                    │         │                              │
│                                    │         ├─→ Update MainWindow.pattern │
│                                    │         ├─→ Set is_dirty = True       │
│                                    │         └─→ Enable save button        │
│                                    │                                        │
│    Internal Signals:                                                       │
│    ├─→ FrameManager.frames_changed ──→ Timeline refresh                    │
│    ├─→ LayerManager.layers_changed ──→ Layer panel refresh                │
│    ├─→ Canvas.pixel_updated ──→ LayerManager.apply_pixel()                 │
│    └─→ Timeline.frameSelected ──→ FrameManager.select()                     │
│                                                                             │
│    Should Also Link:                                                       │
│    ├─→ PreviewTab (live preview while editing)                            │
│    ├─→ PatternLibraryTab (save to library)                                │
│    ├─→ FlashTab (direct flash from design)                                │
│    ├─→ WiFiUploadTab (direct upload from design)                          │
│    └─→ AudioReactiveTab (use as base for audio effects)                   │
└─────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────┐
│ 3. 👁️ PREVIEW TAB                                                           │
│    ──────────────────────────────────────────────────────────────────────── │
│    Purpose: Preview patterns with LED simulator                            │
│    ──────────────────────────────────────────────────────────────────────── │
│                                                                             │
│    Components:                                                              │
│    ├─→ LED Simulator (EnhancedLEDSimulatorWidget)                          │
│    ├─→ Playback Controls                                                   │
│    └─→ Pattern Info Display                                                │
│                                                                             │
│    Signals:                                                                │
│    ├─→ pattern_modified() ──┐                                             │
│    │                         │                                             │
│    └─────────────────────────┼──→ MainWindow.on_pattern_modified()        │
│                              │         │                                    │
│                              │         └─→ Update MainWindow.pattern        │
│                              │                                              │
│    Should Also Link:                                                       │
│    ├─→ DesignToolsTab (sync playback state)                                │
│    ├─→ FlashTab (preview before flash)                                    │
│    └─→ WiFiUploadTab (preview before upload)                              │
└─────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────┐
│ 4. ⚡ FLASH TAB                                                              │
│    ──────────────────────────────────────────────────────────────────────── │
│    Purpose: Build firmware & flash to hardware                             │
│    ──────────────────────────────────────────────────────────────────────── │
│                                                                             │
│    Components:                                                              │
│    ├─→ Chip Selection                                                      │
│    ├─→ GPIO Configuration                                                  │
│    ├─→ Firmware Builder                                                    │
│    └─→ Upload Manager                                                      │
│                                                                             │
│    Signals:                                                                │
│    ├─→ flash_complete(bool, str) ──┐                                      │
│    │                                 │                                      │
│    └─────────────────────────────────┼──→ MainWindow.on_flash_complete()   │
│                                       │         │                            │
│                                       │         └─→ Update status bar       │
│                                       │                                      │
│    Should Also Link:                                                          │
│    ├─→ PreviewTab (verify pattern before flash)                           │
│    ├─→ DesignToolsTab (flash directly from design)                        │
│    ├─→ BatchFlashTab (use same firmware build)                            │
│    └─→ PatternLibraryTab (save flashed pattern)                             │
└─────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────┐
│ 5. 🚀 BATCH FLASH TAB                                                        │
│    ──────────────────────────────────────────────────────────────────────── │
│    Purpose: Flash multiple devices simultaneously                          │
│    ──────────────────────────────────────────────────────────────────────── │
│                                                                             │
│    Components:                                                              │
│    ├─→ Port Selection (multi-select)                                       │
│    ├─→ Chip Configuration                                                  │
│    └─→ Batch Upload Manager                                                │
│                                                                             │
│    Signals:                                                                │
│    ├─→ batch_flash_complete(dict) ──┐  [MISSING - Should Add]             │
│    │                                 │                                      │
│    └─────────────────────────────────┼──→ MainWindow.on_batch_flash_complete│
│                                       │         │                            │
│                                       │         └─→ Show summary dialog     │
│                                       │                                      │
│    Should Also Link:                                                       │
│    ├─→ FlashTab (reuse firmware builder)                                  │
│    ├─→ PreviewTab (verify before batch flash)                             │
│    └─→ PatternLibraryTab (save batch configuration)                        │
└─────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────┐
│ 6. 📚 PATTERN LIBRARY TAB                                                    │
│    ──────────────────────────────────────────────────────────────────────── │
│    Purpose: Manage local pattern library                                   │
│    ──────────────────────────────────────────────────────────────────────── │
│                                                                             │
│    Components:                                                              │
│    ├─→ Pattern List (searchable)                                          │
│    ├─→ Pattern Metadata Display                                            │
│    └─→ Library Manager (PatternLibrary)                                   │
│                                                                             │
│    Signals:                                                                │
│    ├─→ pattern_selected(Pattern, str) ──┐                                 │
│    │                                      │                                 │
│    └──────────────────────────────────────┼──→ MainWindow.on_pattern_library│
│                                            │         │                        │
│                                            │         └─→ load_pattern_to_all │
│                                            │                                  │
│    Should Also Link:                                                       │
│    ├─→ DesignToolsTab (load for editing)                                  │
│    ├─→ PreviewTab (quick preview)                                         │
│    ├─→ FlashTab (flash from library)                                      │
│    ├─→ WiFiUploadTab (upload from library)                                │
│    └─→ MediaUploadTab (auto-add imported patterns)                         │
└─────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────┐
│ 7. 🎵 AUDIO REACTIVE TAB                                                     │
│    ──────────────────────────────────────────────────────────────────────── │
│    Purpose: Generate patterns from audio input                             │
│    ──────────────────────────────────────────────────────────────────────── │
│                                                                             │
│    Components:                                                              │
│    ├─→ Audio Input Device Selection                                        │
│    ├─→ FFT Analyzer                                                        │
│    ├─→ Pattern Generator (AudioReactiveGenerator)                          │
│    └─→ Real-time Visualization                                             │
│                                                                             │
│    Signals:                                                                │
│    ├─→ pattern_generated(Pattern) ──┐                                     │
│    │                                 │                                      │
│    └─────────────────────────────────┼──→ MainWindow.on_audio_pattern_gen  │
│                                       │         │                            │
│                                       │         └─→ load_pattern_to_all_tabs│
│                                       │                                      │
│    Should Also Link:                                                       │
│    ├─→ DesignToolsTab (edit generated pattern)                            │
│    ├─→ PreviewTab (live preview while generating)                          │
│    ├─→ PatternLibraryTab (save generated patterns)                         │
│    └─→ FlashTab (flash audio-reactive pattern)                             │
└─────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────┐
│ 8. 📡 WIFI UPLOAD TAB                                                        │
│    ──────────────────────────────────────────────────────────────────────── │
│    Purpose: Upload patterns/firmware over WiFi (ESP8266/ESP32)            │
│    ──────────────────────────────────────────────────────────────────────── │
│                                                                             │
│    Components:                                                              │
│    ├─→ Device Discovery                                                    │
│    ├─→ Pattern Upload                                                      │
│    ├─→ OTA Firmware Update                                                 │
│    ├─→ Brightness Control                                                  │
│    ├─→ Pattern Scheduling                                                  │
│    └─→ Multi-Device Sync                                                   │
│                                                                             │
│    Signals:                                                                │
│    ├─→ upload_complete(bool, str) ──┐  [MISSING - Should Add]             │
│    │                                 │                                      │
│    └─────────────────────────────────┼──→ MainWindow.on_wifi_upload_complete│
│                                       │         │                            │
│                                       │         └─→ Update status bar       │
│                                       │                                      │
│    Should Also Link:                                                       │
│    ├─→ PreviewTab (preview before upload)                                 │
│    ├─→ DesignToolsTab (upload directly from design)                       │
│    ├─→ PatternLibraryTab (upload from library)                             │
│    └─→ FlashTab (sync firmware version)                                    │
└─────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────┐
│ 9. 🔧 ARDUINO IDE TAB                                                        │
│    ──────────────────────────────────────────────────────────────────────── │
│    Purpose: Generate Arduino code from patterns                            │
│    ──────────────────────────────────────────────────────────────────────── │
│                                                                             │
│    Components:                                                              │
│    ├─→ Code Generator                                                       │
│    ├─→ Template Selection                                                  │
│    └─→ Export Manager                                                       │
│                                                                             │
│    Signals:                                                                │
│    ├─→ code_generated(str, str) ──┐  [MISSING - Should Add]               │
│    │                               │                                        │
│    └───────────────────────────────┼──→ MainWindow.on_code_generated()     │
│                                     │         │                              │
│                                     │         └─→ Open in Arduino IDE?      │
│                                     │                                        │
│    Should Also Link:                                                       │
│    ├─→ DesignToolsTab (export design as code)                             │
│    ├─→ PreviewTab (preview before export)                                 │
│    └─→ PatternLibraryTab (save code templates)                            │
└─────────────────────────────────────────────────────────────────────────────┘

```

---

## 🔗 Current Signal Connections

### ✅ Currently Connected

```
MainWindow (Hub)
│
├─→ MediaUploadTab.pattern_loaded
│   └─→ MainWindow.load_pattern_from_media()
│       └─→ load_pattern_to_all_tabs()
│
├─→ DesignToolsTab.pattern_modified
│   └─→ MainWindow.on_pattern_modified()
│       └─→ Updates MainWindow.pattern, is_dirty
│
├─→ DesignToolsTab.pattern_created
│   └─→ MainWindow._on_design_pattern_created()
│
├─→ PreviewTab.pattern_modified
│   └─→ MainWindow.on_pattern_modified()
│
├─→ FlashTab.flash_complete
│   └─→ MainWindow.on_flash_complete()
│
├─→ PatternLibraryTab.pattern_selected
│   └─→ MainWindow.on_pattern_library_selected()
│       └─→ load_pattern_to_all_tabs()
│
└─→ AudioReactiveTab.pattern_generated
    └─→ MainWindow.on_audio_pattern_generated()
        └─→ load_pattern_to_all_tabs()
```

---

## 🚨 Missing Connections (Should Be Added)

### 1. **Cross-Tab Pattern Synchronization**

```
┌─────────────────────────────────────────────────────────────┐
│ MISSING: Real-time Pattern Sync                             │
│                                                             │
│ When DesignToolsTab modifies pattern:                       │
│   └─→ Should notify PreviewTab (live preview update)       │
│   └─→ Should notify FlashTab (update firmware preview)     │
│   └─→ Should notify WiFiUploadTab (update upload preview)  │
│                                                             │
│ Current: Only MainWindow.pattern is updated                │
│ Problem: Tabs don't know when pattern changes               │
│ Solution: Add pattern_changed signal to MainWindow         │
└─────────────────────────────────────────────────────────────┘
```

### 2. **Batch Flash Tab Signals**

```
┌─────────────────────────────────────────────────────────────┐
│ MISSING: BatchFlashTab.flash_complete                      │
│                                                             │
│ Should emit:                                                │
│   batch_flash_complete(dict)                                │
│     - dict contains: {port: (success, message), ...}       │
│                                                             │
│ Listener: MainWindow.on_batch_flash_complete()             │
│   └─→ Show summary dialog with results                     │
└─────────────────────────────────────────────────────────────┘
```

### 3. **WiFi Upload Tab Signals**

```
┌─────────────────────────────────────────────────────────────┐
│ MISSING: WiFiUploadTab.upload_complete                     │
│                                                             │
│ Should emit:                                                │
│   upload_complete(bool success, str message)               │
│   brightness_changed(int value)                            │
│   schedule_updated(dict schedule)                          │
│                                                             │
│ Listeners:                                                  │
│   └─→ MainWindow.on_wifi_upload_complete()                 │
│   └─→ Status bar updates                                   │
└─────────────────────────────────────────────────────────────┘
```

### 4. **Arduino IDE Tab Signals**

```
┌─────────────────────────────────────────────────────────────┐
│ MISSING: ArduinoIDETab.code_generated                     │
│                                                             │
│ Should emit:                                                │
│   code_generated(str code, str file_path)                  │
│                                                             │
│ Listener: MainWindow.on_code_generated()                   │
│   └─→ Optionally open in Arduino IDE                       │
└─────────────────────────────────────────────────────────────┘
```

### 5. **Pattern Library Auto-Add**

```
┌─────────────────────────────────────────────────────────────┐
│ MISSING: Auto-add to library                               │
│                                                             │
│ When pattern is created/imported:                           │
│   └─→ Should offer to add to PatternLibraryTab             │
│                                                             │
│ Triggers:                                                   │
│   - MediaUploadTab.pattern_loaded                           │
│   - AudioReactiveTab.pattern_generated                      │
│   - DesignToolsTab.pattern_created                          │
└─────────────────────────────────────────────────────────────┘
```

---

## 🎯 Recommended Feature Linkages

### **Linkage Group 1: Pattern Creation Flow**

```
MediaUploadTab
    │ pattern_loaded
    ▼
MainWindow.load_pattern_from_media()
    │
    ├─→ load_pattern_to_all_tabs()
    │   ├─→ PreviewTab.load_pattern()        ✅ Current
    │   ├─→ FlashTab.load_pattern()          ✅ Current
    │   ├─→ WiFiUploadTab.set_pattern()      ✅ Current
    │   │
    │   └─→ [SHOULD ADD]
    │       ├─→ DesignToolsTab.load_pattern()  ❌ Missing
    │       ├─→ PatternLibraryTab.offer_add()   ❌ Missing
    │       └─→ BatchFlashTab.set_pattern()    ❌ Missing
    │
    └─→ [SHOULD ADD]
        └─→ Show notification: "Pattern loaded. Add to library?"
```

### **Linkage Group 2: Design → Preview → Flash Flow**

```
DesignToolsTab
    │ User paints/edits
    ▼
pattern_modified.emit()
    │
    ├─→ MainWindow.on_pattern_modified()     ✅ Current
    │   └─→ Updates MainWindow.pattern
    │
    └─→ [SHOULD ADD]
        ├─→ PreviewTab.update_pattern()      ❌ Missing (live preview)
        ├─→ FlashTab.refresh_preview()       ❌ Missing
        └─→ WiFiUploadTab.refresh_preview()  ❌ Missing
```

### **Linkage Group 3: Library → All Tabs Flow**

```
PatternLibraryTab
    │ User selects pattern
    ▼
pattern_selected.emit(Pattern, file_path)
    │
    └─→ MainWindow.on_pattern_library_selected()  ✅ Current
        └─→ load_pattern_to_all_tabs()
            │
            └─→ [SHOULD ADD]
                ├─→ DesignToolsTab.load_pattern()  ❌ Missing
                └─→ All tabs get pattern            ✅ Current
```

### **Linkage Group 4: Audio → Design → Export Flow**

```
AudioReactiveTab
    │ Generate pattern
    ▼
pattern_generated.emit(Pattern)
    │
    └─→ MainWindow.on_audio_pattern_generated()  ✅ Current
        └─→ load_pattern_to_all_tabs()
            │
            └─→ [SHOULD ADD]
                ├─→ DesignToolsTab.load_pattern()  ❌ Missing
                └─→ Offer: "Edit in Design Tools?"
```

### **Linkage Group 5: Flash Coordination**

```
FlashTab
    │ Build firmware
    ▼
[SHOULD ADD]
    │
    ├─→ firmware_building.emit()  ❌ Missing
    │   └─→ MainWindow.show_progress("Building firmware...")
    │
    ├─→ firmware_built.emit(str path)  ❌ Missing
    │   └─→ BatchFlashTab.use_firmware(path)  ❌ Missing
    │
    └─→ flash_complete.emit(bool, str)  ✅ Current
        └─→ MainWindow.on_flash_complete()
```

### **Linkage Group 6: WiFi Upload Coordination**

```
WiFiUploadTab
    │ Upload pattern
    ▼
[SHOULD ADD]
    │
    ├─→ upload_started.emit()  ❌ Missing
    │   └─→ MainWindow.show_progress("Uploading...")
    │
    ├─→ upload_progress.emit(int percent)  ❌ Missing
    │   └─→ MainWindow.update_progress(percent)
    │
    └─→ upload_complete.emit(bool, str)  ❌ Missing
        └─→ MainWindow.on_wifi_upload_complete()
            └─→ Show success/failure message
```

---

## 📐 Complete Signal Flow Diagram

```
┌─────────────────────────────────────────────────────────────────────────┐
│                        MAIN WINDOW (Signal Hub)                         │
│                                                                         │
│  pattern_changed(Pattern)  ←─── [SHOULD ADD]                           │
│       │                                                                 │
│       ├─→ PreviewTab.update_pattern()                                  │
│       ├─→ FlashTab.refresh_preview()                                    │
│       ├─→ WiFiUploadTab.refresh_preview()                               │
│       └─→ DesignToolsTab.sync_pattern()                                 │
│                                                                         │
│  save_state_changed(bool)  ←─── [SHOULD ADD]                           │
│       │                                                                 │
│       └─→ All tabs: Enable/disable save buttons                         │
└─────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────┐
│                    DESIGN TOOLS TAB SIGNALS                             │
│                                                                         │
│  pattern_modified() ──┐                                                │
│  pattern_created(Pattern) ──┐                                          │
│  frame_changed(int) ──┐     │                                          │
│  layer_changed(int) ──┐     │                                          │
│                       │     │                                          │
│                       └─────┼──→ MainWindow.pattern_changed()          │
│                             │         │                                 │
│                             │         └─→ Broadcast to all tabs        │
│                             │                                            │
│  [SHOULD ADD]                                                           │
│  export_requested(format) ──┐                                          │
│    └─→ MainWindow.handle_export()                                       │
│                                                                         │
│  preview_requested() ──┐                                                │
│    └─→ PreviewTab.show_detached_preview()                               │
└─────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────┐
│                    PREVIEW TAB SIGNALS                                  │
│                                                                         │
│  pattern_modified() ──┐                                                │
│    └─→ MainWindow.on_pattern_modified()                                 │
│                                                                         │
│  [SHOULD ADD]                                                           │
│  playback_state_changed(bool playing) ──┐                               │
│    └─→ DesignToolsTab.sync_playback_state()                             │
│                                                                         │
│  frame_changed(int) ──┐                                                 │
│    └─→ DesignToolsTab.sync_frame_selection()                            │
└─────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────┐
│                    FLASH TAB SIGNALS                                    │
│                                                                         │
│  flash_complete(bool, str) ──┐                                         │
│    └─→ MainWindow.on_flash_complete()                                   │
│                                                                         │
│  [SHOULD ADD]                                                           │
│  firmware_building() ──┐                                                │
│  firmware_built(str path) ──┐                                          │
│    └─→ BatchFlashTab.use_firmware(path)                                 │
│                                                                         │
│  flash_progress(int percent) ──┐                                        │
│    └─→ MainWindow.update_flash_progress()                                │
└─────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────┐
│                    BATCH FLASH TAB SIGNALS                              │
│                                                                         │
│  [SHOULD ADD]                                                           │
│  batch_flash_started(int count) ──┐                                    │
│  batch_flash_progress(int done, int total) ──┐                         │
│  batch_flash_complete(dict results) ──┐                                │
│    └─→ MainWindow.on_batch_flash_complete()                            │
│         └─→ Show summary dialog                                         │
└─────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────┐
│                    WIFI UPLOAD TAB SIGNALS                              │
│                                                                         │
│  [SHOULD ADD]                                                           │
│  upload_started() ──┐                                                   │
│  upload_progress(int percent) ──┐                                      │
│  upload_complete(bool, str) ──┐                                         │
│    └─→ MainWindow.on_wifi_upload_complete()                             │
│                                                                         │
│  brightness_changed(int value) ──┐                                      │
│    └─→ MainWindow.show_notification("Brightness: {value}")             │
│                                                                         │
│  schedule_updated(dict) ──┐                                            │
│    └─→ MainWindow.show_notification("Schedule updated")                 │
└─────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────┐
│                    PATTERN LIBRARY TAB SIGNALS                          │
│                                                                         │
│  pattern_selected(Pattern, str) ──┐                                     │
│    └─→ MainWindow.on_pattern_library_selected()                        │
│                                                                         │
│  [SHOULD ADD]                                                           │
│  pattern_added(Pattern) ──┐                                            │
│    └─→ MainWindow.show_notification("Added to library")                 │
│                                                                         │
│  pattern_removed(str pattern_id) ──┐                                   │
│    └─→ MainWindow.show_notification("Removed from library")             │
└─────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────┐
│                    AUDIO REACTIVE TAB SIGNALS                            │
│                                                                         │
│  pattern_generated(Pattern) ──┐                                        │
│    └─→ MainWindow.on_audio_pattern_generated()                         │
│                                                                         │
│  [SHOULD ADD]                                                           │
│  generation_started() ──┐                                               │
│  generation_progress(int percent) ──┐                                  │
│    └─→ MainWindow.update_progress()                                     │
└─────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────┐
│                    ARDUINO IDE TAB SIGNALS                              │
│                                                                         │
│  [SHOULD ADD]                                                           │
│  code_generated(str code, str path) ──┐                                │
│    └─→ MainWindow.on_code_generated()                                  │
│         └─→ Optionally open in Arduino IDE                             │
│                                                                         │
│  export_requested(format) ──┐                                          │
│    └─→ MainWindow.handle_export()                                       │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## 🔄 Data Flow Patterns

### **Pattern 1: Pattern Creation → Distribution**

```
Source Tab (Media/Design/Audio)
    │
    ├─→ Emit: pattern_loaded/created/generated
    │
    ▼
MainWindow Handler
    │
    ├─→ Store: MainWindow.pattern = pattern
    ├─→ Store: MainWindow.current_file = file_path
    ├─→ Set: MainWindow.is_dirty = False
    │
    ▼
load_pattern_to_all_tabs()
    │
    ├─→ PreviewTab.load_pattern(pattern)
    ├─→ FlashTab.load_pattern(pattern)
    ├─→ WiFiUploadTab.set_pattern(pattern)
    ├─→ DesignToolsTab.load_pattern(pattern)  [SHOULD ADD]
    ├─→ BatchFlashTab.set_pattern(pattern)    [SHOULD ADD]
    └─→ PatternLibraryTab.offer_add(pattern)  [SHOULD ADD]
```

### **Pattern 2: Pattern Modification → Sync**

```
DesignToolsTab / PreviewTab
    │ User edits pattern
    │
    ├─→ Modify: MainWindow.pattern (direct reference)
    ├─→ Emit: pattern_modified()
    │
    ▼
MainWindow.on_pattern_modified()
    │
    ├─→ Set: MainWindow.is_dirty = True
    ├─→ Enable: Save button
    │
    └─→ [SHOULD ADD]
        └─→ Emit: MainWindow.pattern_changed(pattern)
            │
            ├─→ PreviewTab.update_pattern(pattern)  [SHOULD ADD]
            ├─→ FlashTab.refresh_preview()         [SHOULD ADD]
            └─→ WiFiUploadTab.refresh_preview()    [SHOULD ADD]
```

### **Pattern 3: Tab Selection → Pattern Sync**

```
User clicks tab
    │
    ▼
MainWindow.on_tab_changed()
    │
    ├─→ Initialize tab (lazy loading)
    │
    └─→ [SHOULD ADD]
        └─→ If MainWindow.pattern exists:
            └─→ load_pattern_to_tab(tab_name, pattern)
                │
                └─→ Ensures all tabs have current pattern
```

---

## 🎯 Priority Linkage Recommendations

### **Priority 1: Critical Missing Links**

1. **MainWindow.pattern_changed Signal**
   - **Why**: Enables real-time sync across tabs
   - **Impact**: High - Users expect live updates
   - **Effort**: Low - Add signal, connect tabs

2. **DesignToolsTab → PreviewTab Live Preview**
   - **Why**: See changes immediately while editing
   - **Impact**: High - Major UX improvement
   - **Effort**: Medium - Requires debouncing/throttling

3. **PatternLibraryTab Auto-Add Option**
   - **Why**: Easy library management
   - **Impact**: Medium - Convenience feature
   - **Effort**: Low - Add dialog on pattern creation

### **Priority 2: Important Missing Links**

4. **FlashTab → BatchFlashTab Firmware Sharing**
   - **Why**: Reuse firmware builds
   - **Impact**: Medium - Performance improvement
   - **Effort**: Medium - Share firmware path

5. **WiFiUploadTab Progress Signals**
   - **Why**: User feedback during uploads
   - **Impact**: Medium - Better UX
   - **Effort**: Low - Add progress callbacks

6. **Cross-Tab Playback Sync**
   - **Why**: Preview and Design tabs should sync playback
   - **Impact**: Medium - Consistency
   - **Effort**: Medium - Add playback state signals

### **Priority 3: Nice-to-Have Links**

7. **Arduino IDE Tab Integration**
   - **Why**: Seamless code export workflow
   - **Impact**: Low - Niche feature
   - **Effort**: Low - Add signal

8. **Pattern Library Search Integration**
   - **Why**: Quick access from all tabs
   - **Impact**: Low - Convenience
   - **Effort**: Medium - Add search widget

---

## 📋 Implementation Checklist

### **Phase 1: Core Signal Infrastructure**

- [ ] Add `MainWindow.pattern_changed(Pattern)` signal
- [ ] Connect all tabs to `pattern_changed` signal
- [ ] Add `MainWindow.save_state_changed(bool)` signal
- [ ] Update `load_pattern_to_all_tabs()` to include all tabs

### **Phase 2: Missing Tab Signals**

- [ ] Add `BatchFlashTab.batch_flash_complete(dict)` signal
- [ ] Add `WiFiUploadTab.upload_complete(bool, str)` signal
- [ ] Add `WiFiUploadTab.upload_progress(int)` signal
- [ ] Add `ArduinoIDETab.code_generated(str, str)` signal

### **Phase 3: Cross-Tab Features**

- [ ] DesignToolsTab → PreviewTab live preview
- [ ] PreviewTab → DesignToolsTab playback sync
- [ ] FlashTab → BatchFlashTab firmware sharing
- [ ] PatternLibraryTab auto-add dialog

### **Phase 4: Advanced Integration**

- [ ] Cross-tab undo/redo coordination
- [ ] Shared clipboard for patterns
- [ ] Tab state persistence
- [ ] Multi-pattern workspace

---

## 🎨 Visual Feature Relationship Map

```
                    ┌─────────────────┐
                    │   MainWindow    │
                    │  (Central Hub)  │
                    └────────┬────────┘
                             │
        ┌────────────────────┼────────────────────┐
        │                    │                    │
        ▼                    ▼                    ▼
┌───────────────┐    ┌───────────────┐    ┌───────────────┐
│ Pattern State │    │ File Manager  │    │ Status Bar    │
│ (Single Truth)│    │ (I/O)         │    │ (Feedback)    │
└───────────────┘    └───────────────┘    └───────────────┘
        │                    │                    │
        └────────────────────┼────────────────────┘
                             │
        ┌────────────────────┼────────────────────┐
        │                    │                    │
        ▼                    ▼                    ▼
┌───────────────┐    ┌───────────────┐    ┌───────────────┐
│   Creation    │    │   Editing     │    │   Export      │
│   Tabs        │    │   Tabs        │    │   Tabs        │
├───────────────┤    ├───────────────┤    ├───────────────┤
│ Media Upload  │    │ Design Tools  │    │ Flash         │
│ Audio Reactive│    │ Preview       │    │ WiFi Upload   │
│ Pattern Lib   │    │               │    │ Arduino IDE   │
└───────────────┘    └───────────────┘    └───────────────┘
        │                    │                    │
        └────────────────────┼────────────────────┘
                             │
                    ┌────────┴────────┐
                    │  Pattern Object │
                    │  (Shared Data)  │
                    └─────────────────┘
```

---

## 🔧 How Features Should Link

### **1. Pattern Creation Chain**

```
MediaUploadTab / AudioReactiveTab
    │
    ├─→ Generate/Create Pattern
    │
    ▼
MainWindow.load_pattern_from_media/generated()
    │
    ├─→ Store in MainWindow.pattern
    ├─→ Distribute to all tabs
    │
    └─→ [SHOULD ADD]
        └─→ Show dialog: "Add to Pattern Library?"
            ├─→ Yes: PatternLibraryTab.add_pattern()
            └─→ No: Continue
```

### **2. Pattern Editing Chain**

```
DesignToolsTab
    │
    ├─→ User edits (paint, layers, frames)
    │
    ▼
pattern_modified.emit()
    │
    ├─→ MainWindow.on_pattern_modified()
    │   ├─→ Update MainWindow.pattern
    │   └─→ Set is_dirty = True
    │
    └─→ [SHOULD ADD]
        └─→ MainWindow.pattern_changed.emit(pattern)
            │
            ├─→ PreviewTab.update_pattern()  [Live preview]
            ├─→ FlashTab.refresh_preview()  [Update firmware preview]
            └─→ WiFiUploadTab.refresh_preview()  [Update upload preview]
```

### **3. Pattern Selection Chain**

```
PatternLibraryTab
    │
    ├─→ User selects pattern
    │
    ▼
pattern_selected.emit(Pattern, file_path)
    │
    └─→ MainWindow.on_pattern_library_selected()
        │
        ├─→ load_pattern_to_all_tabs()
        │   ├─→ PreviewTab.load_pattern()
        │   ├─→ FlashTab.load_pattern()
        │   ├─→ WiFiUploadTab.set_pattern()
        │   ├─→ DesignToolsTab.load_pattern()  [SHOULD ADD]
        │   └─→ BatchFlashTab.set_pattern()    [SHOULD ADD]
        │
        └─→ Switch to PreviewTab (or user's preference)
```

### **4. Flash Coordination Chain**

```
FlashTab
    │
    ├─→ User clicks "Build & Flash"
    │
    ├─→ [SHOULD ADD]
    │   └─→ firmware_building.emit()
    │       └─→ MainWindow.show_progress("Building firmware...")
    │
    ├─→ Build firmware
    │
    ├─→ [SHOULD ADD]
    │   └─→ firmware_built.emit(firmware_path)
    │       └─→ BatchFlashTab.cache_firmware(firmware_path)
    │
    ├─→ Flash to device
    │
    └─→ flash_complete.emit(success, message)
        └─→ MainWindow.on_flash_complete()
            └─→ Show status: "Flash complete" or "Flash failed"
```

### **5. WiFi Upload Chain**

```
WiFiUploadTab
    │
    ├─→ User clicks "Upload Pattern"
    │
    ├─→ [SHOULD ADD]
    │   └─→ upload_started.emit()
    │       └─→ MainWindow.show_progress("Uploading...")
    │
    ├─→ Upload pattern
    │   │
    │   └─→ [SHOULD ADD]
    │       └─→ upload_progress.emit(percent)
    │           └─→ MainWindow.update_progress(percent)
    │
    └─→ [SHOULD ADD]
        └─→ upload_complete.emit(success, message)
            └─→ MainWindow.on_wifi_upload_complete()
                └─→ Show status: "Upload complete" or "Upload failed"
```

---

## 📊 Signal Connection Matrix

| Source Tab | Signal | Destination | Status | Priority |
|------------|--------|-------------|--------|----------|
| MediaUploadTab | `pattern_loaded` | MainWindow | ✅ Connected | - |
| DesignToolsTab | `pattern_modified` | MainWindow | ✅ Connected | - |
| DesignToolsTab | `pattern_created` | MainWindow | ✅ Connected | - |
| PreviewTab | `pattern_modified` | MainWindow | ✅ Connected | - |
| FlashTab | `flash_complete` | MainWindow | ✅ Connected | - |
| PatternLibraryTab | `pattern_selected` | MainWindow | ✅ Connected | - |
| AudioReactiveTab | `pattern_generated` | MainWindow | ✅ Connected | - |
| MainWindow | `pattern_changed` | All Tabs | ❌ Missing | **P1** |
| DesignToolsTab | `pattern_modified` | PreviewTab | ❌ Missing | **P1** |
| PreviewTab | `playback_state_changed` | DesignToolsTab | ❌ Missing | **P2** |
| BatchFlashTab | `batch_flash_complete` | MainWindow | ❌ Missing | **P2** |
| WiFiUploadTab | `upload_complete` | MainWindow | ❌ Missing | **P2** |
| WiFiUploadTab | `upload_progress` | MainWindow | ❌ Missing | **P2** |
| FlashTab | `firmware_built` | BatchFlashTab | ❌ Missing | **P2** |
| ArduinoIDETab | `code_generated` | MainWindow | ❌ Missing | **P3** |
| PatternLibraryTab | `pattern_added` | MainWindow | ❌ Missing | **P3** |

---

## 🎯 Summary

### **Current State**
- ✅ Basic pattern distribution works
- ✅ Main tabs can create/load patterns
- ✅ MainWindow acts as central hub
- ❌ Missing real-time cross-tab sync
- ❌ Missing progress feedback signals
- ❌ Missing some tab-specific signals

### **Recommended Improvements**
1. **Add MainWindow.pattern_changed signal** (Priority 1)
2. **Enable live preview from DesignToolsTab** (Priority 1)
3. **Add missing completion signals** (Priority 2)
4. **Add progress feedback signals** (Priority 2)
5. **Enable cross-tab feature coordination** (Priority 3)

### **Benefits of Better Linking**
- ✅ Real-time updates across tabs
- ✅ Better user feedback
- ✅ Smoother workflows
- ✅ Reduced confusion
- ✅ Professional feel

---

**End of Document**

