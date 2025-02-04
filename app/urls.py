from app import views
from rest_framework import routers

router = routers.SimpleRouter()

router.register(r"studies", views.StudyViewSet)
router.register(r"assays", views.AssayViewSet)

urlpatterns = router.urls