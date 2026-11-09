from typing import List, Dict, Any, Optional
from .knowledge_base import STORY_CHAPTERS
from ..schemas import StoryChapter

class StoryService:
    def __init__(self):
        self.chapters: List[Dict[str, Any]] = STORY_CHAPTERS

    def get_all_chapters(self) -> List[StoryChapter]:
        return [StoryChapter(**c) for c in self.chapters]

    def get_chapter_by_id(self, chapter_id: str) -> Optional[StoryChapter]:
        for c in self.chapters:
            if c["id"] == chapter_id or c["number"] == chapter_id:
                return StoryChapter(**c)
        return None

story_service = StoryService()

