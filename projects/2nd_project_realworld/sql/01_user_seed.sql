-- 작업자: 다예

-- "사용자 생성" 
-- 명령어: psql -U realworld_user -d realworld -f 01_user_seed.sql

-- 0. pgcrypto 확장 설치 (비밀번호 암호화용)
CREATE EXTENSION IF NOT EXISTS pgcrypto;

-- 1. 기존 유저 테이블 초기화 (필요 시 주석 제거)
-- TRUNCATE TABLE "User" RESTART IDENTITY CASCADE;

-- 2. 랜덤 유저 100명 생성 (비밀번호: '1')
INSERT INTO "User" (email, username, password, image)
SELECT
  'user' || gs || '_' || substr(md5(random()::text), 1, 5) || '@naver.com',
  'user_' || gs || '_' || substr(md5(random()::text), 1, 4),
  crypt('1', gen_salt('bf')),  -- 여기서 바로 암호화된 비번 '1' 삽입
  'https://i.pravatar.cc/150?img=' || (10 + gs)
FROM generate_series(1, 100) AS gs;  

-- 3. 결과 확인
SELECT id, email, username, password
FROM public."User"
ORDER BY id;
