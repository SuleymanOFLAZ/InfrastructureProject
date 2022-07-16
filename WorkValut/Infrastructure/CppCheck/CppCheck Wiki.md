# CppCheck Wiki
## check.py
check.py açıklaması.
## Cppcheck VS Code entegrasyonu
1. Eklenti kurulumu:
*C/C++ Advanced Lint* eklentisi kurulmalıdır.
2. Ayarların yapılması:
*Ctrl+Shift+P* kısayolu ile *Open Settings (JSON)* seçilerek *settings.json* dosyası açılmalıdır.
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
	
- Eklenti cppcheck ayarları yapmak için şu değişkenleri eklemeliyiz:
```json
	"c-cpp-flylint.cppcheck.addons": [
	"cppcheck/misraAddon/misraRule.json"
	],
	"c-cpp-flylint.cppcheck.language": "c",
	"c-cpp-flylint.cppcheck.standard": [
		"c11"
		],
	"c-cpp-flylint.cppcheck.includePaths": [
		"src/include"
		],
	"c-cpp-flylint.cppcheck.severityLevels": {
	"error": "Error",
	"warning": "Warning",
	"style": "Information",
	"performance": "Information",
	"portability": "Information",
	"information": "Information"
	},
```

## Cppcheck Eclipse entegrasyonu
1. Eklenti kurulumu:
TGO üzerinden *Help* > *Eclipse Marketplace...* penceresi açılmalıdır. *cppcheclipse 1.1.1* eklentisi kurulmalıdır.