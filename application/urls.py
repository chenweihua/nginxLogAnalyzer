from django.conf.urls import url, include
from rest_framework.urlpatterns import format_suffix_patterns
from application import views

urlpatterns = [
    url(r'^application/$', views.SnippetList.as_view()),
    url(r'^request/$', views.RequestList.as_view()),
    url(r'^code/$', views.CodeList.as_view()),
    url(r'^code206/$', views.CodeList206.as_view()),
    url(r'^ipcontent/$', views.Ipcontenlist.as_view()),
    url(r'^code200/$', views.CodeList200.as_view()),
    url(r'^code404/$', views.CodeList404.as_view()),
    url(r'^code301/$', views.CodeList301.as_view()),
    url(r'^code302/$', views.CodeList302.as_view()),
    url(r'^code403/$', views.CodeList403.as_view()),
    url(r'^code405/$', views.CodeList405.as_view()),
    url(r'^code406/$', views.CodeList406.as_view()),
    url(r'^code500/$', views.CodeList500.as_view()),
    url(r'^code504/$', views.CodeList504.as_view()),
    url(r'^status/$', views.StatusList.as_view()),
    url(r'^najaktivniji/$', views.NajaktivnijiList.as_view()),
    url(r'^sadrzaj/$', views.ListaTemplate.as_view(), name='sadrzaj'),
    url(r'^table/$', views.dataTabs, name="table"),
    url(r'^table2/$', views.datacontent, name="table2"),
    url(r'^table3/$', views.vrijemeview, name="table3"),
    url(r'^table4/$', views.simple_list, name="table4"),
    url(r'^procesing/$', views.run_script, name="procesing"),
    url(r'^tables/$', views.pisem_html, name="tables"),
    url(r'^nginxgraph1/$', views.nginx_graphOne, name="nginxgraph1"),
    url(r'^nginxgraph2/$', views.nginx_graphTwo, name="nginxgraph2"),
    url(r'^nginxgraph3/$', views.nginx_graphtreci, name="nginxgraph3"),
    url(r'^nginxgraph4/$', views.nginx_cetvrti, name="nginxgraph4"),
    url(r'^delete/(?P<stb_id>\d+)/$', views.delete, name="delete"),
    url(r'^upload/$', views.procesing_html, name="upload"),
    url(r'^overall/$', views.static1, name="overall"),
    url(r'^index/$', views.static, name="index"),
    url(r'^$', views.home, name='home'),
    url(r'^regex/$', views.searchregwx, name='regex'),
    url(r'^default/$', views.defaultempty, name="default"),
    url(r'^default2/$', views.default2, name="default2"),
    url(r'^userclient/$', views.total_client_request_defined_by_user, name="userclient"),
    url(r'^whois/$', views.Whois, name="whois"),


]

urlpatterns = format_suffix_patterns(urlpatterns)
