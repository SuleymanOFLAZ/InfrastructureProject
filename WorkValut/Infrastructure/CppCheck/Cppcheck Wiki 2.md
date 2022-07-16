# CppCheck Wiki
## check.py
check.py açıklaması.
## Cppcheck VS Code entegrasyonu
1. Eklenti kurulumu:
*C/C++ Advanced Lint* eklentisi kurulmalıdır.
2. Ayarların yapılması:
*Ctrl+Shift+P* kısayolu ile *Open Settings (JSON)* seçerek *settings.json* dosyası açılmalıdır.
- Eklenti ayarılarını yapmak için şu değişkenleri eklemeliyiz:
```json
	"c-cpp-flylint.enable": true,
	"c-cpp-flylint.cppcheck.enable": true,
	"c-cpp-flylint.flawfinder.enable": false,
    "c-cpp-flylint.flexelint.enable": false,
    "c-cpp-flylint.lizard.enable": false,
    "c-cpp-flylint.language": "c",
    "c-cpp-flylint.standard": [
        "c11"
    ],
```
- Eki