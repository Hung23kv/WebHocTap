# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Baihoc(models.Model):
    id_khoahoc = models.ForeignKey('Khoahoc', models.DO_NOTHING, db_column='id_khoahoc', blank=True, null=True)
    tieude = models.CharField(db_column='TieuDe', max_length=250, blank=True, null=True)  # Field name made lowercase.
    thutu = models.IntegerField(db_column='ThuTu', blank=True, null=True)  # Field name made lowercase.
    diem = models.IntegerField(db_column='Diem', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'BaiHoc'


class Dtnguoidung(models.Model):
    nguoigui = models.ForeignKey('Nguoidung', models.DO_NOTHING, db_column='NguoiGui', blank=True, null=True)  # Field name made lowercase.
    nguoinhan = models.ForeignKey('Nguoidung', models.DO_NOTHING, db_column='NguoiNhan', related_name='dtnguoidung_nguoinhan_set', blank=True, null=True)  # Field name made lowercase.
    tinnhan = models.CharField(db_column='TinNhan', max_length=255, blank=True, null=True)  # Field name made lowercase.
    ngay = models.DateField(db_column='Ngay', blank=True, null=True)  # Field name made lowercase.
    id_doithoai = models.ForeignKey('Doithoai', models.DO_NOTHING, db_column='id_DoiThoai', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'DTNguoiDung'


class Doithoai(models.Model):
    tieude = models.CharField(db_column='TieuDe', max_length=255, blank=True, null=True)  # Field name made lowercase.
    muctieu = models.CharField(db_column='MucTieu', max_length=255, blank=True, null=True)  # Field name made lowercase.
    hinhanh = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'DoiThoai'


class Khoahoc(models.Model):
    ten = models.CharField(db_column='Ten', max_length=50, blank=True, null=True)  # Field name made lowercase.
    ngaytao = models.DateField(db_column='NgayTao', blank=True, null=True)  # Field name made lowercase.
    diemlencap = models.IntegerField(db_column='DiemLenCap', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Khoahoc'


class Nguoidung(models.Model):
    ten = models.CharField(db_column='Ten', max_length=100, blank=True, null=True)  # Field name made lowercase.
    email = models.CharField(db_column='Email', max_length=255, blank=True, null=True)  # Field name made lowercase.
    matkhau = models.CharField(db_column='MatKhau', max_length=50, blank=True, null=True)  # Field name made lowercase.
    quyen = models.CharField(db_column='Quyen', max_length=50, blank=True, null=True)  # Field name made lowercase.
    ngaytao = models.DateField(db_column='NgayTao', blank=True, null=True)  # Field name made lowercase.
    otp = models.CharField(max_length=6, blank=True, null=True)
    verotp = models.CharField(db_column='verOtp', max_length=6, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'NguoiDung'


class Ontap(models.Model):
    id_nguoidung = models.ForeignKey(Nguoidung, models.DO_NOTHING, db_column='id_nguoidung', blank=True, null=True)
    id_baihoc = models.ForeignKey(Baihoc, models.DO_NOTHING, db_column='id_baihoc', blank=True, null=True)
    ngaylam = models.DateField(db_column='ngayLam', blank=True, null=True)  # Field name made lowercase.
    ketqua = models.IntegerField(db_column='ketQua', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'OnTap'


class Thoai(models.Model):
    id_doithoai = models.ForeignKey(Doithoai, models.DO_NOTHING, db_column='id_doithoai', blank=True, null=True)
    cauhoi = models.CharField(db_column='Cauhoi', max_length=255, blank=True, null=True)  # Field name made lowercase.
    ngaytao = models.DateField(db_column='NgayTao', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Thoai'


class Tientrinh(models.Model):
    id_nguoidung = models.ForeignKey(Nguoidung, models.DO_NOTHING, db_column='id_nguoidung', blank=True, null=True)
    id_khoahoc = models.ForeignKey(Khoahoc, models.DO_NOTHING, db_column='id_khoahoc', blank=True, null=True)
    diemtong = models.IntegerField(db_column='DiemTong', blank=True, null=True)  # Field name made lowercase.
    tudahoc = models.IntegerField(db_column='TuDaHoc', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'TienTrinh'


class Traloi(models.Model):
    id_nguoidung = models.ForeignKey(Nguoidung, models.DO_NOTHING, db_column='id_nguoidung', blank=True, null=True)
    id_cauhoi = models.ForeignKey(Thoai, models.DO_NOTHING, db_column='id_cauhoi', blank=True, null=True)
    ngaygui = models.DateField(db_column='NgayGui', blank=True, null=True)  # Field name made lowercase.
    noidung = models.CharField(db_column='NoiDung', max_length=255, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'TraLoi'


class Tuvung(models.Model):
    id_baihoc = models.ForeignKey(Baihoc, models.DO_NOTHING, db_column='id_baihoc', blank=True, null=True)
    tu = models.CharField(db_column='Tu', max_length=255, blank=True, null=True)  # Field name made lowercase.
    dich = models.CharField(db_column='Dich', max_length=255, blank=True, null=True)  # Field name made lowercase.
    phatam = models.CharField(db_column='PhatAm', max_length=255, blank=True, null=True)  # Field name made lowercase.
    hinhanh = models.CharField(db_column='HinhAnh', max_length=255, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'TuVung'


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
