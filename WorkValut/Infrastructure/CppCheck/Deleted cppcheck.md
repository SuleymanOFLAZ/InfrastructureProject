*File* > *Preferences* > *Settings* yoluna gidilmelidir. *Ctrl+,* kısayolu ile ulaşabiliriz.
	- *Extensions* > *C/C++ Lint configuration* yoluna gidilmelidir.
	- Şunlar **kapatılmalıdır**:
		- Clang: Enable
		- Flawfinder: Enable
		- Flexelint: Enable
		- Lizard: Enable
	- Şunların açık olduğundan emin olunmalıdır:
		- Cppcheck: Enable
	- Aynı pencerede *Cppcheck: Addons* > *Edit in settings.json* ile json dosyasına gidilmelidir.
		- Misra addon'u çalıştırmak için *c-cpp-flylint.cppcheck.addons* değişkenini şu şekilde düzenlemeliyiz:
		```json
		"c-cpp-flylint.cppcheck.addons": [
		"cppcheck/misraAddon/misraRule.json"
		],
		```
		- Eklenti dil ayarlarını girmek için daha önce düzenleme yaptığımız json dosyasına şu değişkenler girilmelidir:
		```shell
		"c-cpp-flylint.language": "c",
		"c-cpp-flylint.standard": [
		"c11"
		],
		```
		- Cppcheck ayarları için yine json dosyasında şu düzenlemeleri yapabiliriz:
