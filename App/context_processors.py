# App/context_processors.py
from .models import Menu


def site_menus(request):
    """
    ดึงเมนูกลุ่มสำคัญเข้าเทมเพลต:
    - menu_activity : รายการในเมนู Activity
    - menu_csr      : รายการในเมนู CSR
    - menu_careers  : รายการในเมนู Careers
    (ถ้าไม่มีใน DB จะได้ลิสต์ว่าง)
    """

    def get_items(slug):
        try:
            menu = Menu.objects.prefetch_related("items").get(slug=slug)
            return list(menu.items.all())
        except Menu.DoesNotExist:
            return []

    return {
        "menu_activity": get_items("activity"),
        "menu_csr": get_items("csr"),
        "menu_careers": get_items("careers"),
    }
