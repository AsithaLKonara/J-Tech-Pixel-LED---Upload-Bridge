# Layer and Frame-Based Design System

**Upload Bridge - Design Tools Architecture**

---

## 📐 Overview

The Upload Bridge design system uses a **two-level hierarchy** for organizing LED pattern data:

1. **Frames** - Time-based animation frames (temporal dimension)
2. **Layers** - Per-frame compositing layers (spatial dimension)

This architecture allows for complex animations with non-destructive editing, layer compositing, and flexible frame management.

---

## 🎬 Frame System

### What is a Frame?

A **Frame** represents a single moment in time within an animation sequence. Each frame contains:
- **Pixel Data**: RGB values for all LEDs `[(R, G, B), ...]`
- **Duration**: How long to display this frame (in milliseconds)

### Frame Structure

```python
@dataclass
class Frame:
    pixels: List[Tuple[int, int, int]]  # RGB values for each LED
    duration_ms: int                    # Display duration
    
    @property
    def led_count(self) -> int:
        return len(self.pixels)
```

### Frame Management (FrameManager)

The `FrameManager` handles all frame-level operations:

#### Key Operations:
- **Add Frame**: Insert a new blank frame after the current one
- **Duplicate Frame**: Copy an existing frame
- **Delete Frame**: Remove a frame (cannot delete the last one)
- **Move Frame**: Reorder frames in the timeline
- **Set Duration**: Change how long a frame displays
- **Select Frame**: Switch which frame is currently being edited

#### Example Usage:
```python
# Add a new frame
frame_manager.add_blank_after_current(duration_ms=100)

# Duplicate current frame
new_frame_index = frame_manager.duplicate()

# Delete a frame
frame_manager.delete(index=2)

# Move frame from position 3 to position 1
frame_manager.move(src=3, dest=1)

# Change frame duration
frame_manager.set_duration(index=0, duration_ms=200)
```

### Frame Signals

The `FrameManager` emits Qt signals for UI updates:
- `frames_changed` - Emitted when frame structure changes
- `frame_index_changed` - Emitted when current frame selection changes
- `frame_duration_changed` - Emitted when a frame's duration is modified

---

## 🎨 Layer System

### What is a Layer?

A **Layer** is a separate drawing surface within a single frame. Each frame can have multiple layers that are composited together to create the final displayed image.

### Layer Structure

```python
class Layer:
    name: str                           # Layer name (e.g., "Background", "Foreground")
    pixels: List[Tuple[int, int, int]]  # RGB values for this layer
    visible: bool = True                 # Show/hide this layer
    opacity: float = 1.0                # Opacity (0.0 = transparent, 1.0 = opaque)
```

### Layer Properties

1. **Name**: User-friendly identifier (e.g., "Background", "Text", "Effects")
2. **Pixels**: The actual RGB data for this layer
3. **Visible**: Whether the layer contributes to the final composite
4. **Opacity**: Alpha blending value (0.0 to 1.0)

### Layer Management (LayerManager)

The `LayerManager` handles all layer-level operations per frame:

#### Key Operations:
- **Add Layer**: Create a new layer in a frame
- **Remove Layer**: Delete a layer (cannot remove the last one)
- **Move Layer**: Reorder layers (affects compositing order)
- **Set Visibility**: Show/hide a layer
- **Set Opacity**: Adjust layer transparency
- **Set Name**: Rename a layer
- **Apply Pixel**: Paint to a specific layer
- **Get Composite**: Blend all visible layers into final pixels

#### Example Usage:
```python
# Add a new layer to frame 0
layer_index = layer_manager.add_layer(frame_index=0, name="Background")

# Hide a layer
layer_manager.set_layer_visible(frame_index=0, layer_index=1, visible=False)

# Set layer opacity to 50%
layer_manager.set_layer_opacity(frame_index=0, layer_index=1, opacity=0.5)

# Paint a pixel to a specific layer
layer_manager.apply_pixel(
    frame_index=0,
    x=5, y=10,
    colour=(255, 0, 0),  # Red
    width=16, height=16,
    layer_index=1
)

# Get the composite of all visible layers
composite_pixels = layer_manager.get_composite_pixels(frame_index=0)
```

### Layer Compositing

Layers are composited using **alpha blending** from bottom to top:

