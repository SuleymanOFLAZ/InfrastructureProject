# Ceedling'i kullanmak için Adım Adım kılavuz:
1. Ceedling'i Ruby ve MinGW (Cygwin'de olabilir amaç gcc'yi edinmek) ile birlikte kurun.
2. Şunu kullanarak yeni bir projeyle birlikte veya var olan bir projeyi kullanarak bir ceeding framework oluşturun:
	```shell
	ceedling new <projectname>
	```
1. Project.yml dosyasında gerekli ortam girişleri, path'lar, CMock seçenekleri, ve kullabılacak kütüphaneleri yapılandırın.
2. Tüm kaynak dosyaların project.yml içinde tanımlanan kaynak dizinde mevcut olduğundan emin olun.
3. Test edilen kaynak modül işlevselliği için birim test kodunu yazın. Gerekli tüm header dosyalarını (unity, mock header'leri) eklediğinizden emin olun.
4. Birim testi oluşturulduktan sonra, tüm birim testlerini oluşturmak ve yürütmek için şu komutu kullanın:
	```shell
	ceedling test:all
	```
	Bireysel modül testi şu şekilde yürütülebilir:
	```shell
	ceedling test:<modulemane>
	```
7. Build işleminin başlangıcında, Ceedling header dosyası fonksiyonlarını okur ve taklit başlık dosyalarını oluşturur.
8. Taklit dosyalar, mock_ başına eklenmiş olarak kaynak dosya adıyla aynı ada sahip derleme dizini altında oluşturulur. Örneğin. “display.h” için oluşturulan taklit dosya “mock_display.h” olarak adlandırılacaktır.
9. Ceedling, ilgili kaynak ve test dosyalarını birbirine bağlar ve bir çıktı (.out) dosyası oluşturur.
10. Birim testini yürütür ve beklenen sonuçları kullanılan onaylama fonksiyonlarına göre karşılaştırır.
11. Son olarak, ekranda test özetini görüntüler.