# PID Digitization with Tesseract OCR

This is a modified version of the Azure Samples PID Digitization project that has been converted to use **open-source Tesseract OCR** instead of Azure Form Recognizer.

## 🔄 Major Changes Made

### ✅ Replaced Azure Form Recognizer with Tesseract OCR
- **Before**: Used `azure-ai-formrecognizer` package and Azure cloud services
- **After**: Uses `pytesseract` and local Tesseract OCR engine
- **Interface**: Maintained the same `read_text()` method signature for compatibility

### 🛠️ Technical Updates
1. **Dependencies**:
   - Removed: `azure-ai-formrecognizer`, `azure-identity` (for OCR)
   - Added: `pytesseract`, `Pillow`
   - Updated: `pydantic` to v2 for Python 3.13 compatibility

2. **OCR Client** (`src/app/services/text_detection/utils/ocr_client.py`):
   - Complete rewrite using Tesseract
   - Groups words into lines based on Tesseract's line detection
   - Creates bounding box polygons in the same format as before
   - Maintains error handling and same return format

3. **Configuration** (`src/app/config.py`):
   - Removed `form_recognizer_endpoint` requirement
   - Updated to Pydantic v2 syntax (`field_validator`, `model_validator`)
   - Updated `BaseSettings` import from `pydantic_settings`

4. **Documentation**:
   - Updated README.md to remove Azure Form Recognizer requirements
   - Updated text-detection-design.md to explain Tesseract usage
   - Added installation instructions for Tesseract

5. **Dockerfile**:
   - Added `tesseract-ocr` to system packages

6. **Tests**:
   - Updated OCR client tests to mock Tesseract instead of Azure services

## 🚀 Quick Start

### Prerequisites
1. **Install Tesseract OCR**:
   ```bash
   # macOS
   brew install tesseract
   
   # Ubuntu/Debian
   sudo apt-get install tesseract-ocr
   
   # Windows
   # Download from: https://github.com/UB-Mannheim/tesseract/wiki
   ```

2. **Install Python dependencies**:
   ```bash
   cd src
   pip install -r requirements.txt
   ```

### Running the App
1. **Set environment variables** (create `.env` file in `src/` directory):
   ```bash
   BLOB_STORAGE_ACCOUNT_URL=https://your-storage.blob.core.windows.net/
   BLOB_STORAGE_CONTAINER_NAME=your-container
   SYMBOL_DETECTION_API=https://your-symbol-api.com/
   SYMBOL_DETECTION_API_BEARER_TOKEN=your-token
   GRAPH_DB_CONNECTION_STRING=your-db-connection
   ```

2. **Run the application**:
   ```bash
   cd src
   python init_app.py
   ```

3. **Test OCR functionality**:
   ```bash
   # Run minimal test app
   python super_minimal_app.py
   # Visit http://localhost:8000/docs for API documentation
   ```

## 🎯 Benefits of This Change

1. **✅ Open Source**: No dependency on proprietary Azure services
2. **💰 Cost-Free**: No API costs for OCR processing  
3. **🔒 Privacy**: All processing happens locally
4. **🏗️ Self-Contained**: No external service dependencies
5. **🌐 Offline**: Works without internet connection
6. **🔧 Customizable**: Can tune Tesseract parameters for specific use cases

## 📋 Original vs. Modified

| Feature | Original (Azure) | Modified (Tesseract) |
|---------|------------------|---------------------|
| OCR Engine | Azure Form Recognizer | Tesseract OCR |
| Cost | Pay-per-use API | Free |
| Network | Requires internet | Offline capable |
| Setup | Azure subscription needed | Local installation only |
| Privacy | Data sent to cloud | Local processing only |
| Dependencies | Azure SDK packages | Open source packages |

## 🧪 Testing

The OCR client maintains the same interface, so existing code should work without modification:

```python
from app.services.text_detection.utils.ocr_client import ocr_client

# Same interface as before
for text, bounding_box in ocr_client.read_text(image_bytes):
    print(f"Found text: {text}")
    print(f"Bounding box: {bounding_box}")
```

## 📚 Additional Notes

- **Performance**: Tesseract performance may differ from Azure Form Recognizer depending on image quality and type
- **Accuracy**: For production use, you may want to fine-tune Tesseract parameters based on your specific P&ID images
- **Compatibility**: Maintains full backward compatibility with existing code that uses the OCR client

## 🤝 Contributing

This is a community-driven open-source modification. Feel free to:
- Report issues with Tesseract OCR integration
- Suggest improvements to OCR accuracy
- Add support for additional image preprocessing techniques
- Optimize Tesseract configuration parameters

---
*Based on the original Azure Samples PID Digitization project, modified to use open-source alternatives.*