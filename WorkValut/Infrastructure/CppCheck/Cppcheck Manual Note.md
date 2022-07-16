# CppCheck Manual Note
Cppcheck, C/C++ için bir analiz aracıdır. Hataları, tanımsız davranışları ve tehlikeli kodlama yalarını bulmaya odaklanır. Cppcheck C/C++ kodumuzu belirli bir syntax standardı olmasa bile (gömülü projelerde yaygın olduğu gibi) analiz etmek için tasarlandı.

### Statik Analiz Hakkında
Statik analiz ile şu tip hataları bulabiliriz.
- Tanımsız davranış
- Tehlikeli kodlama paterni kullanma
- Kodlama sitili

Statik analiz ile bulamayacağımız birçok hata vardır. Statik analiz araçları, kodumuzun ne yapmak istediği hakkında bir insan bilgisine sahip değildir. Eğer programımızın çıktısı geçerli fakat beklendiği gibi değilse, bu statik analiz aracı ile bulunabilecek bir hata değildir.
Statik analiz araçları vencemizin bir tamamlayıcısı olarak kullanılmalıdır. Şunların hiçbirinin yerini tutamaz;
- Dikkatli dizayn
- Test etme
- Dinamik analiz
- fuzzing

___
## Başlarken
### GUI
Project Settings penceresinde ilk seçeneğimiz *Import Project*'dir. Eğer bu özelliği kullanabiliyorsak, kullanmamız önerilir. Cppcheck şunları import edebilir:
- Visual Studio projesi
- CMake/qbs/etc gibi build dosyalarından üretilebilecek *Compile database*
- Borland C++ Builder 6

Proje ayarlarını doldurduktan sonra OK' basarak analize başlayabiliriz.
### Command line
Basitce bir .c dosyasını vererek analizi gerçekleştirebiliriz.
```shell
cppcheck file.c
```
#### Bir klasördeki tüm dosyaları kontrol etmek
Cppcheck'e path olarak bir klasör verirsek, cppcheck klasördeki içiçe tüm kaynak dosyalrını tarayacaktır ve analize alacaktır.