```python
def get_composite_pixels(self, frame_index: int) -> List[Color]:
    """Blend all visible layers into final composite."""
    composite = [(0, 0, 0)] * (width * height)  # Start with black
    
    for layer in layers:  # Bottom to top order
        if not layer.visible:
            continue
        
        opacity = layer.opacity
        for i in range(len(composite)):
            r1, g1, b1 = composite[i]      # Current composite
            r2, g2, b2 = layer.pixels[i]   # Layer pixel
            
            # Alpha blend: composite = (1-opacity) * composite + opacity * layer
            r = int(r1 * (1 - opacity) + r2 * opacity)
            g = int(g1 * (1 - opacity) + g2 * opacity)
            b = int(b1 * (1 - opacity) + b2 * opacity)
            
            composite[i] = (r, g, b)
    
    return composite
```

### Layer Signals

The `LayerManager` emits Qt signals for UI updates:
- `layers_changed` - Emitted when layer structure changes
- `layer_added` - Emitted when a new layer is created
- `layer_removed` - Emitted when a layer is deleted
- `layer_moved` - Emitted when layers are reordered
- `pixel_changed` - Emitted when a pixel is modified
- `frame_pixels_changed` - Emitted when frame pixels are updated

---

## 🔄 How Frames and Layers Work Together

### Architecture Overview

```
Pattern
├── Frame 0 (100ms)
│   ├── Layer 0: "Background" (visible, opacity=1.0)
│   ├── Layer 1: "Text" (visible, opacity=1.0)
│   └── Layer 2: "Effects" (visible, opacity=0.5)
│   └── [Composite] → Frame.pixels
│
├── Frame 1 (150ms)
│   ├── Layer 0: "Background" (visible, opacity=1.0)
│   ├── Layer 1: "Text" (visible, opacity=1.0)
│   └── [Composite] → Frame.pixels
│
└── Frame 2 (100ms)
    ├── Layer 0: "Background" (visible, opacity=1.0)
    └── [Composite] → Frame.pixels
```

### Data Flow

1. **User paints on canvas** → Pixel applied to active layer
2. **LayerManager** → Updates layer's pixel array
3. **Compositing** → All visible layers blended into composite
4. **Frame sync** → Composite pixels written to `Frame.pixels`
5. **Canvas refresh** → UI displays the composite

### Key Principles

1. **Layers are per-frame**: Each frame has its own independent set of layers
2. **One-way sync**: Layers → Frame (composite is written to frame, not read from it)
3. **Non-destructive**: Editing layers doesn't modify the frame directly until compositing
4. **Independent control**: Each layer can be shown/hidden and have different opacity

---

## 🎯 Use Cases

### Use Case 1: Background + Foreground

**Scenario**: Create an animation with a static background and animated foreground.

**Solution**:
- Frame 0:
  - Layer 0: "Background" - Static pattern (visible, opacity=1.0)
  - Layer 1: "Foreground" - Animated element (visible, opacity=1.0)
- Frame 1:
  - Layer 0: "Background" - Same static pattern
  - Layer 1: "Foreground" - Moved/changed animated element

**Benefit**: Background is drawn once, foreground changes per frame.

### Use Case 2: Text Overlay

**Scenario**: Add text that appears over an existing animation.

**Solution**:
- All frames:
  - Layer 0: "Animation" - Original animation (visible, opacity=1.0)
  - Layer 1: "Text" - Text overlay (visible, opacity=1.0)

**Benefit**: Text can be edited independently without touching the animation.

### Use Case 3: Fade Effects

**Scenario**: Create a fade-in effect for an element.

**Solution**:
- Frame 0:
  - Layer 0: "Background" (visible, opacity=1.0)
  - Layer 1: "Fade Element" (visible, opacity=0.0)
- Frame 1:
  - Layer 0: "Background" (visible, opacity=1.0)
  - Layer 1: "Fade Element" (visible, opacity=0.25)
- Frame 2:
  - Layer 0: "Background" (visible, opacity=1.0)
  - Layer 1: "Fade Element" (visible, opacity=0.5)
- ... (continue to opacity=1.0)

**Benefit**: Smooth fade effect by adjusting layer opacity across frames.

### Use Case 4: Non-Destructive Editing

**Scenario**: Try different effects without losing the original.

**Solution**:
- Frame 0:
  - Layer 0: "Original" (visible, opacity=1.0)
  - Layer 1: "Effect Test" (visible, opacity=0.5) - Try effect here
  - Layer 2: "Alternative" (visible=False) - Hide while testing

**Benefit**: Can toggle layers on/off to compare different versions.

---

## 🔧 Technical Implementation

### Pattern State Management

The system uses a `PatternState` object to maintain the current pattern:

```python
class PatternState:
    """Central state container for the current pattern."""
    def pattern(self) -> Optional[Pattern]
    def frames(self) -> List[Frame]
    def width(self) -> int
    def height(self) -> int
```

### Layer Storage

