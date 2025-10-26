# App/admin.py
from datetime import datetime

from django import forms
from django.contrib import admin
from django.utils.html import format_html

from .models import Activity, ActivityImage, ActivitySection, Menu, MenuItem


# ---------- Forms ----------
def year_choices(start=2000, end=None):
    if end is None:
        end = datetime.now().year + 1
    years = [(str(y), str(y)) for y in range(end, start - 1, -1)]
    return [("", "----")] + years


class ActivitySectionForm(forms.ModelForm):
    class Meta:
        model = ActivitySection
        fields = "__all__"
        widgets = {
            "start_date": forms.DateInput(attrs={"type": "date"}),
            "end_date": forms.DateInput(attrs={"type": "date"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["year"].widget = forms.Select(choices=year_choices(2000))


# ---------- Inlines ----------
class ActivityImageInline(admin.TabularInline):
    model = ActivityImage
    extra = 1
    fields = ("image", "caption", "is_portrait", "order", "preview_inline")
    ordering = ("order",)
    readonly_fields = ("preview_inline",)

    def preview_inline(self, obj):
        if obj.pk and obj.image:
            return format_html(
                '<a href="{}" target="_blank"><img src="{}" style="max-height:70px;border-radius:6px"/></a>',
                obj.image.url,
                obj.image.url,
            )
        return "(ยังไม่มีรูป)"

    preview_inline.short_description = "ตัวอย่าง"


class ActivitySectionInline(admin.StackedInline):
    model = ActivitySection
    form = ActivitySectionForm
    extra = 1
    show_change_link = True
    fields = (
        "title",
        "year",
        "location",
        "participants",
        "start_date",
        "end_date",
        "description",
        "order",
    )
    ordering = ("order",)


# ---------- Activity Admin ----------
@admin.register(Activity)
class ActivityAdmin(admin.ModelAdmin):
    list_display = ("name", "slug", "view_on_site_link")
    prepopulated_fields = {"slug": ("name",)}
    inlines = [ActivitySectionInline]

    def view_on_site_link(self, obj):
        return format_html(
            '<a href="{}" target="_blank">ดูหน้า</a>', obj.get_absolute_url()
        )

    view_on_site_link.short_description = "เปิดดูหน้า"


@admin.register(ActivitySection)
class ActivitySectionAdmin(admin.ModelAdmin):
    form = ActivitySectionForm
    list_display = ("title", "activity", "year", "date_range", "order")
    list_filter = ("activity", "year")
    ordering = ("activity", "order")
    inlines = [ActivityImageInline]


@admin.register(ActivityImage)
class ActivityImageAdmin(admin.ModelAdmin):
    list_display = ("preview_thumb", "section", "caption", "is_portrait", "order")
    list_filter = ("section",)
    ordering = ("section", "order")
    readonly_fields = ("preview_large",)
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "section",
                    "image",
                    "caption",
                    "is_portrait",
                    "order",
                    "preview_large",
                )
            },
        ),
    )

    def preview_thumb(self, obj):
        if obj.image:
            return format_html(
                '<a href="{}" target="_blank"><img src="{}" style="max-height:60px;border-radius:6px"/></a>',
                obj.image.url,
                obj.image.url,
            )
        return "—"

    preview_thumb.short_description = "ตัวอย่าง"

    def preview_large(self, obj):
        if obj.image:
            return format_html(
                '<a href="{}" target="_blank"><img src="{}" style="max-width:360px;border-radius:10px"/></a>',
                obj.image.url,
                obj.image.url,
            )
        return "—"

    preview_large.short_description = "ตัวอย่าง (ใหญ่)"


# ---------- Menu Admin ----------
class MenuItemInline(admin.TabularInline):
    model = MenuItem
    extra = 1
    fields = (
        "label",
        "activity_page",
        "named_url",
        "url",
        "open_new_tab",
        "order",
        "preview_link",
    )
    readonly_fields = ("preview_link",)
    ordering = ("order",)

    def preview_link(self, obj):
        if not obj.pk:
            return "—"
        href = obj.resolved_href()
        return format_html('<a href="{}" target="_blank">เปิดลิงก์</a>', href)

    preview_link.short_description = "ทดสอบลิงก์"


@admin.register(Menu)
class MenuAdmin(admin.ModelAdmin):
    list_display = ("name", "slug")
    search_fields = ("name", "slug")
    inlines = [MenuItemInline]


@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    list_display = ("label", "menu", "order", "open_new_tab", "dest")
    list_filter = ("menu", "open_new_tab")
    search_fields = ("label", "named_url", "url", "menu__name")
    ordering = ("menu", "order")

    def dest(self, obj):
        if obj.activity_page:
            return f"Activity: {obj.activity_page.slug}"
        if obj.named_url:
            return f"named: {obj.named_url}"
        return obj.url or "—"

    dest.short_description = "ปลายทาง"
