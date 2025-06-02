-- 작업자: 다예

-- "게시글 생성" 
-- 명령어: psql -U realworld_user -d realworld -f 02_article_seed.sql

-- 게시글 초기화 + 시퀀스 리셋
-- TRUNCATE public."Article" RESTART IDENTITY CASCADE;

-- 게시글 INSERT (중복 slug는 무시)
INSERT INTO "Article" (
  slug, title, description, body,
  "createdAt", "updatedAt", "authorId"
)
SELECT
  -- 랜덤한 slug: "slug-" + 8자리 해시값 (중복 가능성 낮음)
  'slug-' || substr(md5(random()::text), 1, 8),
  '랜덤 타이틀 ' || gs,  -- 타이틀
  '랜덤 설명 ' || gs,  -- 설명
  '랜덤 본문 ' || gs,  -- 본문
  now(), now(),  -- 생성일 / 수정일
  1           -- 작성자: 항상 authorId = 1

FROM generate_series(1, 50) AS gs 
ON CONFLICT (slug) DO NOTHING;

-- 게시글 개수 확인 (랜덤 타이틀 기준)
SELECT COUNT(*) FROM "Article"
WHERE title LIKE '랜덤 타이틀%';

