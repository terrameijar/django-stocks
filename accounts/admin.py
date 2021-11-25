from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserChangeForm, CustomUserCreationForm
from .models import CustomUser
from api.models import StockHolding


class UserFilter(admin.SimpleListFilter):
    def queryset(self, request, queryset):
        return queryset.filter(self.value())


class CustomUserAdmin(UserAdmin):
    # list_filter = (UserFilter,)
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ("email", "is_staff", "is_active")
    list_filter = ("email", "is_staff", "is_active")
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        ("Permissions", {"fields": ("is_staff", "is_active")}),
        (
            "Stock Holding",
            {"fields": ("stock_holding",)},
        ),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("email", "password1", "password2", "is_staff", "is_active"),
            },
        ),
    )
    search_fields = ("email",)
    ordering = ("email",)

    # def formfield_for_manytomany(self, db_field: StockHolding, request, **kwargs):
    #     """Limit many to many list to stock holdings for current user."""

    #     if db_field.name == "stock_holding":
    #         # qs = super(CustomUserAdmin, self).get_queryset(request)
    #         # breakpoint()
    #         kwargs["queryset"] = StockHolding.objects.filter(user=request.user)
    #         # kwargs["queryset"] = StockHolding.objects.filter(user=request.user)
    #     return super().formfield_for_manytomany(db_field, request, **kwargs)


admin.site.register(CustomUser, CustomUserAdmin)
