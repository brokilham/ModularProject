from django.db import models

class t_master_jenis_pulsa(models.Model):
    jenis_voucher = models.CharField(max_length=30)
    kode_voucher  = models.CharField(max_length=30)
    tipe_voucher  = models.CharField(max_length=30)
    created_by    = models.CharField(max_length=30)
    created_date  = models.DateField()
    updated_by    = models.CharField(max_length=30)
    update_date   = models.DateField()

