-- 작업자: 다예

-- "유저 간 팔로우" 
-- 명령어: psql -U realworld_user -d realworld -f 06_user_follows.sql

-- 1. 기존 팔로우 데이터 초기화 (선택사항)
-- TRUNCATE public."_UserFollows" RESTART IDENTITY;

-- 2. 팔로우 관계 수동 삽입
INSERT INTO public."_UserFollows"("A", "B") VALUES
    (1, 2),
    (1, 3),
    (1, 4),
    (2, 1),
    (2, 3),
    (2, 4),
    (3, 1),
    (3, 2),
    (3, 4),
    (4, 1),
    (4, 2),
    (4, 3),
    (1, 5),
    (2, 5)
ON CONFLICT DO NOTHING;

-- 3. 확인: 누가 누구를 팔로우하는지 전체 보기
SELECT
  a."username" AS follower,
  b."username" AS following
FROM
  public."_UserFollows" uf
JOIN public."User" a ON uf."A" = a."id"
JOIN public."User" b ON uf."B" = b."id"
ORDER BY a."username", b."username";