#### Dosyaları manuel olarak kontrol etmek yada proje dosyası kullanmak
Cppcheck ile dosya veya yolları ve ayarları belirterek dosyaları manuel olarak kontrol edebiliriz. Yada CMake, Visual Studio gibi build enviroment'ler kullanabiliriz.
Hangi yaklaşımın (proje dosyası veya manuel konfigürasyon) daha içi sonuç vereceğini bilemiyoruz. İki yaklaşımında denenmesi tavsiye edilir. Farklı sonuçlar almamız mümkündür, bu sebeple mümkün olan en fazla hatayı tespit edebilmek için içi yaklaşımıda kullanmamız gerekir.
#### Verilen bir filtre ile dosyaları kontrol etme
*--file-filter=str* ile bir dosya filtresi uygulayabiliriz. Filtre ile uyumlu dosyalar kontrol edilecektir.
Örnek olarak yanlızca *src/ alt* dosyasındakı *test* ile başlayan dosyaları kontrol etmek istiyoruz; bu durumda şunu deneyebiliriz.
```shell
cppcheck src/ --file-filter=src/test*
```
Bu durumda cppcheck src/'deki dosyaları toplayacak ve bundan sonra fitre uygulayacaktır. Yani filtre verilen başlangıç klasörüyle başlamalıdır.
#### Bir klasör veya dosyayı kontrolden çıkartmak
Bir klasör veya dosyayı kontrolden çıkarmanın iki yolu vardır. İlk seçenek yanlızca kontrol edilmesi istenilen dosya ve yolları vermektir:
```shell
cppcheck src/a src/b
```
Bu yöntemle yanlızca *src/a* ve *src/b* altındaki dosyalar kontrol edilecektir.
İkinci seçenek görmezden gelinecek dosya ve yolları *-i* ile belirtmektir:
```shell
cppcheck -isrc/c src
```
Bu yöntem ile *scr* altındaki dosyalar kontrol edilirken *src/c* altındaki dosyalar görmezden gelinecektir.
Bu seçenek yanlızda verilen bir yol için geçerlidir. Birçok yolu görmezden gelmek için her birine ayrı ayrı *-i* flag'ı verilmelidir.
```shell
cppcheck -isrc/b -isrc/c
```
Bu yöntem ile hem *src/b* hem de *src/c* yolu görmezden gelinecektir.
#### Clang parser (deneyimsel)
Varsayılan olarak Cppcheck dahili *C/C++ parser* kullanmaktadır. Buna rağmen Clang parser'i yerine kullanabileceğimiz deneyimsel bir seçenek vardır.
Clang'ı yükle ve daha sonra *--clang* Cppcheck opsiyonunu kullan.
Teknik olarak Cppcheck, clang'ı *-ast-dump* opsiyonu ile yürütecektir. Daha sonra clang çıktısı aktarılıp normal Cppcheck formatına çevirilecektir. Sonuç olarak Cppcheck analizi bunun üzerinde gerçekleşir.
*--clang=clang-10* örneğini kullanarak, seçeneklere custom bir Clang yürütülebiliri de verebiliriz. Bunu aynı zamanda path'ı ile birlikte de verebiliriz. Windows'da path kullanmadığımız sürece .exe uzantısını sonuna ekleyecektir.
### Ciddiyet
Mesajlar için var olan ciddiyet seviyeleri şunlardır:
**error**
Kod yürütülürken, memory leak, resource leak gibi tanımsız bir davranış veya başka bir hata varsa.
**warning**
Kod yürütülürken tanımsız bir davranış olabilir.
**style**
unused functions, redundant code, constness, operator precedence, possible mistakes gibi sitilistik meseleler varsa.
**performance**
Yaygın bilgiye dayalı run-time performans önerileri. Yine de bu mesajları düzeltilerek ölçülebilir bir hız değişimi kazanılması kesin değildir.
**portability**
Taşınılabilirlik uyarıları. İmplementasyon tanımlı davranış. 64-bit uyumluluğu.
**information**
Sözdizimsel doğruluk ile alakası olmayan konfigürasyon problemleri, fakat kullanılan Cppcheck konfigürasyonları iyileştirilebilir.
### Şablon kodunu olası hızlandırma analizi
Cppcheck kodumuzdaki şablonları (templates) örneklendirir.
Eğer şablonumuz içiçe ise bu çok fazla hafıza kullanıma yol açacak şekilde analizi yavaşlatır. Cppcheck potansiyel problemler olduğunda bilgilendirme mesajları yazacaktır.
Örnek kod:
```c
template <int i>
void a() 
{ 
	a<i+1>0(); 
} 
void foo()
{
	a<0>();
}
```
Cppcheck çıktısı:
```
test.cpp:4:5: information: TemplateSimplifier: max template recursion 
	(100) reached for template 'a<101>'. You might want to limit Cppcheck 
	recursion. [templateRecursion] 
	a<i+1>(); 
	^
```
Görüleceği gibi Cppcheck a<i+1>'i a<101>'e kadar örnekledi, sonra çıktı.
Şablon içiçe örneklemesini limitlemek için:
- *Template specialisation* ekle
- Cppcheck'i yapılandır. (GUI üzerinden halledilebilir)

*Template specialisation* kod örneği
```c
template <int i>
void a() 
{ 
	a<i+1>(); 
} 

void foo() 
{ 
	a<0>(); 
} 

#ifdef __cppcheck__ 
template<> void a<3>() {} 
#endif
```
Kodu kontrol ederken *-D\__cppcheck__* kullanabiliriz.

---
## Cppcheck build folder
Cppceck build klasörü kullanmak zorunluluk değildir fakat tavsiye edilir.
Cppcheck analiz bilgisini bu klasörde depolar.
Faydaları:
- Incremental analizi mümkün kıldığı için analizi hızlandırır. Tekrar analizlerde yanlızca değişmiş dosyalar analiz edilir.
- Birden fazla thread kullanıldığında, tüm program analizi

