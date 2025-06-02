-- 작업자: 다예

-- "댓글 삽입" 
-- 명령어: psql -U realworld_user -d realworld -f 05_comment_seed.sql

-- 1. 기존 댓글 데이터 삭제 + ID 초기화
-- TRUNCATE public."Comment" RESTART IDENTITY;

-- 2. 랜덤 댓글 10개 생성 및 삽입
DO
$$
DECLARE
    i INT := 1;
    random_body TEXT;
BEGIN
    WHILE i <= 20 LOOP
        -- 랜덤 댓글 내용 생성
        random_body := '댓글' || i || '_' || substr(md5(random()::text), 1, 6);

        -- -- 실제 존재하는 게시글 중 하나를 랜덤 선택
        -- SELECT id INTO random_article_id
        -- FROM public."Article"
        -- ORDER BY random()
        -- LIMIT 1;

        -- 댓글 삽입 (주의: 대소문자 정확히 반영)
        INSERT INTO public."Comment"(body, "articleId", "authorId", "createdAt", "updatedAt")
        VALUES (
            random_body,
            1,  -- 게시글 ID 고정
            1,  -- 작성자 ID 고정
            now(),  -- 생성 시간
            now()  -- 수정 시간
        );

        i := i + 1;
    END LOOP;
END
$$;

-- 3. 삽입 확인
SELECT * FROM public."Comment"
ORDER BY id ASC;
