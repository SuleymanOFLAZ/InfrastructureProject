# Embedded Software Unit Testing with Ceedling
Unit Testing (Birim testi), tüm kodu küçük parçalara bölerek test etmeyi amaçlayan bir tekniktir. Bu birimler, yazılımın belirli bir yönünün davranışını kontrol etmek için doğrulanabilir. Gömülü yazılımın birim testinde yer alan en büyük zorluklardan biri, kodun donanım çevre birimleri ile etkileşime girmesidir. Çoğu durumda, birim testleri sırasında donanıma erişilemez. Donanım etkileşimini olabildiğince ince tutmak, kodun çoğunu küçük parçalara bölerek test etmeye yardımcı olur. Bu parçalar daha sonra donanım etkileşimi olmadan bağımsız olarak test edilebilir.
Ceedling, Gömülü C yazılım birimi testi için mevcut en iyi automation framework'lerden biridir. Bir build sistemi olarak çalışır ve kaynak kodu taklit etmek (mock source code) ve testleri yürütmek için işlevsellik sağlar. Ceedling build sistemi, Makefiles'e benzeyen Ruby dilindeki Rakefile'lerden oluşur. Ceedling, Ceedling işlevine ayrı ayrı katkıda bulunan üç ana yardımcı program **(Unity, CMock ve CException)** içerir.

## Unity (Unit Test Environmet)
Unity (Unit Test Environment), C dilinde yazılmış bir test framework'dür. Tek bir sorce file, iki header file ve test runner'ları oluşturmak için yardımcı araçlar içerir (her test için otomatik olarak oluşturulan test dosyaları). Unity, veri türleri (datatypes) ve bit-size, hex-value, signed-unsigned types, pointers, memory assertions ve daha fazlası veri türü nitelikleri için testleri doğrulamak amaçıyla farklı onaylama ifadeleri sağlar.
## CMock
CMock, C header dosyalarından taklit (mock) fonksiyonlar oluşturmak için bir araçtır. Her bir fonksiyon için taklitler üretir ve bunları çalışma zamanında oluşturulan yeni taklit dosyalara yerleştirir. Sağlanan CMock konfigürasyonlarını proje konfigürasyon dosyasına (project.yml) ve kaynak header dosyalarını alır.
Bunların her ikisine dayanarak, modülün her fonksiyonu için beş farklı türde taklit fonksiyon üretir. Bu beş taklit fonksiyon: **Expect, Array, Callback, CException ve Ignore**. Bunlara örnek:
```c
void DoesSomething_ExpectAndReturn(int a, int b, int toReturn);

void DoesSomething_ExpectAndThrow(int a, int b, EXCEPTION_T error);

void DoesSomething_StubWithCallback(CMOCK_DoesSomething_CALLBACK YourCallback);

void DoesSomething_IgnoreAndReturn(int toReturn);
```
Bu taklit fonksiyonlar çalışma zamanı sırasında *runner files* içerisinde oluşturulur ve bu taklit fonksiyonun isminden çıkarılacağı gibi farklı senaryolarda birim testi için kullanılabilir. Örneğin *ExpectAndReturn* dönüş değerini kontrol etmek için, *ExpectAndThrow* fonksiyondan istisnayı kontrol etmek için kullanılabilir. Genellikle teklit fonksiyonların isimleri şu şekildedir:
```text
Return_Type SourceFunctionName_MockFuntionality(args);
```
Bu taklit dosyalar, test modülü koduyla birlikte derlenir ve linklenir.
## CException
CException, istisna işleme (exception-handling) işlevleri sağlayan bir exception library'dir.

Bir ceedling projesinin dizin yapısı, bir top-level yapılandırma dosyası (project.yml) ile birlikte src, test ve build dizinlerini içerir. Bu yapılandırma dosyası (project.yml), path'lar, enviroment'ler, library'ler, CMock, Project ve daha birçok gerekli/isteğe bağlı ayar için tag'ları ve field değerlerini içerir. Bu dosya, proje oluşturma sırasında otomatik olarak oluşturulur ve proje konfigürasyonlarına göre daha fazla güncelleme gerektirir.

## Unit Test Code Format
Ceedling, test kodunun ayrıştırılması ve yürütülmesi için belirli bir formatı tanımlar. Test fonksiyonları ile birlikte header dosyaları (framework, mock module, and source headers), *setUp* ve *tearDown* fonksiyonlarını içerir. setUp fonsiyonu her testin başında çağrılırken, her testin sonunda tearDown fonksiyonu çağrılır.

Ceedling framework, test kodunu ve kaynak kodu dosyalarını tanımlamak için project.yml dosyasında tanımlanan *“test_file_prefix”* özniteliğini kullanır. Tüm test kodu dosyaları "test_file_prefix" ile başlamalıdır.Örneğin:
```yml
# project.yml dosyasından bir kesit
:test_file_prefix: test_
```
Yukarıdaki proje.yml dosyasında, "test_file_prefix", "\_test" ile tanımlanmıştır, dolayısıyla bu projedeki her test kodu dosyası "\_test" ile başlamalıdır.

Aşağıdaki kod parçası, birim test örnek dosyasını tanımlar. “unity.h(Unity framework) ve “mock\_bar.h”(Taklit fonksiyonnlar) dosyasını içerir. Burada "mock\_bar.h"nin eklenmesi, "bar.h" dosyasının kaynak dosya olduğunu ve test için taklit edilmesi gerektiğini söyler. Bu sayede CMock, kaynak kod dizininde “bar.h” dosyasını arar. Dosyayı bulduğunda, CMock, header dosyasında bulunan her bir fonksiyon için sahte fonksiyonlar içeren "mock\_bar.h" dosyasını oluşturur. Ayrıca koşucu dosyaları (runner files) oluşturur ve bunları main fonksiyonu ve diğer CMock, unity fonksiyonları içeren *test_\<testfilename\>\_runner.c* ile derleme dizinine koyar.
```c
// Header files
#include "unity.h" // compile/link in Unit test framework 
#include "mock_bar.h" // bar.h will be found mocked as mock_bar.c + compiled linked in:

// every test file requires this function:
void setUp(void){}

// every test file requires this function:
void tearDown(void){}

// a test case function
void test_Function1_should_Call_Bar(void)
{

}
```
Ceedling ayrıca kaynak kapsamı raporu (source coverage report) oluşturmak için işlevsellik sağlar. Bunu yapmak için *gcov* ve *gvcovr* modül paketi gerekir. HTML veya XML dosya formatında bir rapor oluşturmak için bu modüllerin Project.yml dosyasında yapılandırılması gerekir. Bu, test edilmemiş herhangi bir ölü kodun veya kaynak kodun keşfedilmesine yardımcı olur.