Komut satırında*--cppcheck-build-dir=path* ile konfigüre edilebilir. Örnek:
```shell
mkdir b
cppcheck --cppcheck-build-dir=b src # <- All files are analyzed 
cppcheck --cppcheck-build-dir=b src # <- Faster! Results of unchanged
	files are reused
``` 
---
## Proje Import etme
Bazı proje dosyalarını ve build konfigürasyonlarını Cppcheck'e import edebiliriz. Cppcheck'e proje import etmek için *--project=...* argümanını kullanırız.
### Cppheck GUI Projesi
Komut satırı üzerinden Cppcheck GUI projesini import edebilir ve kullanabiliriz.
```shell
cppcheck --project=foobar.cppcheck
```
Cppcheck GUI, komut satırında direk olarak olmayan bazı seçeneklere sahiptir. Bu seçeneklere sahip olmak için GUI proje dosyası import edebiliriz. Komut satırı aracının kullanımı kasıtlı olarak basit tutulmuştur ve bu nedenle seçenekler sınırlıdır.
Projedeki belirli klasörleri yok saymak için -i kullanabilirsiniz. Bu, foo klasöründeki kaynak dosyaların analizini atlayacaktır.
```shell
cppcheck --project=foobar.cppcheck -ifoo
```
### CMake
ilk önce bir **compile database** üretmemiz gerekir. Bunun için:
```shell
cmake -DCMAKE_EXPORT_COMPILE_COMMANDS=ON .
```
Bulunan klasörde *compile_commands.json* dosyası üretilir. Sonra Cppcheck'i şu şekilde çalıştırabiliriz:
```shell
cppcheck --project=compile_commands.json
```
Herhangi bir dosyayı görmezden gelmek için *-i* ile bahsedebiliriz.
### Visual Studio
Cppcheck'i özel olarak proje dosyasında (\*.vcxproj) yada tüm solution'da (\*.sln) çalıştırabiliriz.
Cppcheck'i tüm Visual Studio solution'da çalıştırmak için:
```shell
cppcheck --project=foobar.sln
```
Cppcheck'i Visual Studio projesinde çalıştırmak için:
```shell
cppcheck --project=foobar.vcxproj
```
İki seçenekte proje veya projelerdeki olası tüm konfigürasyonları değerlendiracektir. Bir konfigürasyona limitlemek için:
```shell
cppcheck --project=foobar.sln "--project-configuration=Release|Win32"
```
### C++ Builder 6
Cppcheck'i C++ Builder 6 projesinde çalıştırmak için:
```shell
cppcheck --project=foobar.bpr
```

### Diğer build yapıları
Eğer bir *compile database* oluşturabiliyorsak, bunu Cppcheck'e import etmek olasıdır. Örneğin diğer derleme araçlarından bir compile database üretmek için *BEAR* aracı kullanılabilir.
```shell
bear make
```
---
## Preprocessor Ayarları
Eğer *--project* kullanıyorsak Cppcheck import edilen proje dosyasındaki preprocessor ayarlarını otomatik olarak kullanacaktır ve ekstra olarak bir konfigürasyon yapmaya gerek olmaması olasıdır.
Eğer *--project* kullanmıyorsak, biraz manuel preprocessor ayarı gerekli olabilir. Bunarağmen Cppheck define'ların otomatik konfigürasyonuna sahiptir.
### Preprocessor define'ların otomatik konfigürasyonu
Cppcheck, analizde mümkün olduğunca yüksek kapsama alanı elde etmek için farklı preprocessor define'larını kombinasyonlarını otomatik olarak test eder.
Örnek olarak 3 hata içeren bir dosya (x,y,z atandığında):
```c
#ifdef A 
	x=100/0; 
	#ifdef B 
		y=100/0; 
	#endif 
#else 
	z=100/0; 
#endif 

#ifndef C 
#error C must be defined 
#endif
```
*-D* bayrağı Cppcheck'e bir adın tanımlandığını söyler. Bu tanımlama olmadan Cppcheck analizi olmayacaktır. *-U* bayrağı Cppcheck'e bir adın tanımlanmadığını söyler. Bu tanımla birlikte Cppcheck analizi olmayacaktır. 
*--force* ve *--max-configs* bayrakları kaç kombinasyonun kontrol edildiğini kontrol etmek için kullanılır. *-D* kullanıldığında, bunlar kullanılmadıkça Cppcheck yalnızca 1 yapılandırmayı kontrol eder.
Örnek:
```shell
cppcheck test.c => test all configurations => all bugs are found 
cppcheck -DA test.c => only test configuration "-DA" => No bug is found 
	(#error) 
cppcheck -DA -DC test.c => only test configuration "-DA -DC" => The first 
	bug is found 
cppcheck -UA test.c => The configuration "-DC" is tested => The last bug is found cppcheck --force -DA test.c => All configurations with "-DA" are tested => 
	The two first bugs are found
```
### Include paths
Bir Include Path eklemek için '-I' ve devamında path girilmelidir.
Cppcheck'in preprocessor'ü basitce include'leri diğer preprocessor'ler gibi ele alır. Ancak, diğer preprocessor'ler bir eksik header ile karşılaştıklarında dururken, Cppcheck bir bilgilendirme mesajı yazar ve ayrıştırmaya devam eder.
Bu davranışın amacı, Cppcheck'in kodun tamamını görmeden çalışması gerektiğidir. Aslında tüm include path'ların verilmesi önerilmez. Cppcheck için üyelerinin implementasyonunu kontrol ederken bir class bildirimini görmek faydalı olsa da, standart kütüphane header'larını vermek önerilmez, çünkü analiz tam olarak çalışmaz ve daha uzun bir kontrol süresine neden olur. Bu gibi durumlarda, .cfg dosyaları, fonksiyonların ve type'lerin Cppcheck'e uygulanması hakkında bilgi sağlamanın tercih edilen yoludur.

