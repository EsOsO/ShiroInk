# Miglioramento Punto 3: Pipeline di Processing Configurabile

## Obiettivo
Implementare una pipeline di processing modulare e configurabile che permetta di:
- Modificare l'ordine delle operazioni di processing
- Abilitare/disabilitare singoli step
- Creare preset ottimizzati per diversi dispositivi
- Estendere facilmente con nuovi step di processing

## Architettura

### Pattern Utilizzati
- **Strategy Pattern**: Ogni step di processing è una strategia intercambiabile
- **Chain of Responsibility**: Gli step vengono eseguiti in sequenza
- **Builder Pattern**: Costruzione fluida della pipeline con method chaining
- **Factory Pattern**: PipelinePresets per creare configurazioni predefinite

## Modifiche Implementate

### 1. Interfaccia ProcessingStep (src/image_pipeline/pipeline.py)

```python
class ProcessingStep(ABC):
    """Abstract base class for image processing steps."""
    
    @abstractmethod
    def process(self, image: Image.Image) -> Image.Image:
        """Process the image."""
        pass
    
    @abstractmethod
    def get_name(self) -> str:
        """Get the name of this processing step."""
        pass
```

**Caratteristiche:**
- Interfaccia comune per tutti gli step
- Configurazione tramite kwargs nel costruttore
- Rappresentazione string per debugging

### 2. Classe ImagePipeline

```python
class ImagePipeline:
    """Configurable image processing pipeline."""
    
    def add_step(self, step: ProcessingStep) -> "ImagePipeline"
    def remove_step(self, step_name: str) -> "ImagePipeline"
    def clear(self) -> "ImagePipeline"
    def process(self, image: Image.Image) -> Image.Image
```

**Funzionalità:**
- Gestione dinamica degli step (add, remove, clear)
- Method chaining per costruzione fluida
- Esecuzione sequenziale degli step
- Informazioni sulla pipeline (get_steps, len, repr)

### 3. Refactoring Step Esistenti

#### ContrastStep
```python
class ContrastStep(ProcessingStep):
    def __init__(self, factor: float = 1.5):
        super().__init__(factor=factor)
        self.factor = factor
```

#### SharpenStep
```python
class SharpenStep(ProcessingStep):
    def __init__(self, factor: float = 1.2):
        super().__init__(factor=factor)
        self.factor = factor
```

#### QuantizeStep
```python
class QuantizeStep(ProcessingStep):
    def __init__(self, palette: bytes = Palette16):
        super().__init__(palette=palette)
        self.palette = palette
```

**Nota:** Le funzioni legacy (contrast, sharpen, quantize) sono mantenute per backward compatibility.

### 4. Pipeline Presets (src/image_pipeline/presets.py)

#### Preset Disponibili

**Kindle** (default)
- Contrast (factor=1.5) → High contrast per display e-ink
- Sharpen (factor=1.2) → Moderato sharpening
- Quantize (16 colors) → Riduzione dimensione file

**Tablet**
- Contrast (factor=1.3) → Moderato contrasto
- Sharpen (factor=1.1) → Leggero sharpening
- No Quantize → Preserva i colori

**Print**
- Sharpen (factor=1.05) → Solo leggero sharpening
- Minimal processing per stampa

**High Quality**
- Contrast (factor=1.2) → Leggero contrasto
- Sharpen (factor=1.4) → Enhanced sharpening
- No Quantize → Qualità massima

**Minimal**
- Pipeline vuota → Nessun processing

**Custom**
```python
PipelinePresets.custom(
    contrast=1.8,      # Optional
    sharpen=1.5,       # Optional
    quantize=True      # Optional
)
```

### 5. Integrazione con ProcessingConfig

```python
@dataclass
class ProcessingConfig:
    # ... altri campi ...
    pipeline_preset: str = "kindle"
    custom_pipeline: ImagePipeline | None = None
    
    def get_pipeline(self) -> ImagePipeline:
        """Get the pipeline based on configuration."""
        if self.custom_pipeline is not None:
            return self.custom_pipeline
        else:
            return PipelinePresets.get_preset(self.pipeline_preset)
```

### 6. Supporto CLI

```bash
python src/main.py src dest --pipeline kindle      # Default
python src/main.py src dest --pipeline tablet
python src/main.py src dest --pipeline print
python src/main.py src dest --pipeline high_quality
python src/main.py src dest --pipeline minimal
```

```
-p {kindle,tablet,print,high_quality,minimal}, --pipeline {kindle,tablet,print,high_quality,minimal}
    Processing pipeline preset to use (default: kindle)
```

## Esempi di Utilizzo

### Uso CLI Standard
```bash
# Kindle preset (default)
python src/main.py manga_folder output_folder

# Tablet preset
python src/main.py manga_folder output_folder --pipeline tablet

# Minimal processing
python src/main.py manga_folder output_folder --pipeline minimal
```

### Uso Programmatico - Preset
```python
from image_pipeline.presets import PipelinePresets
from image_pipeline import process

# Usa preset
pipeline = PipelinePresets.kindle()
process(image_path, output_path, resolution, pipeline=pipeline)
```

### Uso Programmatico - Custom
```python
from image_pipeline.pipeline import ImagePipeline
from image_pipeline.contrast import ContrastStep
from image_pipeline.sharpen import SharpenStep

# Costruisci pipeline custom
pipeline = ImagePipeline()
pipeline.add_step(ContrastStep(factor=2.0))
pipeline.add_step(SharpenStep(factor=1.8))

process(image_path, output_path, resolution, pipeline=pipeline)
```

