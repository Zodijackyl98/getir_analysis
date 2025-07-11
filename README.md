## PROJE KURULUM AŞAMALARI

## PostgreSQL 14/ pgAdmin4

Getir adında sıfırdan bir database kurulumu yapıldı. Bu veritabanının kurulması çok önemli çünkü gerek pgAdmin4 gerek Python üzerinden sqlalchemy modülü aracılığıyla databaseden veri sorgulamaları veya doğrudan veritabanına tablo aktarılması gibi işlemler çoğu python\_related klasörü içerisindeki scriptlerde mevcut.

## Python/Anaconda

Proje boyunce ihtiyacınız olacak tüm modüllerin bir çıktısını requirements.txt adlı dosyada bulabilirsiniz. İçerisinde sadece Spyder-Kernels ve bu modülün gereksinimleri fazlalıktır. Python 3.12.11 sürümü kullanılarak hazırlanmıştır ve modüller arası bir çakışma yaşanmamıştır. Sıfırdan bu proje için oluşturulan virtual environment Anaconda ile kurulmuş olup Conda 23.9.0 sürümü kullanılmıştır.

## QGIS

Proje boyunca QGIS 3.30.0-'s-Hertogenbosch sürümü kullanılmıştır. Çalışma boyunca yoğun saatlere karşılık hiçbir çökme ile karşılaşılmamıştır. Ekstra bir plugin gereksinimi yoktur. PostgreSQL getir veritabanı, Data Source Manager aracılığıyla QGIS’e kaydedilmelidir. Bu adım, projede sıkça kullanılmasının yanı sıra projenin kapatılıp yeniden sorunsuz açılması için önemli.

## SQL scriptleri

Getir/SQL related klasöründen bu dosyalara ulaşılabilir. İlk aşamada `/getir/python_related/ push.py` dosyası çalıştırılarak hem siparis hem de warehose csv dosyaları postgreSQL sistemine aktarılır. Aktarımın ardından `/getir/sql_related/getir_create_geom.sql` scripti adım adım takip edilir. `/getir/python_related/getir_data.py` çalıştırılır. Hali hazırda dosya içerisinde bulacağınız bursa\_district.geojson dosyasini OSM kullanarak kendiniz üretecekseniz Multipolygon tipine dönüştürmeniz zorunlu bunun için scriptin en altındaki işlem uygulanıyor fakat bunun öncesinde OSM üzerinden elde ettiğiniz geojson dosyasındaki “@relations” sütununu kendiniz silmeniz gerekmektedir. Geopandas veya QGIS kullanılarak bu sorun aşılır. Sorunsuz ilerlenilirse Geojson çıktısı PostgreSQL veritabanına aktarılır. Tamamlanmasını ardından `/sql_related/py/getir_dist.sql` scriptinin takip edilmesi gerekiyor. `./getir_query.sql` dosyası veriler üretilirken yapılan sorguları içeren dosyadır. Yalnızca sorgu dosyası olmakla beraber kullanılmaması bir aksaklık yaratmaz. SQL dosyalarının içerisindeki kod bloklarının teker teker çalıştırılması olası hataların önüne geçecektir.

## Python Scriptleri 
   - Bu aşamada işlemleri belli bir başlık altında toplaması zor çünkü hepsi bir arada kullanılmaya başlanacak. `/python_related/getir_service_ors.py` scripti çalıştırılır. Heigit üzerinden sonraki aşamalarda rota hesaplanması için gerekli OpenRouteService(ORS) API keyinın veri üretmeyi planlayacak kişiler için zorunlu olduğunu belirteyim. Key için `/getir/python_related/` klasörü altında .env dosyasının oluşturulması gerekmektedir veya kendi anahtarınızı yapıştırabilirsiniz. 24 saatte bir sorgu limitleriniz sorgu çeşitlerine göre yenilenmektedir. Tüm projenin oluşturulmasında herhangi bir limit aşımı söz konusu olmamıştır. Script ile üretilen yalnızca geojson dosyasının PostgreSQL’e aktarımı yapılmalıdır, diğer tüm dosyalar otomatik olarak içeri aktarılmaktadır. Proje QGIS üzerinden hiçbir csv açma zorunluluğu içermez, tek seferlik **elde edilen geojson formatındaki çıktılar PostgreSQL’e aktarıldıkları koşuluyla**.
   - Aynı klasör içerisinden `getir_service_ors_bicyle.py` çalıştırılarak aynı işlem bisiklet senaryosuna göre gerçekleştirilir, geojson çıktısının PostgreSQL’e aktarılması gerekir.
   - `ors.compare.py` ile iki farklı araç senaryosu içerisinden zaman ve mesafeye göre hangisinin avantajlı olduğunu gösteren tabloyu oluşturur. Script sonunda oluşturulan CSV opsiyoneldir, kullanımı zorunlu değildir.
   - `pipe.py` Kendi SQL sorgularınızı çalıştırıp DataFrame’e dönüştürebileceğiniz tamamen opsiyonel bir scripttir.
   - `shortest.py` iki koordinat çifti arasıdaki mesafe ve süresinin hesaplayabileceğinz basir bir script, tamamen opsiyonel.
   - `service_point_needed.py`, “getir\_service\_ors.py” çıktısı olan `sip_war_with_routes.csv` dosyasındaki noktaları kullanarak istenilen servis noktasının sayısına göre Kmeans kullanarak işlem sonucunda geojson çıktısı veren script.
   - `service_point_isochrone[median,min,half_median].py` scripleri ORS kullanılarak isochrome haritaları oluşturmak için kullanılıyor. Farklı scriptlerin oluşturulmasındaki amaç “delivery\_duration” yani teslimat süresinden elde edilen farklı istatistiksel verilere göre farklı haritaların elde edilmesi. Hepsi veya tercih etmek istediğiniz arasından bir tanesi ile çalışılabilir hatta hiç kullanılmayada bilir.
   - `siparis_bursa_valid.py` PostgreSQL’de bulunan “siparis” tablosu ile “bursa\_mahalle\_valid” tablolarını birleştirip, geojson formatında kaydediyor. Tamamen opsiyonel ilerleyen aşamalara bir katkısı yoktur.
   - `neighbourhood_order_count.py` Mahalle bazlı toplam sipariş sayılarını QGIS üzerinden gösterme amaçlı iki farklı PostgreSQL sorgusunu birleştirip, “order\_counts\_by\_hood.geojson” çıktısını üreten script.
   - `district_order_count.py` İlçe bazlı sipariş sayısının oluşturulması için postgreSQL sorgusu çalıştırıp, çıktıyı “district\_order\_count.geojson” olarak kaydeder.
   - `gen_df_then_to_postgre` Mahalle bazlı nüfus bilgisi bu proje içerisinde edinilmesi en güç veri oldu, yalnızca veriye ulaşım değil güncel veriye ulaştıktan sonrada standart dışı oluşturulmuş csv dosyalarını düzenleyerek, düzenleme sonrası mahalle adlarında yaşanabilecek ufak değişiklikleri yakalayarak doğru mahallelere atanmasını sağlayan PostgreSQL sorgusunu çalıştırır. Sorgu sonrası `mahalle_pop_matched.geojson` dosyası ilişkili mahelle nüfus değerlerini ve mahalle bölgelerini içerisinde barındırır.