---
## Platform
Hedef ortamla eşleşen platform konfigürasyonları kullanmalıyız. 
Eğer kod lokal olarak derlenip yürütülyorsa, Cppcheck varsayılan olarak düzgün çalışan yerli platform konfigürasyonlarını kullanır. 
Cppcheck Unix ve Windows hedefleri için yerleşik konfigürasyonlara sahiptir. Bunları *--platform* bayrağı ile birlikte kolaylıkla kullanabiliriz.
Aynı zamanda kendi custom platform konfigürasyonlarımızı XML dosyasında oluşturabiliriz.
```xml
<?xml version="1"?>
<platform>
	<char_bit>8</char_bit>
	<default-sign>signed</default-sign>
	<sizeof>
		<short>2</short>
		<int>4</int>
		<long>4</long>
		<long-long>8</long-long>
		<float>4</float>
		<double>8</double>
		<long-double>12</long-double>
		<pointer>4</pointer>
		<size_t>4</size_t>
		<wchar_t>2</wchar_t>
	</sizeof>
</platform>
```
---
## C/C++ Standard
Komut satırında bir C/C++ standardından bahsetmek için*--std* kullanabiliriz.
Cppcheck kodun en son C/C++ standardı ile uyumlu olduğunnu varsayar, fakat bunu değiştirmek mümkündür.
Kullanılabir seçenekler şunlardır:
- c89: C code is C89 compatible 
- c99: C code is C99 compatible 
- c11: C code is C11 compatible (default) 
- c++03: C++ code is C++03 compatible 
- c++11: C++ code is C++11 compatible 
- c++14: C++ code is C++14 compatible 
- c++17: C++ code is C++17 compatible 
- c++20: C++ code is C++20 compatible (default)
---
## Cppcheck build dir
Cppcheck build dir kullanmak iyi bir fikirdir. Komut satırında *--cppcheck-build-dir* ile kullanabiliriz. GUI de build dir proje seceçenleri arasından yapılandırılabilir.
Kodu tekrar kontrol etme çok daha hızlı olacaktır. Cppcheck değişmemiş kodu analiz etmez. Eski uyarılar buid dir'den yüklenir ve rapor edilir.
Cppcheck build dir kullanmadığımız sürece, çoklu thread kullanıldığı zaman tüm program analizi mümkün olmayacaktır. Örnek olarak, *unusedFunction* uyarısı tüm program analizi gerektirmektedir.