### Method Chaining
```python
pipeline = (ImagePipeline()
           .add_step(ContrastStep(factor=1.5))
           .add_step(SharpenStep(factor=1.2))
           .add_step(QuantizeStep()))
```

### Modifica Dinamica
```python
# Parti da un preset
pipeline = PipelinePresets.kindle()

# Rimuovi quantization per preservare colori
pipeline.remove_step("Quantize")

# Aggiungi uno step custom
pipeline.add_step(CustomBlurStep(radius=2))
```

## Estendibilità

### Creare un Nuovo Processing Step

```python
from image_pipeline.pipeline import ProcessingStep
from PIL import Image, ImageFilter

class BlurStep(ProcessingStep):
    """Custom blur processing step."""
    
    def __init__(self, radius: float = 2.0):
        super().__init__(radius=radius)
        self.radius = radius
    
    def process(self, image: Image.Image) -> Image.Image:
        return image.filter(ImageFilter.GaussianBlur(self.radius))
    
    def get_name(self) -> str:
        return "Blur"

# Uso
pipeline = ImagePipeline()
pipeline.add_step(BlurStep(radius=3.0))
```

### Creare un Nuovo Preset

```python
@staticmethod
def manga_optimized() -> ImagePipeline:
    """Pipeline ottimizzata per manga."""
    pipeline = ImagePipeline()
    pipeline.add_step(ContrastStep(factor=1.8))
    pipeline.add_step(SharpenStep(factor=1.5))
    pipeline.add_step(QuantizeStep())
    return pipeline
```

## Testing

### Test Unitari (test_pipeline.py)
```bash
python -m unittest test_pipeline.py -v
```

**Coverage:**
- 16 test passati
- Test per ogni step individuale
- Test per pipeline con multiple configurazioni
- Test per tutti i preset
- Test per modifica dinamica della pipeline

**Risultati:**
```
Ran 16 tests in 0.005s
OK
```

### Test Funzionali
```bash
# Test con diversi preset
python src/main.py test_dir output --dry-run --pipeline kindle
python src/main.py test_dir output --dry-run --pipeline tablet
python src/main.py test_dir output --dry-run --pipeline minimal
```

## Vantaggi Ottenuti

### 1. Flessibilità
- **Prima:** Pipeline hardcoded (contrast → sharpen → quantize)
- **Dopo:** Pipeline completamente configurabile via CLI o codice

### 2. Estendibilità
- Aggiungere nuovi step richiede solo:
  1. Creare classe che estende ProcessingStep
  2. Implementare process() e get_name()
- Zero modifiche al core del sistema

### 3. Testabilità
- Ogni step testabile isolatamente
- Pipeline testabile con mock steps
- 16 unit test che validano funzionalità

### 4. Riusabilità
- Preset predefiniti per casi d'uso comuni
- Facile creare nuovi preset
- Pipeline condivisibili tra progetti

### 5. Performance
- Possibilità di disabilitare step costosi
- Pipeline minimal per processing veloce
- Ottimizzazioni device-specific

## Confronto Prima/Dopo

### Prima: Hardcoded Pipeline
```python
def process(image_path, output_path, ...):
    img = contrast(img)      # Sempre applicato
    img = sharpen(img)       # Sempre applicato
    img = quantize(img)      # Sempre applicato
```

**Problemi:**
- Impossibile modificare ordine
- Impossibile disabilitare step
- Impossibile aggiungere step custom
- Un solo caso d'uso (Kindle)

### Dopo: Configurable Pipeline
```python
def process(image_path, output_path, ..., pipeline=None):
    if pipeline is None:
        pipeline = PipelinePresets.kindle()
    
    processed_img = pipeline.process(img)  # Configurabile!
```

**Vantaggi:**
- Ordine modificabile
- Step abilitabili/disabilitabili
- Estensibile con step custom
- Multiple configurazioni (5 preset + custom)

## Backward Compatibility

**100% mantenuta:**
- Comportamento default identico (Kindle preset)
- Funzioni legacy (contrast, sharpen, quantize) ancora disponibili
- API process() retrocompatibile (pipeline parameter opzionale)

## Metriche

- **Nuove classi:** 4 (ProcessingStep, ImagePipeline, PipelinePresets + 3 Step classes)
- **Preset predefiniti:** 5 (kindle, tablet, print, high_quality, minimal)
- **Linee di codice:** ~400 (pipeline.py + presets.py + refactoring)
- **Test coverage:** 16 unit test, 100% successo
- **Flessibilità:** Da 1 configurazione fissa a infinite configurazioni

## Casi d'Uso Reali

### 1. Webcomic per Mobile
```bash
python src/main.py webcomic/ output/ --pipeline tablet -r 1080x1920
```

### 2. Manga per E-Ink
```bash
python src/main.py manga/ output/ --pipeline kindle
```

### 3. Archivio Alta Qualità
```bash
python src/main.py original/ archive/ --pipeline high_quality
```

### 4. Conversione Veloce (No Processing)
```bash
python src/main.py source/ dest/ --pipeline minimal
```

## Conclusioni

Il refactoring della pipeline di processing rappresenta un miglioramento sostanziale:

1. **Architettura**: Da monolitica a modulare
2. **Configurabilità**: Da zero a completa
3. **Estendibilità**: Facile aggiungere nuovi step
4. **Testabilità**: Ogni componente testabile isolatamente
5. **Usabilità**: Preset pronti all'uso + personalizzazione avanzata

Il sistema è ora pronto per supportare qualsiasi caso d'uso di processing immagini mantenendo semplicità per gli utenti base e potenza per gli utenti avanzati.
