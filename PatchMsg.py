"""
Patch for qq-botpy==1.2.1
Adds missing GROUP_MESSAGE_CREATE parser.

⚠️ 严格遵循 GroupMessage(api, event_id, data) 签名
"""

import json
from typing import Any, Dict

import botpy
from botpy import logging as botpy_logging
from botpy.connection import ConnectionState
from botpy.message import GroupMessage

logger = botpy_logging.get_logger("patch_qqofficial")

# GroupMessage 有 __slots__ 限制，用字典存额外属性
_msg_author_bot: dict = {}


def _ensure_group_message_create_parser() -> None:
    if hasattr(ConnectionState, "parse_group_message_create"):
        return

    def parse_group_message_create(self: ConnectionState, payload: Dict[str, Any]) -> None:
        try:
            # ✅ qq-botpy 1.2.1 的真实签名
            data = payload.get("d", {})
            group_message = GroupMessage(
                self.api,
                payload.get("id"),      # event_id
                data,                   # data
            )
            # 直接从原始 JSON 提取 author.bot（GroupMessage 有 __slots__，用字典存）
            # ⚠️ 用 data.id（消息 ID）而非 payload.id（事件 ID），因为 GroupMessage.id 指向 data.id
            msg_id = data.get("id", "")
            _msg_author_bot[msg_id] = data.get("author", {}).get("bot", False)

            logger.info("[QQOfficial] 📥 收到消息 JSON:\n%s",
                         json.dumps(payload, ensure_ascii=False, indent=2))

            self._dispatch("group_message_create", group_message)

        except Exception as e:
            logger.warning(
                "[QQOfficial] Failed to parse GROUP_MESSAGE_CREATE: %s",
                e,
                exc_info=True,
            )

    setattr(ConnectionState, "parse_group_message_create", parse_group_message_create)


def clean_group_message_content(content: str, mentions: list) -> str:
    if not content:
        return ""
    for m in mentions or []:
        # 兼容 _User 对象 和 dict
        mid = getattr(m, "id", None) or (m.get("id") if isinstance(m, dict) else None)
        if mid:
            content = content.replace(f"<@{mid}>", "").replace(f"<@!{mid}>", "")
    return content.strip()


def is_bot_mentioned(mentions: list) -> bool:
    for m in mentions or []:
        if isinstance(m, dict):
            if m.get("is_you"):
                return True
        elif getattr(m, "is_you", False):
            return True
    return False


def is_author_bot(msg_id: str) -> bool:
    """判断某条消息的作者是否是机器人"""
    return _msg_author_bot.get(msg_id, False)


__all__ = [
    "_ensure_group_message_create_parser",
    "clean_group_message_content",
    "is_bot_mentioned",
    "is_author_bot",
]