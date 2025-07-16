# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.BooleanField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.BooleanField()
    is_active = models.BooleanField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class BursaDistrict(models.Model):
    id = models.CharField(primary_key=True)
    geom = models.TextField(blank=True, null=True)  # This field type is a guess.
    field_id = models.CharField(db_column='@id', blank=True, null=True)  # Field renamed to remove unsuitable characters. Field renamed because it started with '_'.
    admin_level = models.CharField(blank=True, null=True)
    boundary = models.CharField(blank=True, null=True)
    name = models.CharField(blank=True, null=True)
    name_ar = models.CharField(db_column='name:ar', blank=True, null=True)  # Field renamed to remove unsuitable characters.
    name_az = models.CharField(db_column='name:az', blank=True, null=True)  # Field renamed to remove unsuitable characters.
    name_azb = models.CharField(db_column='name:azb', blank=True, null=True)  # Field renamed to remove unsuitable characters.
    name_be = models.CharField(db_column='name:be', blank=True, null=True)  # Field renamed to remove unsuitable characters.
    name_bg = models.CharField(db_column='name:bg', blank=True, null=True)  # Field renamed to remove unsuitable characters.
    name_bn = models.CharField(db_column='name:bn', blank=True, null=True)  # Field renamed to remove unsuitable characters.
    name_ca = models.CharField(db_column='name:ca', blank=True, null=True)  # Field renamed to remove unsuitable characters.
    name_ce = models.CharField(db_column='name:ce', blank=True, null=True)  # Field renamed to remove unsuitable characters.
    name_ceb = models.CharField(db_column='name:ceb', blank=True, null=True)  # Field renamed to remove unsuitable characters.
    name_chm = models.CharField(db_column='name:chm', blank=True, null=True)  # Field renamed to remove unsuitable characters.
    name_de = models.CharField(db_column='name:de', blank=True, null=True)  # Field renamed to remove unsuitable characters.
    name_el = models.CharField(db_column='name:el', blank=True, null=True)  # Field renamed to remove unsuitable characters.
    name_en = models.CharField(db_column='name:en', blank=True, null=True)  # Field renamed to remove unsuitable characters.
    name_eo = models.CharField(db_column='name:eo', blank=True, null=True)  # Field renamed to remove unsuitable characters.
    name_es = models.CharField(db_column='name:es', blank=True, null=True)  # Field renamed to remove unsuitable characters.
    name_fa = models.CharField(db_column='name:fa', blank=True, null=True)  # Field renamed to remove unsuitable characters.
    name_fr = models.CharField(db_column='name:fr', blank=True, null=True)  # Field renamed to remove unsuitable characters.
    name_grc = models.CharField(db_column='name:grc', blank=True, null=True)  # Field renamed to remove unsuitable characters.
    name_he = models.CharField(db_column='name:he', blank=True, null=True)  # Field renamed to remove unsuitable characters.
    name_it = models.CharField(db_column='name:it', blank=True, null=True)  # Field renamed to remove unsuitable characters.
    name_ja = models.CharField(db_column='name:ja', blank=True, null=True)  # Field renamed to remove unsuitable characters.
    name_ka = models.CharField(db_column='name:ka', blank=True, null=True)  # Field renamed to remove unsuitable characters.
    name_ko = models.CharField(db_column='name:ko', blank=True, null=True)  # Field renamed to remove unsuitable characters.
    name_ku = models.CharField(db_column='name:ku', blank=True, null=True)  # Field renamed to remove unsuitable characters.
    name_la = models.CharField(db_column='name:la', blank=True, null=True)  # Field renamed to remove unsuitable characters.
    name_lt = models.CharField(db_column='name:lt', blank=True, null=True)  # Field renamed to remove unsuitable characters.
    name_min = models.CharField(db_column='name:min', blank=True, null=True)  # Field renamed to remove unsuitable characters.
    name_ms = models.CharField(db_column='name:ms', blank=True, null=True)  # Field renamed to remove unsuitable characters.
    name_nl = models.CharField(db_column='name:nl', blank=True, null=True)  # Field renamed to remove unsuitable characters.
    name_nn = models.CharField(db_column='name:nn', blank=True, null=True)  # Field renamed to remove unsuitable characters.
    name_no = models.CharField(db_column='name:no', blank=True, null=True)  # Field renamed to remove unsuitable characters.
    name_pa = models.CharField(db_column='name:pa', blank=True, null=True)  # Field renamed to remove unsuitable characters.
    name_pl = models.CharField(db_column='name:pl', blank=True, null=True)  # Field renamed to remove unsuitable characters.
    name_ro = models.CharField(db_column='name:ro', blank=True, null=True)  # Field renamed to remove unsuitable characters.
    name_ru = models.CharField(db_column='name:ru', blank=True, null=True)  # Field renamed to remove unsuitable characters.
    name_sq = models.CharField(db_column='name:sq', blank=True, null=True)  # Field renamed to remove unsuitable characters.
    name_sr = models.CharField(db_column='name:sr', blank=True, null=True)  # Field renamed to remove unsuitable characters.
    name_sw = models.CharField(db_column='name:sw', blank=True, null=True)  # Field renamed to remove unsuitable characters.
    name_tg = models.CharField(db_column='name:tg', blank=True, null=True)  # Field renamed to remove unsuitable characters.
    name_th = models.CharField(db_column='name:th', blank=True, null=True)  # Field renamed to remove unsuitable characters.
    name_tr = models.CharField(db_column='name:tr', blank=True, null=True)  # Field renamed to remove unsuitable characters.
    name_tr_suffix = models.CharField(db_column='name:tr:suffix', blank=True, null=True)  # Field renamed to remove unsuitable characters.
    name_tt = models.CharField(db_column='name:tt', blank=True, null=True)  # Field renamed to remove unsuitable characters.
    name_uk = models.CharField(db_column='name:uk', blank=True, null=True)  # Field renamed to remove unsuitable characters.
    name_ur = models.CharField(db_column='name:ur', blank=True, null=True)  # Field renamed to remove unsuitable characters.
    name_vi = models.CharField(db_column='name:vi', blank=True, null=True)  # Field renamed to remove unsuitable characters.
    name_war = models.CharField(db_column='name:war', blank=True, null=True)  # Field renamed to remove unsuitable characters.
    name_zh = models.CharField(db_column='name:zh', blank=True, null=True)  # Field renamed to remove unsuitable characters.
    name_zza = models.CharField(db_column='name:zza', blank=True, null=True)  # Field renamed to remove unsuitable characters.
    network = models.CharField(blank=True, null=True)
    old_name = models.CharField(blank=True, null=True)
    old_name_de = models.CharField(db_column='old_name:de', blank=True, null=True)  # Field renamed to remove unsuitable characters.
    old_name_el = models.CharField(db_column='old_name:el', blank=True, null=True)  # Field renamed to remove unsuitable characters.
    old_name_es = models.CharField(db_column='old_name:es', blank=True, null=True)  # Field renamed to remove unsuitable characters.
    old_name_grc = models.CharField(db_column='old_name:grc', blank=True, null=True)  # Field renamed to remove unsuitable characters.
    type = models.CharField(blank=True, null=True)
    wikidata = models.CharField(blank=True, null=True)
    wikimedia_commons = models.CharField(blank=True, null=True)
    wikipedia = models.CharField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'bursa_district'


