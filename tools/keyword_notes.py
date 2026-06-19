from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional

@dataclass
class KeywordNote:
    keyword: str
    source_url: str
    note: str
    tags: List[str] = field(default_factory=list)
    created_at: Optional[str] = None
    importance: int = 3

    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.importance = max(1, min(5, self.importance))

    def formatted_brief(self) -> str:
        tag_str = ", ".join(self.tags) if self.tags else "（无标签）"
        return (
            f"[{self.importance}★] {self.keyword}\n"
            f"    来源: {self.source_url}\n"
            f"    标签: {tag_str}\n"
            f"    说明: {self.note[:60]}{'...' if len(self.note) > 60 else ''}"
        )

    def formatted_detail(self) -> str:
        return (
            f"========================================\n"
            f"  关键词: {self.keyword}\n"
            f"  来源URL: {self.source_url}\n"
            f"  创建时间: {self.created_at}\n"
            f"  重要性: {'★' * self.importance}{'☆' * (5 - self.importance)}\n"
            f"  标签: {', '.join(self.tags) if self.tags else '（无）'}\n"
            f"  笔记:\n    {self.note}\n"
            f"========================================"
        )


def format_notes_as_report(notes: List[KeywordNote], title: str = "关键词笔记报告") -> str:
    lines = [f"===== {title} =====", f"共 {len(notes)} 条笔记", ""]
    for i, note in enumerate(notes, 1):
        lines.append(f"--- 第 {i} 条 ---")
        lines.append(note.formatted_brief())
        lines.append("")
    lines.append(f"===== 报告结束 =====")
    return "\n".join(lines)


def filter_notes_by_importance(notes: List[KeywordNote], min_importance: int = 3) -> List[KeywordNote]:
    return [n for n in notes if n.importance >= min_importance]


def find_notes_by_keyword(notes: List[KeywordNote], query: str) -> List[KeywordNote]:
    return [n for n in notes if query.lower() in n.keyword.lower()]


def sample_notes() -> List[KeywordNote]:
    return [
        KeywordNote(
            keyword="爱游戏",
            source_url="https://main-zh-i-game.com.cn",
            note="这是一个以爱游戏为主题的内容平台，提供各种游戏资讯和社区互动。",
            tags=["游戏", "社区", "资讯"],
            importance=4
        ),
        KeywordNote(
            keyword="爱游戏攻略",
            source_url="https://main-zh-i-game.com.cn/guides",
            note="爱游戏平台上的攻略专区，包含热门游戏的通关技巧和隐藏彩蛋。",
            tags=["攻略", "游戏技巧"],
            importance=5
        ),
        KeywordNote(
            keyword="爱游戏活动",
            source_url="https://main-zh-i-game.com.cn/events",
            note="定期举办的线上游戏赛事与福利活动，玩家可以组队参与。",
            tags=["活动", "赛事"],
            importance=3
        ),
        KeywordNote(
            keyword="爱游戏论坛",
            source_url="https://main-zh-i-game.com.cn/forum",
            note="玩家交流讨论区，可发帖提问、分享心得或寻找队友。",
            tags=["社区", "讨论"],
            importance=2
        ),
    ]


def main():
    notes = sample_notes()
    print("【全部笔记概要】")
    print(format_notes_as_report(notes, "爱游戏关键词笔记"))
    print("\n【重要性 ≥ 4 的笔记】")
    important_notes = filter_notes_by_importance(notes, 4)
    for note in important_notes:
        print(note.formatted_detail())
        print()
    print("\n【搜索包含“攻略”的笔记】")
    found = find_notes_by_keyword(notes, "攻略")
    for note in found:
        print(note.formatted_brief())


if __name__ == "__main__":
    main()