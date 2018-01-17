-- postgresql数据库
-- 豆瓣影评表
DROP TABLE IF EXISTS public.db_movie;
CREATE TABLE public.db_movie(
    user_name character(50),
    comment_time text,
    film_critics text
);
COMMENT ON TABLE public.db_movie IS '豆瓣影评表';
COMMENT ON COLUMN public.db_movie.user_name IS '用户名';
COMMENT ON COLUMN public.db_movie.comment_time IS '评论时间';
COMMENT ON COLUMN public.db_movie.film_critics IS '影评内容';