class BursaEduCombined(models.Model):
    education_level = models.CharField(max_length=50, blank=True, null=True)
    osmangazi = models.IntegerField(blank=True, null=True)
    nilufer = models.IntegerField(blank=True, null=True)
    yildirim = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'bursa_edu_combined'


class BursaMahalleValid(models.Model):
    id = models.CharField(primary_key=True)
    geom = models.TextField(blank=True, null=True)  # This field type is a guess.
    field_id = models.CharField(db_column='@id', blank=True, null=True)  # Field renamed to remove unsuitable characters. Field renamed because it started with '_'.
    addr_city = models.CharField(db_column='addr:city', blank=True, null=True)  # Field renamed to remove unsuitable characters.
    addr_district = models.CharField(db_column='addr:district', blank=True, null=True)  # Field renamed to remove unsuitable characters.
    admin_level = models.CharField(blank=True, null=True)
    alt_name = models.CharField(blank=True, null=True)
    boundary = models.CharField(blank=True, null=True)
    cycleway = models.CharField(blank=True, null=True)
    name = models.CharField(blank=True, null=True)
    network = models.CharField(blank=True, null=True)
    place = models.CharField(blank=True, null=True)
    type = models.CharField(blank=True, null=True)
    wikidata = models.CharField(blank=True, null=True)
    wikipedia = models.CharField(blank=True, null=True)
    district_name = models.TextField(blank=True, null=True)
    area_km2 = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'bursa_mahalle_valid'


class BursaNilPop(models.Model):
    district_name = models.TextField(blank=True, null=True)
    hood_name = models.TextField(blank=True, null=True)
    population = models.BigIntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'bursa_nil_pop'


