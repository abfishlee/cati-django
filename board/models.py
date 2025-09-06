from django.db import models


# 게시글(Post) 데이터를 위한 '설계도'를 정의하는 클래스입니다.
# models.Model을 상속받아 장고 모델로서의 기능을 갖게 됩니다.
class Post(models.Model):
    """
    게시글의 구조를 정의하는 모델입니다.
    각 필드는 데이터베이스 테이블의 컬럼에 해당합니다.
    """

    # 제목: 최대 200자까지 저장 가능한 문자열 필드입니다.
    # verbose_name은 관리자 페이지 등에서 표시될 필드의 별칭입니다.
    title = models.CharField(max_length=200, verbose_name="제목")

    # 내용: 글자 수 제한이 없는 긴 텍스트 필드입니다.
    content = models.TextField(verbose_name="내용")

    # 작성자: 최대 50자까지 저장 가능한 문자열 필드입니다.
    # 나중에 사용자 인증 기능과 연결하여 ForeignKey로 변경할 수 있습니다.
    author = models.CharField(max_length=50, verbose_name="작성자")

    # 생성일: 데이터가 처음 생성될 때의 날짜와 시간이 자동으로 저장됩니다.
    # auto_now_add=True 옵션이 이 기능을 수행합니다.
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="생성일")

    # 수정일: 데이터가 업데이트될 때마다 해당 시점의 날짜와 시간이 자동으로 저장됩니다.
    # auto_now=True 옵션이 이 기능을 수행합니다.
    updated_at = models.DateTimeField(auto_now=True, verbose_name="수정일")

    # 객체가 문자열로 표현될 때, 게시글의 제목을 반환하도록 설정합니다.
    # 주로 장고 관리자 페이지나 디버깅 시에 객체를 쉽게 식별하기 위해 사용됩니다.
    def __str__(self):
        return self.title

    # 모델의 추가 옵션을 정의하는 내부 클래스입니다.
    class Meta:
        # 이 모델의 별칭(단수)을 '게시글'로 설정합니다.
        verbose_name = "게시글"
        # 이 모델의 별칭(복수)을 '게시글 목록'으로 설정합니다.
        verbose_name_plural = "게시글 목록"
        # 게시글 목록을 조회할 때 기본 정렬 순서를 생성일의 내림차순으로 설정합니다.
        # '-' 기호는 내림차순(최신순)을 의미합니다.
        ordering = ["-created_at"]


# Create your models here.
