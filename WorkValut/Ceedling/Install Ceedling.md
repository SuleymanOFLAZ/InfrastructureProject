# Ceedling'i kurmak
Ceedling'in çalıışması için hem **GCC**'ye hem de **Ruby**'e ihtiyacı var. Bu sebeple önce GCC ve Ruby kurmalıyız.
	**Not:** Host PC'miz için native GCC kurmalıyız, yani hedef işlemci için cross-compler'i değil. Buradaki hedefimiz unit tesleti host PC'de kurup çalıştırmaktır.

Ceedling komut satırında çalışacaktır, yani Ruby ve GCC için path'ların ortam dağişkenlerinde tanımlı olması gerekmektedir.

## Ruby kurulumu
Ruby'i indirmek için: [rubyinstaller.org.](https://rubyinstaller.org/downloads/)
- Kurulum sırasında *Add Ruby executables to your PATH* seçilebilir.
>**NOT**: **Ruby version 3.0.x kurulmalıdır.** Version 3.1.x ile birlikte gelen gem psych 4.xx sürümü ile yaml dosyası açma problemleri oluşuyor. Ruby 3.0.x ile geleb psych 3.xx de bu problem yok. (yaml dosyaları için "safe_load - load" farkı)

## GCC kurulummu
Cygwin: [Cygwin](https://www.cygwin.com/)
- gcc, g++, gdb, make, bash indirmekte fayda var.

## Ceedling'i kurmak
Şu komut satırı ile ceedling'i kurabiliriz:
```cmd
gem install ceedling
```
Şu komut satırı ile ceedling kurulumunu kontrol edebiliriz:
```cmd
gem list ceedling
```