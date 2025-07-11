from dataclasses import dataclass


@dataclass
class PostConfig:
    title_min_length: int = 3
    title_max_length: int = 191


@dataclass
class PostServiceConfig:
    post_cache_exp_in_seconds: int = 900  # 15 minutes
    post_cache_key: str = "posts"
