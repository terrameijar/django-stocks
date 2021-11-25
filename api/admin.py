from django.contrib import admin
from .models import Stock, StockHolding


class StockHoldingAdmin(admin.ModelAdmin):
    def get_queryset(self, request):
        qs = super(StockHoldingAdmin, self).get_queryset(request)
        return qs.filter(user=request.user)

    def formfield_for_foreignkey(self, db_field: StockHolding, request, **kwargs):
        # kwargs["queryset"] = StockHolding.objects.filter(user=request.user)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


admin.site.register(Stock)
admin.site.register(StockHolding, StockHoldingAdmin)
