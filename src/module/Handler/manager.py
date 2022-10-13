from dataclasses import dataclass
from src.settings import Global
from telethon.tl.functions import channels, users, messages
import io


async def get_description_account(dialog):
    if dialog.is_user:
        return (await Global.client(users.GetFullUserRequest(dialog.entity.id))).full_user.about
    elif dialog.is_channel:
        return (await Global.client(channels.GetFullChannelRequest(dialog.entity.id))).full_chat.about
    else:
        return (await Global.client(messages.GetFullChatRequest(dialog.entity.id))).full_chat.about


async def get_chat_info(dialog):
    this_chat = ChatStencil()

    this_chat.chat_id = dialog.id
    this_chat.name = dialog.title
    this_chat.category = {dialog.is_channel: "channel", dialog.is_group: "group", dialog.is_user: "user"}[True]
    this_chat.phone = dialog.entity.phone if this_chat.category == 'user' else None
    this_chat.tag = dialog.entity.__dict__.get("username")
    await Global.client.download_profile_photo(this_chat.chat_id, file=this_chat.photo)
    this_chat.photo.seek(0)
    this_chat.bio = await get_description_account(dialog)
    this_chat.status = True
    this_chat.active = True if this_chat.category is not "channel" else False

    return this_chat


@dataclass
class ChatStencil:
    chat_id: int = None
    name: str = None
    category: str = None
    phone: int = None
    tag: str = None
    photo: io.BytesIO = io.BytesIO()
    bio: str = None
    status: bool = None
    active: bool = None
