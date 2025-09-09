# Django의 필수 기능들을 가져옵니다.
import json  # JSON 데이터를 다루기 위한 라이브러리

from django.forms.models import model_to_dict  # Django 모델 객체를 Python 딕셔너리로 변환하는 함수
from django.http import JsonResponse  # JSON 형식으로 응답을 보내기 위한 클래스
from django.shortcuts import get_object_or_404, render  # HTML 템플릿 렌더링 및 객체 조회를 위한 함수
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.decorators.http import (
    require_http_methods,  # 특정 HTTP 요청 메소드만 허용하는 데코레이터
)

# 현재 앱 폴더(.)의 models.py 파일에서 Post 모델을 가져옵니다.
from .models import Post

# -----------------------------------------------------------------------------
# 1. 웹 페이지 렌더링 뷰 (사용자에게 화면을 보여주는 역할)
# -----------------------------------------------------------------------------


@ensure_csrf_cookie
def post_list(request):
    """
    게시판의 메인 HTML 페이지를 렌더링(보여주는)하는 함수입니다.
    이 함수는 실제 데이터를 포함하지 않은 'post_list.html'이라는 껍데기 페이지만 제공합니다.
    실제 데이터는 페이지가 로드된 후, JavaScript(AG Grid)가 아래의 API 뷰들을
    호출하여 동적으로 화면을 채워넣게 됩니다. (최신 웹 개발 방식)
    """
    return render(request, "board/post_list.html")


# -----------------------------------------------------------------------------
# 2. API(Application Programming Interface) 뷰 (데이터만 주고받는 통신 역할)
# -----------------------------------------------------------------------------


@require_http_methods(["GET"])  # 이 함수는 GET 요청에만 응답하도록 제한합니다.
def posts_api(request):
    """
    AG Grid에 필요한 '전체 게시글 목록'을 JSON 형식으로 제공하는 API입니다.
    """
    try:
        # Post.objects.all() 로 모든 게시글을 가져온 뒤,
        # order_by('-created_at') 를 통해 최신글이 맨 위로 오도록 정렬합니다.
        posts = Post.objects.all().order_by("-created_at")

        # .values()는 모델 객체 목록을 Python 딕셔너리 리스트로 변환해주는 효율적인 방법입니다.
        # 이 과정에서 Python의 datetime 객체가 JSON이 이해할 수 있는 문자열 형태로 자동 변환되어,
        # 이전 단계에서 겪었던 JSON 변환 오류를 원천적으로 방지합니다.
        data = list(posts.values("id", "title", "author", "created_at", "updated_at"))

        # JsonResponse를 사용하여 파이썬 리스트를 안전하게 JSON 데이터로 변환하여 응답합니다.
        # safe=False 옵션은 응답 데이터가 딕셔너리가 아닌 리스트 형태일 때 반드시 필요합니다.
        return JsonResponse(data, safe=False)
    except Exception as e:
        # 데이터베이스 조회 등 서버 내부에서 오류가 발생한 경우,
        # 500 상태 코드와 함께 에러 메시지를 JSON으로 반환합니다.
        return JsonResponse(
            {"error": f"서버에서 데이터를 가져오는 중 오류가 발생했습니다: {str(e)}"},
            status=500,
        )


@require_http_methods(["POST"])  # 이 함수는 POST 요청에만 응답하도록 제한합니다.
def create_post_api(request):
    """'새 게시글 생성' 요청을 처리하는 API입니다."""
    try:
        # 프론트엔드에서 fetch를 통해 보낸 request.body의 JSON 문자열을
        # json.loads()를 사용해 파이썬 딕셔너리로 변환합니다.
        data = json.loads(request.body)

        # Post.objects.create()를 사용하여 새 게시글 객체를 만들고 즉시 데이터베이스에 저장합니다.
        Post.objects.create(
            title=data.get("title"),
            content=data.get("content"),
            author=data.get("author"),
        )

        # 성공적으로 생성되었음을 알리는 201 상태 코드와 간단한 메시지를 반환합니다.
        # 프론트엔드는 이 성공 응답을 받고 그리드를 새로고침합니다.
        return JsonResponse(
            {"message": "게시글이 성공적으로 생성되었습니다."}, status=201
        )
    except json.JSONDecodeError:
        # 프론트엔드가 유효하지 않은 JSON 데이터를 보낸 경우 400 에러를 반환합니다.
        return JsonResponse(
            {"error": "요청 형식이 잘못되었습니다 (Invalid JSON)."}, status=400
        )
    except Exception as e:
        return JsonResponse(
            {"error": f"데이터 저장 중 서버 오류가 발생했습니다: {str(e)}"}, status=500
        )


@require_http_methods(["GET", "PUT", "DELETE"])  # GET, PUT, DELETE 요청에만 응답합니다.
def post_detail_api(request, pk):
    """pk(Primary Key) 값으로 '특정 게시글 하나'를 조회, 수정, 삭제하는 API입니다."""

    # get_object_or_404: 해당 pk의 객체가 있으면 가져오고, 없으면 404 Not Found 에러를
    # 자동으로 발생시켜주는 매우 편리한 Django 단축 함수입니다.
    post = get_object_or_404(Post, pk=pk)

    # --- 요청 메소드에 따라 분기 처리 ---

    if request.method == "GET":  # '상세보기' 요청
        # model_to_dict: Django 모델 객체를 깔끔한 Python 딕셔너리로 변환합니다.
        return JsonResponse(model_to_dict(post))

    elif request.method == "PUT":  # '수정' 요청
        try:
            data = json.loads(request.body)
            # 전달받은 데이터로 게시글 객체의 각 필드를 업데이트합니다.
            # data.get(key, post.title) 구문은, 만약 title 값이 없으면 기존 값을 그대로 사용하라는 의미입니다.
            post.title = data.get("title", post.title)
            post.content = data.get("content", post.content)
            post.author = data.get("author", post.author)
            post.save()  # 변경된 내용을 데이터베이스에 최종 반영합니다.
            return JsonResponse({"message": "게시글이 성공적으로 수정되었습니다."})
        except json.JSONDecodeError:
            return JsonResponse(
                {"error": "요청 형식이 잘못되었습니다 (Invalid JSON)."}, status=400
            )
        except Exception as e:
            return JsonResponse(
                {"error": f"데이터 수정 중 서버 오류가 발생했습니다: {str(e)}"},
                status=500,
            )

    elif request.method == "DELETE":  # '삭제' 요청
        post.delete()  # 객체를 데이터베이스에서 삭제합니다.
        # HTTP 표준에 따라, 삭제 성공 시에는 특별한 내용 없이 204 No Content 상태 코드를 반환하는 것이 가장 좋습니다.
        return JsonResponse({}, status=204)
