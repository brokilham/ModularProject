import datetime
import json
from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.serializers.json import DjangoJSONEncoder
from django.views import View
from django.http import JsonResponse, HttpResponse
from .models import t_master_jenis_pulsa,t_master_harga_pulsa,t_transaksi_pulsa
from django.db.models import Q

 
class jenis_pulsa_webview(View):       
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
        kode_voucher  = request.POST['kode_voucher'], tipe_voucher = request.POST['tipe_voucher'],
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

class harga_webview(View):
    def get(self, request):
        jobs = request.GET['jobs'].lower()
        if jobs == "get_data_select_jenis_pulsa":
            return self._select_jenis_pulsa(request)
        elif jobs =="get_data_datatable":      
           return self._datatables(request)
        return JsonResponse({'status':'e','result':""})

    def post(self, request):
        return JsonResponse({'status':'e','result':""})

    def _select_jenis_pulsa(self,request):
        dt_jenis_pulsa = t_master_jenis_pulsa.objects.all()
        option = "<option value = "" selected> Pilih nama voucher</option>"
        for item in dt_jenis_pulsa:
            option += "<option value='"+ str(item.id) +"'>"+ item.jenis_voucher +" (" + item.kode_voucher +")"+"</option>"
        return HttpResponse(option)

    def _datatables(self, request):
        datatables = request.GET
        # Ambil draw
        draw = int(datatables.get('draw'))
        # Ambil length (limit)
        length = int(datatables.get('length'))
        # Ambil data search
        search = datatables.get('search[value]')
        # Set record total
        records_total = t_master_harga_pulsa.objects.all().count()
		# Set records filtered
        records_filtered = records_total
        # Ambil data all
        dt_harga_pulsa = t_master_harga_pulsa.objects.all()

        if search:
            dt_harga_pulsa = t_master_harga_pulsa.objects.filter(
                Q(id__icontains=search)|
                Q(harga_beli__icontains=search)|
                Q(harga_jual__icontains=search)
            )
            records_total = dt_harga_pulsa.count()
            records_filtered = records_total

        # Atur paginator
        paginator = Paginator(dt_harga_pulsa, length)

        try:
            object_list = paginator.page(draw).object_list
        except PageNotAnInteger:
            object_list = paginator.page(draw).object_list
        except EmptyPage:
            object_list = paginator.page(paginator.num_pages).object_list

        data = [
            {
                'id': item.id,
                'jenis_voucher': item.t_master_jenis_pulsa.jenis_voucher,
                'harga_beli': item.harga_beli,
                'harga_jual': item.harga_jual,
                'periode_mulai': item.periode_mulai,
                'periode_akhir': item.periode_akhir,
                'action': '<a id="anchor_update"  attr-id-item="'+ str(item.id) +'"  attr-jenis-voucher="'+ str(item.t_master_jenis_pulsa.id) +'"  attr-harga-beli="'+ str(item.harga_beli) +'" attr-harga-jual="'+ str(item.harga_jual) +'" attr-periode-mulai="'+ str(item.periode_mulai) +'" attr-periode-akhir="'+ str(item.periode_akhir) +'"  class="btn btn-success m-btn m-btn--icon btn-sm m-btn--icon-only">'
                            '<i class="la la-edit"></i>'
                          '</a> &nbsp;'
                          '<a id="anchor_delete" attr-id-item="'+ str(item.id) +'" class="btn btn-danger m-btn m-btn--icon btn-sm m-btn--icon-only">'
                            '<i class="la la-trash"></i>'
                          '</a>',
            } for item in object_list
        ]
        datatable = { 'draw': draw,'recordsTotal': records_total,
                      'recordsFiltered': records_filtered,'data': data}
        return HttpResponse(json.dumps(datatable, cls=DjangoJSONEncoder), content_type='application/json')

class harga(View):
    def _create(self, request):
        jenis_pulsa = t_master_jenis_pulsa.objects.get(id=request.POST['slc_id_jenis_pulsa'])
        harga_pulsa = t_master_harga_pulsa()
        harga_pulsa.t_master_jenis_pulsa = jenis_pulsa
        harga_pulsa.harga_beli = request.POST['txt_harga_beli']
        harga_pulsa.harga_jual = request.POST['txt_harga_jual']
        harga_pulsa.periode_mulai =  request.POST['date_periode_mulai']
        harga_pulsa.periode_akhir =  request.POST['date_periode_akhir']
        harga_pulsa.created_by    = "ilham"
        harga_pulsa.created_date  = datetime.datetime.today().strftime('%Y-%m-%d')
        harga_pulsa.updated_by    = ""
        harga_pulsa.update_date   = datetime.datetime.today().strftime('%Y-%m-%d')
        harga_pulsa.save()
        return JsonResponse({'status':'s','result':'Data berhasil disimpan'})  
    
    def _put(self, request):
        return JsonResponse({'status':'s','result':'Data berhasil diperbarui'})  
    
    def _delete(self, request):
        t_master_harga_pulsa.objects.filter(pk=request.POST['id']).delete()        
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
        return render(request, "Harga/index.html")

