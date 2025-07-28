import html

from telegram import Update, ext
from telegram.constants import ParseMode

from .config import settings
from .context import WebhookDataContext
from .schemas import WebhookData


async def start_hdlr(update: Update, context: WebhookDataContext) -> None:
    """Display a message with instructions on how to use this bot."""

    assert update.message is not None

    assert update.effective_user is not None
    assert update.effective_chat is not None
    user_id = update.effective_user.id
    chat_id = update.effective_chat.id
    await update.message.reply_markdown_v2(
        f'你的用户 ID `{user_id}`, 当前对话 ID `{chat_id}`'
    )

    wh = settings.TELEGRAM_WEBHOOK_URL
    payload_url = html.escape(f'{wh}{chat_id}/users/{user_id}?value=a&value=b')
    text = (
        f'检查程序正在运行 <code>{wh}health-check</code>.\n\n'
        f'推送测试数据 <code>{payload_url}</code>.'
    )
    await update.message.reply_html(text=text)


async def webhook_data_hdlr(
    update: WebhookData,
    context: WebhookDataContext,
) -> None:
    print('收到 webhook 数据')
    chat_member = await context.bot.get_chat_member(
        chat_id=update.chat_id,
        user_id=update.user_id,
    )

    assert isinstance(context.user_data, dict)
    values = context.user_data.setdefault('values', [])
    for payload in update.value:
        values.append(payload)

    combined_payloads = '</code>\n• <code>'.join(values)
    text = (
        f'用户 {chat_member.user.mention_html()} 收到如下内容 \n\n'
        f'• <code>{combined_payloads}</code>'
    )
    await context.bot.send_message(
        chat_id=update.chat_id,
        text=text,
        parse_mode=ParseMode.HTML,
    )


handlers = [
    ext.CommandHandler('start', start_hdlr),
    ext.TypeHandler(type=WebhookData, callback=webhook_data_hdlr),
]
