from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.serializers.json import DjangoJSONEncoder
from django.views import View
from django.http import JsonResponse, HttpResponse
from .models import t_master_jenis_pulsa
import datetime
import json
from django.db.models import Q

class jenis_pulsa_weblist(View):       
    def get(self, request):
        datatable = self._datatables(request)
        return HttpResponse(json.dumps(datatable, cls=DjangoJSONEncoder), content_type='application/json')
    
    def _datatables(self, request):
        datatables = request.GET
        # Ambil draw
        draw = int(datatables.get('draw'))
        # Ambil length (limit)
        length = int(datatables.get('length'))
        # Ambil data search
        search = datatables.get('search[value]')
        # Set record total
        records_total = t_master_jenis_pulsa.objects.all().count()
		# Set records filtered
        records_filtered = records_total
        # Ambil data all
        dt_jenis_pulsa = t_master_jenis_pulsa.objects.all()

        if search:
            dt_jenis_pulsa = t_master_jenis_pulsa.objects.filter(
					Q(id__icontains=search)|
					Q(jenis_voucher__icontains=search)|
					Q(kode_voucher__icontains=search)|
					Q(tipe_voucher__icontains=search)
				)
            records_total = dt_jenis_pulsa.count()
            records_filtered = records_total

        # Atur paginator
        paginator = Paginator(dt_jenis_pulsa, length)

        try:
            object_list = paginator.page(draw).object_list
        except PageNotAnInteger:
            object_list = paginator.page(draw).object_list
        except EmptyPage:
            object_list = paginator.page(paginator.num_pages).object_list


        data = [
            {
                'id': item.id,
                'jenis_voucher': item.jenis_voucher,
                'kode_voucher': item.kode_voucher,
                'tipe_voucher': item.tipe_voucher,
                'action': '<a id="anchor_update"  attr-id-item="'+ str(item.id) +'" attr-jenis_voucher="'+ item.jenis_voucher +'"  attr-kode_voucher="'+ item.kode_voucher +'" attr-tipe_voucher="'+ item.tipe_voucher +'" class="btn btn-success m-btn m-btn--icon btn-sm m-btn--icon-only">'
                            '<i class="la la-edit"></i>'
                          '</a> &nbsp;'
                          '<a id="anchor_delete" attr-id-item="'+ str(item.id) +'" class="btn btn-danger m-btn m-btn--icon btn-sm m-btn--icon-only">'
                            '<i class="la la-trash"></i>'
                          '</a>',
            } for item in object_list
        ]

        return {
            'draw': draw,
            'recordsTotal': records_total,
			'recordsFiltered': records_filtered,
            'data': data,
        }
class jenis_pulsa(View):
    def _create(self,request):
        try:      
            jenis_pulsa = t_master_jenis_pulsa()
            jenis_pulsa.jenis_voucher = request.POST['txt_jenis_voucher']
            jenis_pulsa.kode_voucher  = request.POST['txt_kode_voucher']
            jenis_pulsa.tipe_voucher  = request.POST['txt_tipe_voucher']
            jenis_pulsa.created_by    = "ilham"
            jenis_pulsa.created_date  = datetime.datetime.today().strftime('%Y-%m-%d')
            jenis_pulsa.updated_by    = ""
            jenis_pulsa.update_date   = datetime.datetime.today().strftime('%Y-%m-%d')
            jenis_pulsa.save()
            return JsonResponse({'status':'s','result':'Data berhasil disimpan'}) 
        except ValueError  as Argument: 
            return JsonResponse({'status':'e','result':Argument})
    
    def _put(self,request):
        t_master_jenis_pulsa.objects.filter(pk=request.POST['id']).update(jenis_voucher = request.POST['jenis_voucher'], 
        kode_voucher  = request.POST['kode_voucher'], tipe_voucher  = request.POST['tipe_voucher'],  
        updated_by = 'ilham',  update_date  = datetime.datetime.today().strftime('%Y-%m-%d'))
        return JsonResponse({'status':'s','result':'Data berhasil diperbarui'})

    def _delete(self,request):
        t_master_jenis_pulsa.objects.filter(pk=request.POST['id']).delete()        
        return JsonResponse({'status':'s','result':'data berhasil di hapus'}) 
           
    def post(self, request, *args, **kwargs):
        method = request.POST['http_type'].lower()
        if method == "post":
            return self._create(request)
        elif method == "put":
            return self._put(request)
        elif method == "delete":
            return self._delete(request)
        return JsonResponse({'status':'e','result':'http_type tidak diketahui'}) 

    def get(self, request, *args, **kwargs):    
        return render(request, "Jenis_Pulsa/index.html") 

class penjualan(View):
    def get(self, request, *args, **kwargs):
        return render(request, "Penjualan/index.html")

class harga(View):
    def get(self, request, *args, **kwargs):    
        return render(request, "Harga/index.html")

@login_required
def index_penjualan(request):
    return render(request, "Penjualan/index.html")


@login_required
def index_harga(request):
    return render(request, "Harga/index.html")


@login_required
def index_jenis_pulsa(request):
    return render(request, "Jenis_Pulsa/index.html")