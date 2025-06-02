-- 작업자: 다예

-- "게시글-태그 연결" 
-- 명령어: psql -U realworld_user -d realworld -f 04_article_tag_link.sql

-- 1. 기존 태그 연결 삭제
DELETE FROM public."_ArticleToTag"
WHERE "A" = 8;

-- 2. 태그 연결 다시 삽입
INSERT INTO public."_ArticleToTag" ("A", "B")
SELECT 1, id  -- 게시글 ID = 1, 태그 ID = 각 랜덤 태그
FROM public."Tag"
WHERE name LIKE 'tag_%';