Layers are stored per frame in a dictionary:
```python
_layers: Dict[int, List[Layer]] = {
    0: [Layer("Background"), Layer("Foreground")],
    1: [Layer("Background"), Layer("Foreground")],
    2: [Layer("Background")]
}
```

### Compositing Algorithm

The compositing process:
1. Start with black background `[(0, 0, 0), ...]`
2. For each layer (bottom to top):
   - Skip if not visible
   - Alpha blend: `composite = (1-opacity) * composite + opacity * layer`
3. Write composite to `Frame.pixels`

### Frame Synchronization

When layers change, the frame is updated:
```python
def sync_frame_from_layers(self, frame_index: int):
    """Update frame pixels from composite of all layers."""
    composite = self.get_composite_pixels(frame_index)
    self._state.pattern().frames[frame_index].pixels = composite
```

---

## 📊 Data Structure Hierarchy

```
Pattern
│
├── PatternMetadata
│   ├── width, height
│   ├── color_order
│   ├── brightness
│   └── ... (configuration)
│
└── frames: List[Frame]
    │
    └── Frame 0
        ├── pixels: List[RGB]  ← Composite from layers
        ├── duration_ms: int
        │
        └── layers: List[Layer]  ← Managed by LayerManager
            ├── Layer 0: "Background"
            │   ├── pixels: List[RGB]
            │   ├── visible: bool
            │   └── opacity: float
            │
            └── Layer 1: "Foreground"
                ├── pixels: List[RGB]
                ├── visible: bool
                └── opacity: float
```

---

## 🎨 UI Integration

### Canvas Painting

When user paints on the canvas:
1. Get active layer index from layer panel
2. Calculate pixel position (x, y)
3. Call `layer_manager.apply_pixel(frame_index, x, y, color, width, height, layer_index)`
4. LayerManager updates the layer's pixels
5. LayerManager composites all layers
6. LayerManager syncs composite to frame
7. Canvas refreshes to show the composite

### Layer Panel

The layer panel shows:
- List of layers for current frame
- Visibility checkboxes
- Opacity sliders
- Layer names (editable)
- Add/remove layer buttons
- Layer reordering (drag & drop)

### Timeline

The timeline shows:
- All frames in sequence
- Current frame indicator (playhead)
- Frame durations
- Layer tracks (optional visualization)
- Automation overlays

---

## 🔄 Workflow Examples

### Creating a Multi-Layer Animation

1. **Create Pattern**: New pattern with dimensions (e.g., 16×16)
2. **Add Frame**: Create first frame
3. **Add Background Layer**: 
   - Add layer named "Background"
   - Paint background pattern
4. **Add Foreground Layer**:
   - Add layer named "Foreground"
   - Paint animated element
5. **Add More Frames**:
   - Duplicate frame
   - Modify foreground layer only
   - Background stays the same
6. **Adjust Opacity**:
   - Set foreground layer opacity to 0.8 for subtle effect
7. **Export**: Composite layers → Frame pixels → Export pattern

### Editing Workflow

1. **Select Frame**: Click on timeline frame
2. **Select Layer**: Click on layer in layer panel
3. **Paint**: Draw on canvas (paints to selected layer)
4. **Toggle Visibility**: Hide/show layers to see different versions
5. **Adjust Opacity**: Fine-tune layer blending
6. **Reorder Layers**: Drag layers to change compositing order

---

## 🎯 Benefits of This Architecture

### 1. Non-Destructive Editing
- Original content preserved in separate layers
- Can hide/show layers to compare versions
- Can adjust opacity without losing data

### 2. Flexible Compositing
- Multiple layers per frame
- Independent visibility control
- Opacity-based blending
- Layer reordering

### 3. Efficient Workflow
- Reuse layers across frames
- Edit one layer without affecting others
- Quick iteration with layer toggling

### 4. Professional Features
- Similar to Photoshop/GIMP layer system
- Familiar workflow for designers
- Supports complex animations

---

## 📝 Key Classes and Methods

### FrameManager (`domain/frames.py`)

**Purpose**: Manage frame-level operations

**Key Methods**:
- `add_blank_after_current(duration_ms)` - Add new frame
- `duplicate(index)` - Copy frame
- `delete(index)` - Remove frame
- `move(src, dest)` - Reorder frames
- `set_duration(index, duration_ms)` - Change frame duration
- `select(index)` - Switch current frame

### LayerManager (`domain/layers.py`)

**Purpose**: Manage layer-level operations per frame

