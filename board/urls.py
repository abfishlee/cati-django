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
    # --- 웹 페이지 렌더링을 위한 URL ---
    # 사용자가 '.../board/' 주소로 접근하면 views.py의 post_list 함수를 실행합니다.
    path("", views.post_list, name="post_list"),
    # --- 데이터 처리를 위한 API(Application Programming Interface) URL ---
    # '/api/posts/' 주소로 GET 요청: 모든 게시글 목록을 JSON으로 반환
    path("api/posts/", views.posts_api, name="posts_api"),
    # '/api/posts/create/' 주소로 POST 요청: 새 게시글 생성
    path("api/posts/create/", views.create_post_api, name="create_post_api"),
    # '/api/posts/<int:pk>/' 주소로 GET, PUT, DELETE 요청: 특정 게시글 조회, 수정, 삭제
    path("api/posts/<int:pk>/", views.post_detail_api, name="post_detail_api"),
]
