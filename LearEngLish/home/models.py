from django.db import models

class NguoiDung(models.Model):
    Ten = models.CharField(max_length=100, db_column='Ten')
    Email = models.CharField(max_length=255, db_column='Email')
    MatKhau = models.CharField(max_length=50, db_column='MatKhau')
    Quyen = models.CharField(max_length=50, db_column='Quyen')
    NgayTao = models.DateField(db_column='NgayTao')
    otp = models.CharField(max_length=6, db_column='otp')
    verOtp = models.CharField(max_length=6, db_column='verOtp')

    class Meta:
        managed = False
        db_table = 'NguoiDung'


class TienTrinh(models.Model):
    id_nguoidung = models.ForeignKey('NguoiDung', db_column='id_nguoidung', on_delete=models.CASCADE)
    id_khoahoc = models.IntegerField(db_column='id_khoahoc')  # Không liên kết ForeignKey do bảng này không dùng join
    diem_tong = models.IntegerField(db_column='DiemTong')
    tuvung_hoc = models.IntegerField(db_column='TuDaHoc')

    class Meta:
        managed = False
        db_table = 'TienTrinh'


class KhoaHoc(models.Model):
    Ten = models.CharField(max_length=50)
    NgayTao = models.DateField(auto_now_add=True)
    DiemLenCap = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'Khoahoc'


class BaiHoc(models.Model):
    id_khoahoc = models.ForeignKey('KhoaHoc', db_column='id_khoahoc', on_delete=models.CASCADE)
    TieuDe = models.CharField(max_length=250)
    ThuTu = models.IntegerField()
    Diem = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'BaiHoc'


class TuVung(models.Model):
    id_baihoc = models.ForeignKey('BaiHoc', db_column='id_baihoc', on_delete=models.CASCADE)
    Tu = models.CharField(max_length=255)
    Dich = models.TextField()
    PhatAm = models.CharField(max_length=255, blank=True, null=True)
    HinhAnh = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'TuVung'


class OnTap(models.Model):
    id_nguoidung = models.IntegerField(db_column='id_nguoidung')
    id_baihoc = models.IntegerField(db_column='id_baihoc')
    ngayLam = models.DateField(db_column='ngayLam')
    ketQua = models.IntegerField(db_column='ketQua')

    class Meta:
        managed = False
        db_table = 'OnTap'