**Key Methods**:
- `get_layers(frame_index)` - Get all layers for a frame
- `add_layer(frame_index, name)` - Create new layer
- `remove_layer(frame_index, layer_index)` - Delete layer
- `move_layer(frame_index, from_index, to_index)` - Reorder layers
- `set_layer_visible(frame_index, layer_index, visible)` - Show/hide
- `set_layer_opacity(frame_index, layer_index, opacity)` - Set opacity
- `apply_pixel(frame_index, x, y, color, width, height, layer_index)` - Paint pixel
- `get_composite_pixels(frame_index)` - Get blended result
- `sync_frame_from_layers(frame_index)` - Update frame from layers

### Layer (`domain/layers.py`)

**Purpose**: Represent a single layer

**Properties**:
- `name: str` - Layer identifier
- `pixels: List[RGB]` - Pixel data
- `visible: bool` - Visibility flag
- `opacity: float` - Opacity (0.0-1.0)

### Frame (`core/pattern.py`)

**Purpose**: Represent a single animation frame

**Properties**:
- `pixels: List[RGB]` - Final composite pixels
- `duration_ms: int` - Display duration

---

## 🔍 Signal Flow

### When User Paints a Pixel:

```
User clicks canvas
    ↓
CanvasController.handle_paint()
    ↓
LayerManager.apply_pixel(frame_index, x, y, color, layer_index)
    ↓
Layer.pixels updated
    ↓
LayerManager.sync_frame_from_layers()
    ↓
LayerManager.get_composite_pixels()  ← Blends all visible layers
    ↓
Frame.pixels = composite
    ↓
Signals emitted:
    - pixel_changed.emit()
    - layers_changed.emit()
    - frame_pixels_changed.emit()
    ↓
UI updates:
    - Canvas refreshes
    - Layer panel updates
    - Timeline updates
```

### When User Adds a Layer:

```
User clicks "Add Layer"
    ↓
LayerManager.add_layer(frame_index, name)
    ↓
New Layer created with blank pixels
    ↓
Layer added to frame's layer list
    ↓
Signals emitted:
    - layer_added.emit(frame_index, layer_index)
    - layers_changed.emit(frame_index)
    ↓
UI updates:
    - Layer panel shows new layer
    - Canvas ready for painting
```

---

## 💡 Best Practices

### 1. Layer Organization
- **Name layers descriptively**: "Background", "Text", "Effects"
- **Keep layers focused**: One purpose per layer
- **Use layer order**: Bottom = background, Top = foreground

### 2. Frame Management
- **Consistent layer structure**: Same layers across frames for consistency
- **Frame durations**: Set appropriate durations for smooth animation
- **Frame ordering**: Organize frames logically in timeline

### 3. Performance
- **Limit layer count**: Too many layers can slow compositing
- **Hide unused layers**: Improves compositing performance
- **Optimize opacity**: Full opacity (1.0) is faster than partial

### 4. Workflow
- **Start with background**: Create background layer first
- **Add details incrementally**: Build up layers one at a time
- **Test visibility**: Toggle layers to see different combinations

---

## 🎬 Example: Creating a Scrolling Text Animation

### Step-by-Step:

1. **Create Pattern**: 16×16 matrix, 10 frames

2. **Frame 0**:
   - Layer 0: "Background" - Solid color
   - Layer 1: "Text" - "HELLO" at position (0, 7)

3. **Frame 1**:
   - Layer 0: "Background" - Same (duplicated)
   - Layer 1: "Text" - "HELLO" at position (1, 7) ← Scrolled right

4. **Frame 2-9**:
   - Continue scrolling text across matrix

**Result**: Text scrolls across a static background, with each layer independently editable.

---

## 🔧 Advanced Features

### Layer Binding in Automation

Layers can be bound to automation actions:
```python
LayerBinding(
    layer_index=1,
    action="scroll",
    direction="right"
)
```

This allows automation to affect specific layers independently.

### Per-Frame Layer Variations

Each frame can have different layers:
- Frame 0: 3 layers
- Frame 1: 2 layers
- Frame 2: 4 layers

This flexibility allows for complex animations where layer structure changes over time.

---

## 📚 Summary

The layer and frame-based design system provides:

✅ **Frames** - Temporal dimension (animation over time)  
✅ **Layers** - Spatial dimension (compositing within a frame)  
✅ **Non-destructive editing** - Layers preserve original content  
✅ **Flexible compositing** - Visibility, opacity, ordering  
✅ **Professional workflow** - Similar to image editing software  
✅ **Signal-based updates** - Reactive UI updates  
✅ **Independent control** - Edit frames and layers separately  

This architecture enables complex LED matrix animations with professional-grade editing capabilities.

---

**End of Document**

