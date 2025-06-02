-- 작업자: 은영

-- "좋아요 매핑"
-- 명령어: psql -U realworld_user -d realworld -f 07_user_favorites.sql

-- 1. 모든 사용자 ID와 모든 게시글 ID를 조합하여 좋아요 하기

-- 사용자 ID (현재 데이터베이스에 실제로 존재하는 모든 사용자 ID를 가져옴)
WITH user_ids AS (
    SELECT "id" AS user_id
    FROM public."User" -- 실제 사용자 테이블 이름
),
-- 게시글 ID (현재 데이터베이스에 실제로 존재하는 모든 게시글 ID를 가져옴)
article_ids AS (
    SELECT "id" AS article_id
    FROM public."Article" -- 실제 게시글 테이블 이름
)
-- 모든 사용자 ID와 모든 게시글 ID를 CROSS JOIN하여 모든 가능한 조합 생성
-- 그리고 그 결과를 _UserFavorites 테이블에 삽입
INSERT INTO public."_UserFavorites" ("A", "B") -- "A"는 게시글 ID, "B"는 사용자 ID
SELECT
    a.article_id,   -- 실제로 존재하는 게시글 ID (A 컬럼)
    u.user_id       -- 실제로 존재하는 사용자 ID (B 컬럼)
FROM
    user_ids u
CROSS JOIN
    article_ids a

ON CONFLICT ("A", "B") DO NOTHING; --이미 존재하는 조합은 무시하고 존재하지 않는 새로운 조합만 삽입하도록 설정

-- 첫 번째 쿼리(INSERT)를 끝내는 세미콜론 (이것은 있어도 됩니다. 다음 SELECT와 구분)
;

-- 삽입이 완료된 후 public."_UserFavorites" 테이블의 내용을 조회
SELECT * FROM public."_UserFavorites";
