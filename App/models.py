# App/models.py
from django.core.exceptions import ValidationError
from django.db import models
from django.urls import reverse
from django.utils.text import slugify


def activity_image_upload_to(instance, filename: str) -> str:
    act_slug = instance.section.activity.slug or "activity"
    return f"activity/{act_slug}/{instance.section_id}/{filename}"


# --------- Activity / Sections / Images (แบบเดิม) ---------
class Activity(models.Model):
    name = models.CharField(
        max_length=200, verbose_name="ชื่อหน้า", help_text="เช่น Outing Activity"
    )
    slug = models.SlugField(
        max_length=80,
        unique=True,
        db_index=True,
        verbose_name="Slug",
        help_text="ใช้ใน URL เช่น 'outing' (ปล่อยว่างให้ระบบสร้างอัตโนมัติได้)",
        blank=True,
    )
    subtitle = models.CharField(
        max_length=255, blank=True, verbose_name="ข้อความใต้หัวเรื่อง"
    )

    class Meta:
        verbose_name = "Activity Page"
        verbose_name_plural = "Activity Pages"

    def __str__(self) -> str:
        return self.name

    def get_absolute_url(self) -> str:
        return reverse("activity_detail", kwargs={"slug": self.slug})

    def save(self, *args, **kwargs):
        if not self.slug and self.name:
            base = slugify(self.name) or "activity"
            slug = base
            i = 1
            while Activity.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                i += 1
                slug = f"{base}-{i}"
            self.slug = slug
        super().save(*args, **kwargs)


class ActivitySection(models.Model):
    activity = models.ForeignKey(
        Activity,
        on_delete=models.CASCADE,
        related_name="sections",
        verbose_name="อยู่ในหน้า",
    )
    title = models.CharField(max_length=255, verbose_name="หัวข้อ")
    year = models.CharField(
        max_length=10,
        blank=True,
        verbose_name="ปี (แสดงผล)",
        help_text="เช่น 2024 หรือปล่อยว่าง",
    )
    location = models.CharField(max_length=255, blank=True, verbose_name="สถานที่")
    participants = models.PositiveIntegerField(
        null=True, blank=True, verbose_name="ผู้เข้าร่วม (คน)"
    )
    start_date = models.DateField(null=True, blank=True, verbose_name="วันที่เริ่ม")
    end_date = models.DateField(null=True, blank=True, verbose_name="วันที่สิ้นสุด")
    description = models.TextField(blank=True, verbose_name="รายละเอียด")
    order = models.PositiveIntegerField(
        default=0, verbose_name="ลำดับแสดง", help_text="เลขยิ่งน้อยยิ่งอยู่บน"
    )

    class Meta:
        ordering = ["order", "id"]
        verbose_name = "หัวข้อกิจกรรม"
        verbose_name_plural = "หัวข้อกิจกรรม"
        constraints = [
            models.UniqueConstraint(
                fields=["activity", "order"], name="uniq_section_order_per_activity"
            ),
            models.UniqueConstraint(
                fields=["activity", "title"], name="uniq_section_title_per_activity"
            ),
        ]

    def __str__(self) -> str:
        return f"{self.activity.slug} · {self.title}"

    @property
    def date_range(self) -> str:
        if self.start_date and self.end_date:
            if self.start_date == self.end_date:
                return self.start_date.strftime("%d %b %Y")
            return f"{self.start_date.strftime('%d %b %Y')} - {self.end_date.strftime('%d %b %Y')}"
        if self.start_date and not self.end_date:
            return f"{self.start_date.strftime('%d %b %Y')} - "
        if self.end_date and not self.start_date:
            return f"- {self.end_date.strftime('%d %b %Y')}"
        return ""

    def clean(self):
        if self.year:
            digits = "".join(ch for ch in self.year if ch.isdigit())
            if len(digits) == 4:
                self.year = digits
            elif len(digits) == 0:
                self.year = ""
            else:
                raise ValidationError({"year": "กรุณาใส่ปีเป็นตัวเลข 4 หลัก หรือปล่อยว่าง"})
        if self.start_date and self.end_date and self.end_date < self.start_date:
            raise ValidationError({"end_date": "วันที่สิ้นสุดต้องไม่น้อยกว่าวันที่เริ่ม"})