class BursaNiluferEdu(models.Model):
    education_level_id = models.AutoField(primary_key=True)
    education_level = models.CharField(max_length=50)
    population_count = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'bursa_nilufer_edu'


class BursaOsmPop(models.Model):
    district_name = models.TextField(blank=True, null=True)
    hood_name = models.TextField(blank=True, null=True)
    population = models.BigIntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'bursa_osm_pop'


class BursaOsmangaziEdu(models.Model):
    education_level_id = models.AutoField(primary_key=True)
    education_level = models.CharField(max_length=50)
    population_count = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'bursa_osmangazi_edu'


class BursaPopAll(models.Model):
    district_name = models.TextField(blank=True, null=True)
    hood_name = models.TextField(blank=True, null=True)
    population = models.BigIntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'bursa_pop_all'


class BursaYilPop(models.Model):
    district_name = models.TextField(blank=True, null=True)
    hood_name = models.TextField(blank=True, null=True)
    population = models.BigIntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'bursa_yil_pop'


class BursaYildirimEdu(models.Model):
    education_level_id = models.AutoField(primary_key=True)
    education_level = models.CharField(max_length=50)
    population_count = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'bursa_yildirim_edu'


class DistrictOrderCount(models.Model):
    geom = models.TextField(blank=True, null=True)  # This field type is a guess.
    district_name = models.CharField(blank=True, null=True)
    sip_count = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'district_order_count'


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.SmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    id = models.BigAutoField(primary_key=True)
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class IlceBursaNufusu(models.Model):
    yil = models.IntegerField(blank=True, null=True)
    ilce = models.CharField(max_length=50, blank=True, null=True)
    ilce_nufusu = models.IntegerField(blank=True, null=True)
    erkek_nufusu = models.IntegerField(blank=True, null=True)
    kadin_nufusu = models.IntegerField(blank=True, null=True)
    nufus_yuzdesi = models.CharField(max_length=10, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ilce_bursa_nufusu'


class MahPopDensity(models.Model):
    hood_name = models.CharField(blank=True, null=True)
    district_name = models.TextField(blank=True, null=True)
    geom = models.TextField(blank=True, null=True)  # This field type is a guess.
    area_km2 = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    population = models.IntegerField(blank=True, null=True)
    pop_density = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'mah_pop_density'


class MahallePopMatched(models.Model):
    geom = models.TextField(blank=True, null=True)  # This field type is a guess.
    hood_name = models.CharField(blank=True, null=True)
    district_name = models.CharField(blank=True, null=True)
    population = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'mahalle_pop_matched'


class OrderCountsByHood(models.Model):
    geom = models.TextField(blank=True, null=True)  # This field type is a guess.
    name = models.CharField(blank=True, null=True)
    district_name = models.CharField(blank=True, null=True)
    hood_name = models.CharField(blank=True, null=True)
    sip_count = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'order_counts_by_hood'


class Routes(models.Model):
    geom = models.TextField(blank=True, null=True)  # This field type is a guess.
    index = models.CharField(blank=True, null=True)
    longitude_s = models.FloatField(blank=True, null=True)
    latitude_s = models.FloatField(blank=True, null=True)
    longitude_w = models.FloatField(blank=True, null=True)
    latitude_w = models.FloatField(blank=True, null=True)
    route_km = models.FloatField(blank=True, null=True)
    route_min = models.FloatField(blank=True, null=True)
    route_geometry = models.TextField(blank=True, null=True)  # This field type is a guess.
    route_mid_lon = models.FloatField(blank=True, null=True)
    route_mid_lat = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'routes'


class ServicePoints(models.Model):
    geom = models.TextField(blank=True, null=True)  # This field type is a guess.
    longitude_sp = models.FloatField(blank=True, null=True)
    latitude_sp = models.FloatField(blank=True, null=True)
    service_point_id = models.CharField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'service_points'


class SipDensityPerHood(models.Model):
    hood_name = models.CharField(blank=True, null=True)
    district_name = models.TextField(blank=True, null=True)
    geom = models.TextField(blank=True, null=True)  # This field type is a guess.
    area_km2 = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    population = models.IntegerField(blank=True, null=True)
    sip_count = models.IntegerField(blank=True, null=True)
    population_density = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    order_density = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'sip_density_per_hood'


class SipPerCapita(models.Model):
    district_name = models.CharField(blank=True, null=True)
    hood_name = models.CharField(blank=True, null=True)
    population = models.IntegerField(blank=True, null=True)
    sip_count = models.IntegerField(blank=True, null=True)
    sip_per_capita = models.DecimalField(max_digits=10, decimal_places=4, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'sip_per_capita'


class SipWarWithRoutes(models.Model):
    geom = models.TextField(blank=True, null=True)  # This field type is a guess.
    field_1 = models.CharField(blank=True, null=True)
    longitude_s = models.FloatField(blank=True, null=True)
    latitude_s = models.FloatField(blank=True, null=True)
    longitude_w = models.FloatField(blank=True, null=True)
    latitude_w = models.FloatField(blank=True, null=True)
    route_km = models.FloatField(blank=True, null=True)
    route_min = models.FloatField(blank=True, null=True)
    route_geometry = models.CharField(blank=True, null=True)
    route_mid_lon = models.FloatField(blank=True, null=True)
    route_mid_lat = models.FloatField(blank=True, null=True)
    route_line = models.CharField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'sip_war_with_routes'


class SipWarWithRoutesBicycle(models.Model):
    index = models.TextField(blank=True, null=True)
    longitude_s = models.FloatField(blank=True, null=True)
    latitude_s = models.FloatField(blank=True, null=True)
    longitude_w = models.FloatField(blank=True, null=True)
    latitude_w = models.FloatField(blank=True, null=True)
    route_km = models.FloatField(blank=True, null=True)
    route_min = models.FloatField(blank=True, null=True)
    route_mid_lon = models.FloatField(blank=True, null=True)
    route_mid_lat = models.FloatField(blank=True, null=True)
    route_line = models.TextField(blank=True, null=True)
    midpoint = models.TextField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'sip_war_with_routes_bicycle'


class Siparis(models.Model):
    id = models.BigIntegerField(primary_key=True)
    fid = models.BigIntegerField(blank=True, null=True)
    order_id = models.BigIntegerField(blank=True, null=True)
    latitude = models.FloatField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)
    basket_value = models.FloatField(blank=True, null=True)
    delivery_duration = models.FloatField(blank=True, null=True)
    profit = models.FloatField(blank=True, null=True)
    revenue = models.FloatField(blank=True, null=True)
    client_id = models.TextField(blank=True, null=True)
    geom = models.TextField(blank=True, null=True)  # This field type is a guess.
    nearest_warehouse = models.TextField(blank=True, null=True)
    distance_to_warehouse = models.FloatField(blank=True, null=True)
    district_name = models.TextField(blank=True, null=True)
    hood_name = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'siparis'


class SiparisSer(models.Model):
    geom = models.TextField(blank=True, null=True)  # This field type is a guess.
    nearest_warehouse = models.CharField(blank=True, null=True)
    longitude_s = models.FloatField(blank=True, null=True)
    latitude_s = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'siparis_ser'


class SiparisSerBicycle(models.Model):
    nearest_warehouse = models.TextField(blank=True, null=True)
    longitude_s = models.FloatField(blank=True, null=True)
    latitude_s = models.FloatField(blank=True, null=True)
    siparis_point = models.TextField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'siparis_ser_bicycle'


class SpatialRefSys(models.Model):
    srid = models.IntegerField(primary_key=True)
    auth_name = models.CharField(max_length=256, blank=True, null=True)
    auth_srid = models.IntegerField(blank=True, null=True)
    srtext = models.CharField(max_length=2048, blank=True, null=True)
    proj4text = models.CharField(max_length=2048, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'spatial_ref_sys'


class Warehouse(models.Model):
    fid = models.BigIntegerField(blank=True, null=True)
    city_name = models.TextField(db_column='City_Name', blank=True, null=True)  # Field name made lowercase.
    warehouse_num = models.TextField(blank=True, null=True)
    longitude = models.FloatField(db_column='Longitude', blank=True, null=True)  # Field name made lowercase.
    latitude = models.FloatField(db_column='Latitude', blank=True, null=True)  # Field name made lowercase.
    geom = models.TextField(blank=True, null=True)  # This field type is a guess.
    district_name = models.TextField(blank=True, null=True)
    hood_name = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'warehouse'


class WarehouseIsochronesMedian(models.Model):
    geom = models.TextField(blank=True, null=True)  # This field type is a guess.
    warehouse_num = models.CharField(blank=True, null=True)
    median_min = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'warehouse_isochrones_median'


class WarehouseIsochronesMin(models.Model):
    geom = models.TextField(blank=True, null=True)  # This field type is a guess.
    warehouse_num = models.CharField(blank=True, null=True)
    min_duration_min = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'warehouse_isochrones_min'
