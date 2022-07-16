# CeedlingExample

Temel bir kod ve Ceedling kullanılarak birim testi yapılmıştır. Kaynak dosyalar:

Point.c:
```c
#include "point.h"
#include "display.h"

struct point MakePoint(int x, int y)
{
	struct point pt;
	pt.x = x;
	pt.y = y;
	return pt;
}
void DrawPoint(struct point pt)
{
	Draw_Int(pt.x);
	Draw_Int(pt.y);
}
```

Display.c:
```c
#include "display.h"
#include <stdio.h>

void Draw_Int(int a)
{
	TEST_IGNORE_MESSAGE("Draw Int is called with value: %d\n", a);
}
```

Point.h:
```c
#include "unity.h"
#ifndef POINT_H
#define POINT_H

struct point {
	int x;
	int y;
};

void DrawPoint(struct point);
struct point MakePoint(int, int);
#endif
```

Display.h
```c
#ifndef DISPLAY_H
#define DISPLAY_H

void Draw_Int(int);
#endif
```

Bu, point modülünün fonksiyonunu çağırarak display modülünün işlevselliğini kullandığı iki point ve display kaynak modülü içerir. point.c'de gösterildiği gibi, MakePoint() ve DrawPoint() olmak üzere iki kaynak kodu fonksiyonu içerir.

Burada MakePoint(), bağımsız değişken değerlerini struct değişkenine atar, oysa DrawPoint(), display.c dosyasındaki display modülünün Draw_Int() fonksiyonunu çağırır. point.h ve display.h başlık dosyaları, kaynak fonksiyonların tanımlarını içerir.

Şimdi MakePoint() ve DrawPoint() point modülü işlevselliğini test etmek için bir kod yazalım.

Test_point.c:
```c
#include "unity.h"
#include "point.h"
#include "mock_display.h"

void setUp(void)
{
}

void tearDown(void)
{
}

void test_Makepoint_creates_new_point(void)
{
	struct point pt = MakePoint(2,4);
	TEST_ASSERT_EQUAL_INT(2, pt.x);
	TEST_ASSERT_EQUAL_INT(4, pt.y);
}

void test_MakePoint_Draw_Both_of_its_Coordinates(void)
{
	struct point pt = MakePoint(3,4);
	Draw_Int_Expect(3);
	Draw_Int_Expect(4);
	DrawPoint(pt);
}
```

Yukarıdaki birim test kodu, Point modül işlevselliğini test etmek için yazılmıştır. Display modülü, point modülü işlevselliğini test etmek için taklit edildi, bu nedenle “point.h” ve “mock_display.h” dahil edildi.

Bu test kodu herhangi bir initialization/de-initialization gerektirmez, bu nedenle setUp ve TearDown fonksiyonları boştur. Birim test koduna yazılan iki test fonksiyonu vardır.

test_Makepoint_creates_new_point(), Makepoint()'in tamsayı değerleriyle çağrıldığını ve yapı değişkenlerine doğru değerlerin atandığını kontrol etmek için birlik onaylama (unity assertion) fonksiyonlarını kullanır. Burada Test_point.c dosyasının 15. satırında bilinen girdiler olarak MakePoint(2,5)'i çağırır. point.c satırı 6-8'de gösterildiği gibi, structure pt'nin değişkenleri, sağlanan giriş değerleriyle atanır. Şimdi 16-17 (test_point.c) satırlarında pt'nin x ve y değişkenlerinin değerlerini kontrol ettiğinde test geçilmiş oluyor..

DrawPoint() fonksiyonun beklenen değerlerle display biriminden Draw_Int() işlevini çağırdığını test etmek için başka bir test işlevi test_MakePoint_Draws_Both_of_its_Coordinates() oluşturulur. Bu işlev, bilinen değerlerle (3,4) MakePoint() işlevini ve pt yapısıyla DrawPoint() işlevini çağırır.

DrawPoint(pt)'in x ve y değeriyle Draw_Int() fonksiyonunu çağırdığı işlevselliği test etmek için, Test_point.c'nin 23-24 satırında gösterildiği gibi birlik onaylaması (unity assertion) Expect kullanılır. point.c satırı 12'de görüldüğü gibi, DrawPoint(), argüman olarak yapı değişkeni ile display.c'den Draw_Int() işlevini çağırır. Bu test, DrawPoint(), beklenen değerlerle Draw_Int()'i çağırdığında geçecektir. Sonuç penceresinden bir kesit:
```text
--------------------
OVERALL TEST SUMMARY
____________________
TESTED:  2
PASSED:  2
FAILED:  0
IGNORED: 0
```

Şimdi test framework'un davranışını ve sonuçlarını görmek için point modülünün birim test kodunu değiştirelim. Bu test (aşağıda verilmiştir), DrawInt() çağrılarının sırasını kontrol etmek için kullanılır.

Test_point.c
```c
#include "unity.h"
#include "point.h"
#include "mock_display.h"

void setUp(void)
{
}

void tearDown(void)
{
}

void test_Makepoint_creates_new_point(void)
{
	struct point pt = MakePoint(2,4);
	TEST_ASSERT_EQUAL_INT(2, pt.x);
	TEST_ASSERT_EQUAL_INT(4, pt.y);
}

void test_MakePoint_Draw_Both_of_its_Coordinates(void)
{
	struct point pt = MakePoint(3,4);
	Draw_Int_Expect(4);
	Draw_Int_Expect(3);
	DrawPoint(pt);
}
```

Görüldüğü gibi test_point.c değiştirildi. Draw_Int_Expect() değerleri 23-24. satırda 3 ve 4 yerine 4 ve 3 olarak değiştirildi. DrawPoint()'in kaynak kodu uygulamasına göre, önce x değeri ve ardından y değeri ile Draw_Int()'i çağırır. Bu, beklenen ve gerçek değerlerin eşleşmediğini söyleyerek birim testinde başarısız olur.

Şimdi, aşağıdaki birim kod parçacığında gösterildiği gibi DrawPoint() öğesinin çağrılmadığı bir durumu ele alalım. Bu durumda Draw_Int()'in iki kez çağrılması beklenir ancak çağrılmayacak ve bu nedenle birim testi başarısız olacaktır.

Test_point.c
```c
#include "unity.h"
#include "point.h"
#include "mock_display.h"

void setUp(void)
{
}

void tearDown(void)
{
}

void test_Makepoint_creates_new_point(void)
{
	struct point pt = MakePoint(2,4);
	TEST_ASSERT_EQUAL_INT(2, pt.x);
	TEST_ASSERT_EQUAL_INT(4, pt.y);
}

void test_MakePoint_Draw_Both_of_its_Coordinates(void)
{
	struct point pt = MakePoint(3,4);
	Draw_Int_Expect(4);
	Draw_Int_Expect(3);
}
```