class penjualan_webview(View):

    def _select_harga_pulsa(self,requset):
        dt_harga_pulsa = t_master_harga_pulsa.objects.all()
        option = "<option value =''> Pilih pulsa</option>"
        for item in dt_harga_pulsa:
            option += "<option value='"+ str(item.id) +"'>"+ item.t_master_jenis_pulsa.jenis_voucher+" (" + item.t_master_jenis_pulsa.kode_voucher +")"+"</option>"
        return HttpResponse(option)

    def _datatables(self,request):
        datatables = request.GET
        # Ambil draw
        draw = int(datatables.get('draw'))
        # Ambil length (limit)
        length = int(datatables.get('length'))
        # Ambil data search
        search = datatables.get('search[value]')
        # Set record total
        records_total = t_transaksi_pulsa.objects.all().count()
		# Set records filtered
        records_filtered = records_total
        # Ambil data all
        dt_transaksi_pulsa = t_transaksi_pulsa.objects.all()

        if search:
            dt_transaksi_pulsa = dt_transaksi_pulsa.objects.filter(
					Q(id__icontains=search)
				)
            records_total = dt_transaksi_pulsa.count()
            records_filtered = records_total

        # Atur paginator
        paginator = Paginator(dt_transaksi_pulsa, length)

        try:
            object_list = paginator.page(draw).object_list
        except PageNotAnInteger:
            object_list = paginator.page(draw).object_list
        except EmptyPage:
            object_list = paginator.page(paginator.num_pages).object_list


        data = [
            {
                'id': item.id,
                'no_hp' : item.no_hp,
                'jenis_voucher' : item.t_master_harga_pulsa.t_master_jenis_pulsa.jenis_voucher,
                'total_bayar' : item.total_bayar,
                'tgl_beli'  : item.created_date,
                'catatan' : item.catatan,
                'status_transaksi' : item.status_transaksi,
                'action': '<a id="anchor_update"  attr-id-item="'+ str(item.id) +'" attr-no-hp="'+ str(item.no_hp) +
                '" attr-jenis-voucher="'+ str(item.t_master_harga_pulsa.t_master_jenis_pulsa.jenis_voucher) +
                '" attr-total-bayar="'+ str(item.total_bayar) +'" attr-tgl-beli="'+ str(item.created_date) +
                '" attr-catatan="'+ str(item.catatan) +'" attr-status-transaksi="'+ str(item.status_transaksi) +
                '" attr-id-harga="'+ str(item.t_master_harga_pulsa.id) +'" class="btn btn-success m-btn m-btn--icon btn-sm m-btn--icon-only">'
                            '<i class="la la-edit"></i>'
                          '</a> &nbsp;'
                          '<a id="anchor_delete" attr-id-item="'+ str(item.id) +'" class="btn btn-danger m-btn m-btn--icon btn-sm m-btn--icon-only">'
                            '<i class="la la-trash"></i>'
                          '</a>'
            } for item in object_list
        ]

        datatable =  {'draw': draw,
                 'recordsTotal': records_total,
                 'recordsFiltered': records_filtered,
                 'data': data}

        return HttpResponse(json.dumps(datatable, cls=DjangoJSONEncoder), content_type='application/json')

    def get(self, request):
        jobs = request.GET['jobs'].lower()
        if jobs == "get_data_select_harga_pulsa":
            return self._select_harga_pulsa(request)
        elif jobs =="get_data_datatable":      
           return self._datatables(request)
        return JsonResponse({'status':'e','result':""})

    def post(self, request):
        return JsonResponse({'status':'e','result':""})

class penjualan(View):
    def _create(self, request):
        harga_pulsa = t_master_harga_pulsa.objects.get(id=request.POST['slc_id_harga_pulsa'])
        transaksi_pulsa = t_transaksi_pulsa()
        transaksi_pulsa.t_master_harga_pulsa = harga_pulsa
        transaksi_pulsa.no_hp         = request.POST['txt_nomer_hp']
        transaksi_pulsa.total_bayar   = request.POST['txt_total_bayar']
        transaksi_pulsa.status_transaksi = request.POST['slc_status_transaksi']
        transaksi_pulsa.catatan       = request.POST['txt_catatan']
        transaksi_pulsa.created_by    = "ilham"
        transaksi_pulsa.created_date  = datetime.datetime.today().strftime('%Y-%m-%d')
        transaksi_pulsa.updated_by    = ""
        transaksi_pulsa.update_date   = datetime.datetime.today().strftime('%Y-%m-%d')
        transaksi_pulsa.save()
        return JsonResponse({'status':'s','result':'Data berhasil disimpan'}) 

    def _put(self, request):
        return JsonResponse({'status':'s','result':'Data berhasil diperbarui'})  

    def _delete(self, request):      
        t_transaksi_pulsa.objects.filter(pk=request.POST['id']).delete()        
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
        return render(request, "Penjualan/index.html")


class report_webview(View):
    def _datatables(self,request):
        return JsonResponse({'status':'e','result':'http_type tidak diketahui'}) 

class report(View):
    def get(self, request,*args,**kwargs):
        return render(request,"Report/index.html")

"""
@login_required
def index_penjualan(request):
    return render(request, "Penjualan/index.html")


@login_required
def index_harga(request):
    return render(request, "Harga/index.html")


@login_required
def index_jenis_pulsa(request):
    return render(request, "Jenis_Pulsa/index.html")
"""