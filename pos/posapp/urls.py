from django.urls import path
from django.views.generic import RedirectView

from posapp import views

urlpatterns = [
    path('', views.index, name='index'),
    path('waiter', RedirectView.as_view(url='waiter/tabs'), name='waiter'),
    path('waiter/tabs', views.Waiter.Tabs.as_view(), name='waiter/tabs'),
    path('waiter/tabs/<uuid:id>', views.Waiter.Tabs.Tab.as_view(), name='waiter/tabs/tab'),
    path('waiter/orders', views.Waiter.Orders.as_view(), name='waiter/orders'),
    path('manager', RedirectView.as_view(url="manager/users"), name='manager'),
    path('manager/users', views.Manager.Users.as_view(), name='manager/users'),
    path('manager/users/create', views.Manager.Users.Create.as_view(), name='manager/users/create'),
    path('manager/tills', views.Manager.Tills.as_view(), name='manager/tills'),
    path('manager/tills/assign', views.Manager.Tills.Assign.as_view(), name='manager/tills/assign'),
    path('manager/tills/<uuid:id>', views.Manager.Tills.Till.as_view(), name='manager/tills/till'),
    path('manager/tills/<uuid:id>/stop', views.Manager.Tills.Till.Stop.as_view(), name='manager/tills/till/stop'),
    path('manager/tills/<uuid:id>/count', views.Manager.Tills.Till.Count.as_view(), name='manager/tills/till/count'),
    path('manager/tills/<uuid:id>/close', views.Manager.Tills.Till.Close.as_view(), name='manager/tills/till/close'),
    path('manager/tills/<uuid:id>/edit', views.Manager.Tills.Till.Edit.as_view(), name='manager/tills/till/edit'),
    path('admin', RedirectView.as_view(url="admin/finance"), name='admin'),
    path('admin/finance', RedirectView.as_view(url="finance/currencies"), name='admin/finance'),
    path('admin/finance/currencies', views.Admin.Finance.Currencies.as_view(), name='admin/finance/currencies'),
    path('admin/finance/methods', views.Admin.Finance.Methods.as_view(), name='admin/finance/methods'),
    path('admin/finance/methods/<uuid:id>', views.Admin.Finance.Methods.Method.as_view(),
         name='admin/finance/method/method'),
    path('admin/finance/methods/<uuid:id>/delete', views.Admin.Finance.Methods.Method.Delete.as_view(),
         name='admin/finance/methods/method/delete'),
    path('admin/units', RedirectView.as_view(url="admin/units/overview"), name='admin/units'),
    path('admin/units/overview', views.Admin.Units.as_view(), name='admin/units'),
    path('admin/menu', RedirectView.as_view(url="admin/menu/products"), name='admin/menu'),
    path('admin/menu/products', views.Admin.Menu.Products.as_view(), name='admin/menu/products'),
    path('admin/menu/products/<uuid:id>', views.Admin.Menu.Products.Product.as_view(),
         name='admin/menu/products/product'),
    path('admin/menu/products/<uuid:id>/delete', views.Admin.Menu.Products.Product.Delete.as_view(),
         name='admin/menu/products/product/delete'),
    path('admin/menu/items', views.Admin.Menu.Items.as_view(), name='admin/menu/items'),
    path('admin/menu/items/<uuid:id>', views.Admin.Menu.Items.Item.as_view(),
         name='admin/menu/items/item'),
    path('admin/menu/items/<uuid:id>/delete', views.Admin.Menu.Items.Item.Delete.as_view(),
         name='admin/menu/items/item/delete'),
]
