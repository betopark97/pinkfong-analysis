--
-- PostgreSQL database dump
--

-- Dumped from database version 16.2
-- Dumped by pg_dump version 16.6 (Homebrew)

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: channel_metadata; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.channel_metadata (
    channel_id text,
    channel_title text,
    description text,
    profile_picture text,
    published_at text,
    country text,
    playlist_id text,
    channel_character text,
    channel_handle text,
    channel_link text
);


ALTER TABLE public.channel_metadata OWNER TO postgres;

--
-- Name: channel_stats; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.channel_stats (
    channel_id text,
    subscriber_count bigint,
    video_count bigint,
    view_count bigint
);


ALTER TABLE public.channel_stats OWNER TO postgres;

--
-- Name: playlist_videos; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.playlist_videos (
    playlist_id text,
    video_id text
);


ALTER TABLE public.playlist_videos OWNER TO postgres;

--
-- Name: tags; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.tags (
    tag_id bigint,
    tag text
);


ALTER TABLE public.tags OWNER TO postgres;

--
-- Name: video_categories; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.video_categories (
    category_id bigint,
    category_name text
);


ALTER TABLE public.video_categories OWNER TO postgres;

--
-- Name: video_metadata; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.video_metadata (
    video_id text,
    published_at text,
    title text,
    description text,
    thumbnails text,
    tags text,
    category_id bigint,
    default_audio_language text,
    duration text
);


ALTER TABLE public.video_metadata OWNER TO postgres;

--
-- Name: video_stats; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.video_stats (
    video_id text,
    view_count bigint,
    like_count double precision,
    comment_count double precision
);


ALTER TABLE public.video_stats OWNER TO postgres;

--
-- Name: video_tags; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.video_tags (
    video_id text,
    tag_id bigint
);


ALTER TABLE public.video_tags OWNER TO postgres;

--
-- PostgreSQL database dump complete
--