class ActivityImage(models.Model):
    section = models.ForeignKey(
        ActivitySection,
        on_delete=models.CASCADE,
        related_name="images",
        verbose_name="หัวข้อ",
    )
    image = models.ImageField(upload_to=activity_image_upload_to, verbose_name="ไฟล์รูป")
    caption = models.CharField(max_length=255, blank=True, verbose_name="คำบรรยาย")
    is_portrait = models.BooleanField(
        default=False, help_text="ติ๊กถ้าต้องการให้รูปสูง (70vh)", verbose_name="รูปแนวตั้ง"
    )
    order = models.PositiveIntegerField(
        default=0, verbose_name="ลำดับแสดง", help_text="เลขยิ่งน้อยยิ่งอยู่บน"
    )

    class Meta:
        ordering = ["order", "id"]
        verbose_name = "รูปภาพกิจกรรม"
        verbose_name_plural = "รูปภาพกิจกรรม"
        constraints = [
            models.UniqueConstraint(
                fields=["section", "order"], name="uniq_image_order_per_section"
            ),
        ]

    def __str__(self) -> str:
        return f"{self.section.title} - {self.caption or self.image.name}"


# --------- Generic Menu (ใหม่) ---------
class Menu(models.Model):
    """
    กลุ่มเมนู เช่น 'activity', 'csr', 'careers'
    slug ต้องไม่ซ้ำ และใช้อ้างถึงใน template/context processor
    """

    name = models.CharField(max_length=120, verbose_name="ชื่อกลุ่มเมนู")
    slug = models.SlugField(max_length=60, unique=True, verbose_name="รหัสกลุ่ม (ไม่ซ้ำ)")

    class Meta:
        verbose_name = "เมนู (กลุ่ม)"
        verbose_name_plural = "เมนู (กลุ่ม)"

    def __str__(self) -> str:
        return f"{self.name} ({self.slug})"


class MenuItem(models.Model):
    menu = models.ForeignKey(
        Menu, on_delete=models.CASCADE, related_name="items", verbose_name="อยู่ในเมนู"
    )
    label = models.CharField(max_length=200, verbose_name="ข้อความเมนู")
    # เลือกปลายทางได้ 3 แบบ: Activity page, Django named URL, หรือ external URL
    activity_page = models.ForeignKey(
        Activity,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        verbose_name="ลิงก์ไป Activity",
    )
    named_url = models.CharField(
        max_length=200,
        blank=True,
        verbose_name="Django named URL",
        help_text="เช่น 'contact_us' หรือ 'activity_detail' (จะ reverse ให้อัตโนมัติ)",
    )
    url = models.CharField(
        max_length=500,
        blank=True,
        verbose_name="External URL",
        help_text="เช่น /careers/job-openings/ หรือ https://example.com",
    )
    open_new_tab = models.BooleanField(default=False, verbose_name="เปิดแท็บใหม่")
    order = models.PositiveIntegerField(default=0, verbose_name="ลำดับ")

    class Meta:
        ordering = ["order", "id"]
        verbose_name = "เมนู (รายการ)"
        verbose_name_plural = "เมนู (รายการ)"

    def __str__(self) -> str:
        return f"{self.menu.slug} · {self.label}"

    def clean(self):
        # ต้องระบุอย่างน้อย 1 ช่องจาก (activity_page / named_url / url)
        filled = [bool(self.activity_page), bool(self.named_url), bool(self.url)]
        if sum(filled) == 0:
            raise ValidationError(
                "ต้องเลือกปลายทางอย่างน้อย 1 แบบ (Activity / named URL / URL)"
            )
        if sum(filled) > 1:
            raise ValidationError("เลือกปลายทางได้เพียง 1 แบบเท่านั้น")

    def resolved_href(self) -> str:
        """คืน URL จริงที่ใช้ใน <a href>"""
        if self.activity_page:
            return self.activity_page.get_absolute_url()
        if self.named_url:
            try:
                return reverse(self.named_url)
            except Exception:
                return "#"  # กันพังถ้า named_url สะกดผิด
        return self.url or "#"
