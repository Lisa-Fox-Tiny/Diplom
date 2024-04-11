from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import *


@admin.register(User)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ['id', 'email', 'company', 'position', 'type']
    search_fields = ('email',)
    # """
    # Панель управления пользователями
    # """
    # model = User
    #
    # fieldsets = (
    #     (None, {'fields': ('email', 'password', 'type')}),
    #     ('Personal info', {'fields': ('first_name', 'last_name', 'company', 'position')}),
    #     ('Permissions', {
    #         'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
    #     }),
    #     ('Important dates', {'fields': ('last_login', 'date_joined')}),
    # )
    # list_display = ('email', 'first_name', 'last_name', 'is_staff')


@admin.register(Shop)
class ShopAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'user', 'state']
    search_fields = ('name',)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']
    search_fields = ('name',)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'category']
    search_fields = ('name', 'model',)


@admin.register(ProductInfo)
class ProductInfoAdmin(admin.ModelAdmin):
    list_display = ['id', 'model', 'external_id', 'shop', 'quantity', 'price', 'price_rrc']
    search_fields = ('name', 'model',)


@admin.register(Parameter)
class ParameterAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']
    search_fields = ('product',)


@admin.register(ProductParameter)
class ProductParameterAdmin(admin.ModelAdmin):
    list_display = ['id', 'product_info', 'parameter', 'value']
    search_fields = ('product',)


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'state', 'contact', 'dt']
    search_fields = ('state',)


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['id', 'order', 'product_info', 'quantity']
    search_fields = ('order',)


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'city', 'street', 'house', 'structure', 'building', 'apartment', 'phone']


@admin.register(ConfirmEmailToken)
class ConfirmEmailTokenAdmin(admin.ModelAdmin):
    list_display = ('user', 'key', 'created_at',)


@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    list_display = ('name_first', 'name_last', 'headshot')


