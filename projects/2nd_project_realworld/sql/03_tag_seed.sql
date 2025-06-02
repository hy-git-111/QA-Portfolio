-- 작업자: 다예

-- "태그 생성" 
-- 명령어: psql -U realworld_user -d realworld -f 03_tag_seed.sql

-- 1. 기존 태그 및 연관된 매핑 테이블 모두 초기화
TRUNCATE public."_ArticleToTag", public."Tag" RESTART IDENTITY CASCADE;

-- 2. 랜덤 태그 100개 생성 및 삽입
DO
$$
DECLARE
    i INT := 0;
    tag_text TEXT;
BEGIN
    WHILE i < 100 LOOP  -- 생성할 태그 수를 여기서 조정
        tag_text := 'tag_' || substr(md5(random()::text), 1, 8); -- tag_ 뒤에 랜덤 문자열
        BEGIN
            INSERT INTO public."Tag"(name)
            VALUES (tag_text);
        EXCEPTION WHEN unique_violation THEN
            -- 중복 발생 시 무시하고 다시 시도
            CONTINUE;
        END;
        i := i + 1;
    END LOOP;
END
$$;

-- 3. 삽입된 결과 확인
SELECT * FROM public."Tag"
ORDER BY id ASC;
