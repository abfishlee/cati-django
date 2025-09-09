# board/urls.py

from django.urls import path

from . import views

# Django가 URL을 인식하기 위해 사용하는 '애플리케이션 네임스페이스'입니다.
# 템플릿에서 {% url 'board:post_list' %} 와 같이 사용됩니다.
app_name = "board"

# ★★★ 가장 중요한 부분 ★★★
# Django는 반드시 'urlpatterns'라는 이름의 리스트를 찾습니다.
# 이 변수 이름에 오타가 있으면 이전에 겪으신 오류가 발생합니다.
urlpatterns = [
    # 웹 페이지를 보여주는 URL
    path("", views.post_list, name="post_list"),
    # --- 데이터 API를 위한 URL ---
    # GET 요청으로 전체 목록 가져오기
    path("api/posts/", views.posts_api, name="posts_api"),
    # POST 요청으로 새 글 생성하기
    path("api/posts/create/", views.create_post_api, name="create_post_api"),
    # 특정 글 조회, 수정, 삭제
    path("api/posts/<int:pk>/", views.post_detail_api, name="post_detail_api"),
]
