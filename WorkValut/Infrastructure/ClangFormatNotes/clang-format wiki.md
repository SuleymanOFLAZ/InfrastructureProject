# Clang-format Wiki
### Gereksinimler
1. Clang-format yüklenmelidir.
2. Python yüklenmelidir.
3. Clang-format'ın path'ı Windows'un ortam değişkenlerine eklenmelidir. Clang-format, python, ve git'in terminal üzerinden erişilebilir olması gerekmektedir.

### format.py
format.py, clang-format aracını kaynak kodları üzerinde çalıştıran ve format uyumsuzluklarını bildiren bir script'tir. Kod üzerinde değişiklik yapmamaktadır, sadece format uyumsuzlukarını bildirir. Geliştirici gerekli değişiklikleri kendisi yapmalıdır.
format.py'i iki farklı şekilde kullanabiliriz:
1. Sadece son commit sonrası değiştirilen dosyaların format kontrolünü yapmak:
```shell
python format.py
```
2. Tüm proje kodlarının format kontrolünü yapmak. Bunun için -f argümanı kullanmalıyız.
```shell
python format.py -f
```
## Git pre-commit hook
Git pre-commit hook kullanarak, format.py commit öncesi çalıştırılır, bu sayede format'ı düzgün olmayan commit'ler engellenmiş olur.
Git hook'ları proje kaynak klasörü içerisinde  *.git/hooks/* içerisinde bulunmaktadır. .git klasörü versiyon kontrolüne dahil olmadığı için hook ayarları geliştiriciler arasında direkt olarak paylaşılamamaktadır. Yani git clone ile klonlanan proje dosyalarıyla birlikte git hook ayarları gelmemektedir. Bu sebeple kullanılacak git hook'ları, her geliştirici kendisi proje klonuna entegre etmelidir.
- **Hook entegre etmek**
Kullanılacak pre-commit hook dosyası proje klasöründe *hooks* içerisinde paylaşılmıştır. Buradaki *pre-commit* dosyasının *.git/hooks/* içerisine kopyalanması gerekmektedir. .git klasörünün gizli bir klasör olduğu unutulmamalıdır.
## Clang-format VSCode Entegrasyonu
1. Eklenti kurulumu:
VSCode Clang-Format (xaver tarafından) eklentisi kurulmalıdır. 
2. Gerekli ayarların yapılması:
Clang-format'ı varsayılan formatlayıcı olarak seçmek için *ctrl + shift + P* > *Format document with* > *configure default formatter* > *Clang-Format* seçilmelidir. Ek bir ayar yapmaya gerek yoktur, eklenti proje kök dosyasındaki .clang-format (ayar) dosyasını kendisi görmektedir.
3. Kullanımı:
Format düzenlemesi yapmak istediğimiz dosyada *shift + alt + F* kısyolu ile veya 
*sağ-tık, format document* ile format değişikliklerini yapabiliriz.
## Clang-format Eclipse Entegrasyonu
1. Eklenti kurulumu:
TGO üzerinden *Help* > *Eclipse Marketplace...* penceresi açılmalıdır. Arama penceresine *CppStyle* yazılarak *CppStyle 1.5.0.0* eklentisi kurulmalıdır.
2. Gerekli ayarların yapılması:
	- *Windows* > *Preferences* penceresi altında,
		- *C/C++* > *Code Style* > *Formatter* sekmesinde *Code Formatter: * kutusu altında *CppStyle (clang-format)* seçilmelidir.
		- *C/C++* > *CppStyle* > altında *Clang-format path* girilmelidir.
3. Kullanımı:
	Üzerinde olduğumuz dosyada *Ctrl + Shift + F* ısayolu ile clang-formatı çalıştırabiliriz. Veya *Source* > *Format* yolunu izleyerek kullanabiliriz.