---
## Suppressions
Eğer bazı hataları üretilmeden fitrelemek istersek, bunları baskılamak mümkündür.
### Plain text suppressions
Hata susturma biçimi aşağıdakilerden biridir:
```
[error id]:[filename]:[line] 
[error id]:[filename2] 
[error id]
```
*error id* burada susturmak istediğimiz hatadır. Bunu elde etmenin en kolay yolu *-template=gcc* komut satırı bayrağını kullanmaktır. Id braket içinde gösterilir.
Dosya ismi sırasıyla herhangi bir karakter dizisiyle veya herhangi bir tek karakterle eşleşen, wildchard karakterleri *\* yada ?* içerebilir. Tüm sistemlerde path ayırıcı olarak *"/"* kullanılması tavsiye edilir. Dosya ismi, rapor edilen uyarı mesajındaki dosya ismiyle bire bir uyuşmalıdır. Örnek olarak, eğer uyarı relative path içeriyorsa susturma bu relative path ile eşleşmelidir.
### Command line suppression
*--suppress=* komut satırı seçeneği, komut satırında susturma belirtmeye yarar.Örnek:
```shell
cppcheck --suppress=memleak:src/file1.cpp src/
```
### Suppression in a file
Aşağıdaki örnekteki gibi bir susturma dosyası hazırlayabiliriz:
```text
// suppress memleak and exceptNew errors in the file src/file1.cpp 
memleak:src/file1.cpp 
exceptNew:src/file1.cpp 

uninitvar // suppress all uninitvar errors in all files
```
Susturma dosyalarına boş satır veya yorum satırı ekleyebiliriz. Yorumlar *#* veya *//* ile başlamalıdır ve yeni bir satır başında veya bir susturma satırından sonda olabilir.
Bastırma dosyasının kullanımı şu şekildedir:
```shell
cppcheck --suppressions-list=suppressions.txt src/
```
### XML Suppressions
Bastırmaları bir XML dosyası ile belirtebiliriz. Örnek:
```xml
<?xml version="1.0"?>
<suppressions>
	<suppress>
		<id>uninitvar</id>
		<fileName>src/file1.c</fileName>
		<lineNumber>10</lineNumber>
		<symbolName>var</symbolName>
	</suppress>
</suppressions>
```
XML formatı genişletilebilir, ve ilerde başka niteliklerle genişletilebilir.
XML suppression dosyasının kullanımı şu şekildedir:
```shell
cppcheck --suppress-xml=suppressions.xml src/
```
### Inline Suppressions
Susturmalar özel anahtar sözcükler içeren yorum satırları ile direk olarak koda eklenebilir. Yorum eklemenin kod okunabilirliğini azaltabileceğini unutmamak gerekir.
Şu kod normalde bir hata mesajı üretir:
```c
void f() { 
	char arr[5]; 
	arr[10] = 0; 
}
```
Çıktı:
```shell
cppcheck test.c 
[test.c:3]: (error) Array 'arr[5]' index 10 out of bounds
```
Inline susturmaları aktive etmek için:
```shell
cppcheck --inline-suppr test.c
```
#### Format
Bir *aaaa* uyarısını şunula susturabiliriz:
```c
// cppcheck-suppress aaaa
```
Bir yorumda birçok uyarıyı susturmak için [] kullnanabiliriz:
```c
// cppcheck-suppress [aaaa, bbbb]
```
#### Koddan önce veya aynı satırda yorum
Yorum koddan önce veya aynı satıra eklenebilir.
Koddan önce:
```c
void f() { 
	char arr[5]; 
	// cppcheck-suppress arrayIndexOutOfBounds 
	arr[10] = 0; 
}
```
Yada aynı satırda şu şekilde:
```c
void f() { 
	char arr[5]; 
	arr[10] = 0; // cppcheck-suppress arrayIndexOutOfBounds 
}
```
Bu örnekte 2 satır kod ve bir bastırma yorumu vardır. Bastırma yanlızca 1. satıra: a = b + c 'ye uygulanır.
```c
void f() { 
	a = b + c; // cppcheck-suppress abc 
	d = e + f; 
}
```
Geriye dönük uyumluluk için özel bir durum olarak, kendi satırında bir { ve bundan sonra bir bastırma yorumunuz varsa, bu hem mevcut hem de sonraki satır için uyarıları bastıracaktır. Bu örnek, hem *{* satırı hem de *a = b + c* satırı için abc uyarılarını bastıracaktır:
```c
void f() 
{ // cppcheck-suppress abc 
	a = b + c; 
}
```
#### Çoklu Suppressions
Bir kod satırı için bastırmak istediğimiz birden fazla uyarı olabilir.
Bunun için birkaç seçenek vardır:
Koddan önce iki bastırma yorumu kullanmak:
```c
void f() { 
	char arr[5]; 
	// cppcheck-suppress arrayIndexOutOfBounds
	// cppcheck-suppress zerodiv 
	arr[10] = arr[10] / 0; 
}
```
Koddan önce *[]* ile birlikte bir bastırma yorumu kullanmak:
```c
void f() { 
	char arr[5]; 
	// cppcheck-suppress[arrayIndexOutOfBounds,zerodiv] 
	arr[10] = arr[10] / 0; 
}
```
Bu yorumu aynı satırda yapabiliriz:
```c
void f() { 
	char arr[5]; 
	
	arr[10] = arr[10] / 0; // cppcheck-suppress[arrayIndexOutOfBounds,zerodiv] 
}
```

#### Sembol ismi
Inline susturmanın yanlızca belirli bir sembole uygulanacağını belirtebiliriz:
```c
// cppcheck-suppress aaaa symbolName=arr
```
Yada:
```c
// cppcheck-suppress[aaaa symbolName=arr, bbbb]
```
#### Susturma hakkında yorum
Bir susturma hakkında yorumu şu şekilde yazabiliriz:
```c
// cppcheck-suppress[warningid] some comment 
// cppcheck-suppress warningid ; some comment 
// cppcheck-suppress warningid // some comment
```
---
## XML Çıktı
Cppcheck XML formatında çıktı üretebilir. Bunu aktifleştermek için *--xml* kullanabiliriz.
Bir dosyayı kontrol etmek ve xml çıktısı almak için basit bir komut:
```shell
cppcheck --xml file1.cpp
```
İşte örnek bir rapor:
```xml
<?xml version="1.0" encoding="UTF-8"?>
<results version="2">
	<cppcheck version="1.66"/>
	<errors>
		<error id="someError" severity="error" msg="short error text" verbose="long 								error text" inconclusive="true" cwe="312">
			<location file0="file.c" file="file.h" line="1"/>
	</error>
	</errors>
</results>
```
### \<error> elementi
Her hata \<error> elementi içinde bildirilir. Öznitelikleri:
**id**
Hatanın id'si, ve geçerli sembol adları
**severity**
error/warning/style/performance/portability/information gibi bildirim türlerinden bitanesi
**msg**
Kısa haliyle hata mesajı
**verbose**
Uzun haliyle hata mesajı
**inconclusive**
Bu öznitelik yalnızca hata mesajı sonuçsuz olduğunda kullanılır.
**cwe**
Sorun için CWE Kimliği; bu özelliğin yalnızca mesajın CWE Kimliği bilindiğinde kullanıldığını unutmayın.
### \<location> elementi
Hata ile ilgili tüm konum bilgileril \<location> elementi ile listelenir. İlk konum bilgisi ilk listelenir.
Öznitelikler:
**file**
Dosya ismi, relative veya absolute path olması mümkündür.
**file0**
Kaynak dosyanın ismi (opsiyonel)
**line**
Satır numarası
**info**
Her lokasyon için kısa konum bilgisi (opsiyonel)

---
## Text çıktısını tekrar formatlama
Çıktıyı farklı görünecek şekilde yeniden biçimlendirmek istiyorsak, şablonları kullanabiliriz.
### Önceden tanımlı çıktı formatları
Visual Studio uyumlu çıktı almak için *-template=vs* kullanabiliriz.
```shell
cppcheck --template=vs samples/arrayIndexOutOfBounds/bad.c
```
Bunun çıktısı şu şekilde görünür:
```text
Checking samples/arrayIndexOutOfBounds/bad.c ... samples/arrayIndexOutOfBounds/bad.c(6): error: Array 'a[2]' accessed at 
	index 2, which is out of bounds.
```
gcc uyumlu çıktı almak için *-template=gcc* kullanabiliriz.
Çıktı şu şekilde görünür:
```text
Checking samples/arrayIndexOutOfBounds/bad.c ... samples/arrayIndexOutOfBounds/bad.c:6:6: warning: Array 'a[2]' accessed at 
	index 2, which is out of bounds. [arrayIndexOutOfBounds] 
a[2] = 0; 
  ^
```
### Kullanıcı tanımlı çıktı formatı (tek satır)
Kendi paternimizi yazabiliriz. Örneğin, geleneksel gcc gibi biçimlendirilmiş uyarı mesajları almak için aşağıdaki biçim kullanılabilir:
```text
cppcheck --template="{file}:{line}: {severity}: {message}" samples/arrayIndexOutOfBounds/bad.c
```
Çıktı şu şekilde görünür:
```text
Checking samples/arrayIndexOutOfBounds/bad.c ... samples/arrayIndexOutOfBounds/bad.c:6: error: Array 'a[2]' accessed at 
	index 2, which is out of bounds
```
Virgül ayırmalı format:
```text
cppcheck --template="{file},{line},{severity},{id},{message}" samples/arrayIndexOutOfBounds/bad.c
```
Çıktı şu şekilde görünür:
```text
Checking samples/arrayIndexOutOfBounds/bad.c ... samples/arrayIndexOutOfBounds/bad.c,6,error,arrayIndexOutOfBounds,Array 
	'a[2]' accessed at index 2, which is out of bounds.
```
### Kullanıcı tanımlı çıktı formatı (çoklu satır)
Birçok konumda birden fazla uyarı. Örnek kod:
```c
void f(int *p) 
{ 
	*p = 3; // line 3 
} 

int main() 
{ 
	int *p = 0; // line 8 
	f(p); // line 9 
	return 0; 
}
```
Satır 3'te muhtemel null pointer referansı var. Cppcheck bu sonuca nasıl vardığını ekstra konum bilgisi vererek gösterebilir. Komut satırında hem *-template* hemde *-template-location* kullanmalıyız.
 ```shell
 cppcheck --template="{file}:{line}: {severity}: {message}\n{code}" 
 	--template-location="{file}:{line}: note: {info}\n{code}" multiline.c
 ```
 Cppcheck çıktısı şöyle olur:
 ```text
 Checking multiline.c ... 
 multiline.c:3: warning: Possible null pointer dereference: p 
 	*p = 3; 
	 ^ 
multiline.c:8: note: Assignment 'p=0', assigned value is 0 
	int *p = 0; 
			 ^ 
multiline.c:9: note: Calling function 'f', 1st argument 'p' value is 0 
	f(p); 
	  ^ 
multiline.c:3: note: Null pointer dereference 
	*p = 3;
	 ^
 ```
 Uyarıdaki ilk satır -template formatına göre formatlanmıştır.
 Uyarıdaki diğer satırlar -template-location formatına göre formatlanmıştır.
 #### -template için format belirteçleri
 *-template* için kullanılabilecek belirteçler:
 **{file}**
 Dosya ismi
 **{line}**
 Satır numarası
 **{column}**
 Sütun numarası
 **{callstack}**
 Tüm konumları yaz. [{file}:{line}] formatında yazılan her konum ve -> ile ayrılan her konum. Örnek olarak şu şekilde gözükebilir: [multiline.c:8] -> [multiline.c:9] -> [multiline.c:3]
 **{inconclusive:text}**
 Eğer uyarı sonuçsuzsa, verilen text yazılır. Verilen text { içermeyen herhangi bir text olabilir. Örneğin: {inconclusive:inconclusive,}
 **{severity}**
 error/warning/style/performance/portability/information
 **{message}**
 Uyarı mesajı
 **{id}**
 Uyarı id'si
 **{code}**
 Asıl kod
 **\t**
 Tab
 **\n**
 New line
 **\r**
 Carriage Return
 #### -template-location için format belirteçleri
 **{file}, {line}, {column}, {info}, {code}, \t, \n, \r***
 
 ---
 ## Addons
Eklentiler, güvenli kodlama standartlarıyla uyumluluğu kontrol etmek ve sorunları bulmak için Cppcheck dump dosyalarını analiz eden script dosyalarıdır.
Cppheck aşağıda listelenen bazı ekler ile dağıtılır.
### Desteklenen eklentiler
#### cert.py
cert.py, güvenli programlama standardı SEI CERT ile uyumluluğu kontrol eder.
#### misra.py
misra.py, gömülü sistemler için geliştirilmiş, şüpheli kodlardan kaçınmak için özel bir kurallar dizisi olan MISRA C 2012 ile uyumluluğu doğrulamak için kullanılır.
Bu standart tescillidir ve açık kaynak araçlarının Misra kural metinlerini dağıtmasına izin verilmez. Bu nedenle Cppcheck'in kural metinlerini doğrudan yazmasına izin verilmez. Cppcheck'in kuralları dağıtmasına ve ihlal edilen her kuralın kimliğini görüntülemesine izin verilir (örneğin, [c2012-21.3]). İlgili kural metni de yazılabilir, ancak bunu bizim sağlamamız gerekir. Kural metinlerini (https://www.misra.org.uk)'dan satın almamız gerekir. PDF'deki *“Appendix A - Summary of guidelines”* bölümündeki kural metinlerini kopyalarsanız ve bunları bir metin dosyasına yazarsanız, Cppcheck bu metin dosyasını kullanarak uygun uyarı mesajlarını yazabilir.
Metin dosyasının nasıl biçimlendirilebileceğini görmek için burada listelenen dosyalara bakabiliriz:  https://github.com/danmar/cppcheck/blob/main/addons/test/misra/. Kural metin dosyanızı belirtmek için *--rule-texts* seçeneğini kullanabilirsiniz.
Desteklenen kuralların tam listesi Cppcheck ana sayfasında bulabiliriz.
#### y2038.py
y2038.py, *year 2038 problem safety* için Linux sistemlerini kontrol eder.
#### threadsafety.py
threadsafety.py, birden çok iş parçacığı tarafından kullanılan *static local objects* gibi iş parçacığı güvenliği sorunlarını bulmak için Cppcheck dump dosyalarını analiz eder
### Eklenti çalıştırma
Eklentiler aşağıdaki gibi kumut satırı ile çalıştırılabilir:
```shell
cppcheck --addon=misra.py somefile.c
```
Bu, tüm Cppcheck kontrollerini başlatacak ve ayrıca seçilen eklenti tarafından sağlanan belirli kontrolleri çağıracaktır.
Bazı eklentiler ekstra argümanlara ihtiyaç duyar. Json dosyasında bir eklentiyi nasıl yürüteceğimizi yapılandırabiliriz. Örneğin:
```json
{
	"script": "misra.py",
	"args": [
		"--rule-texts=misra.txt"
	]
}
```
Daha sonra bu konfigürasyon Cppcheck komut satırında şu şekilde yürütülebilir:
```shell
cppcheck --addon=misra.json somefile.c
```
Varsayılan olarak Cppcheck, eklentiyi yükleme işlemi sırasında belirtilen standart path'da arar. Bu path'ı doğrudan da verebiliriz, örneğin:
```shell
cppcheck --addon=/opt/cppcheck/configurations/my_misra.json somefile.c
```
Bu, farklı projeler için birden çok yapılandırma dosyası oluşturmanıza ve yönetmenize olanak tanır.

---
## Kütüphane Yapılandırma
WinAPI, POSIX, gtk, Qt, vb. gibi harici kütüphaneler kullanıldığında, Cppcheck harici fonksiyonların nasıl davrandığını bilmez. Cppcheck daha sonra bellek sızıntıları (memory leaks), arabellek taşmaları (buffer overflows), olası null pointer referansları vb. gibi çeşitli sorunları tespit edemez. Ancak bu, yapılandırma dosyalarıyla düzeltilebilir.
### Kendi custom .cfg dosyamızı kullanma
Projemiz için kendi .cfg dosyalarınızı oluşturabilir ve kullanabiliriz. Neyi yapılandırmanız gerektiğine dair ipuçları almak için *--check-library* ve *--enable=information* kullanabiliriz.
Yapılandırma dosyalarını düzenlemek için Cppcheck GUI'deki *Library Editor*'ü' kullanabiliriz. View menüsünde bulunur.
.cfg dosya formatı hakkında daha fazlası için [Cppcheck .cfg format (sourceforge.io)](https://cppcheck.sourceforge.io/reference-cfg-format.pdf) dökümanına bakabiliriz.

---
## HTML Rapor
Cppcheck'ten gelen XML çıktısını bir HTML raporuna dönüştürebiliriz. Bunun çalışması için Python'a ve pygments modülüne (http://pygments.org/) ihtiyacımız var. Cppcheck kaynak dosyasında, bir Cppcheck XML dosyasını HTML çıktısına dönüştüren bir komut dosyası içeren bir *htmlreport* klasörü vardır.
Şu komut yardım penceresi getirir:
```shell
htmlreport/cppcheck-htmlreport -h
```
Çıktı:
```shell
Usage: cppcheck-htmlreport [options] 
Options: 
	-h, --help show this help message and exit 
	--file=FILE The cppcheck xml output file to read defects from. 
			Default is reading from stdin. 
	--report-dir=REPORT_DIR 
			The directory where the html report content is written. 
	--source-dir=SOURCE_DIR 
			Base directory where source code files can be found.
```
Örnek Kullanım:
```shell
./cppcheck gui/test.cpp --xml 2> err.xml 
htmlreport/cppcheck-htmlreport --file=err.xml --report-dir=test1 
	--source-dir=.
```