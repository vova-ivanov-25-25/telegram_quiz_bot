from telegram import Update
from telegram.ext import ContextTypes
from questions import QUESTIONS
from keyboard import make_options_keyboard
from utils import load_stats, save_stats

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    text = (
        f"Привет, {user.first_name}!\n"
        "Ответь на несколько вопросов.\n"
        "Команды: /quiz — начать, /stats — статистика, /help — помощь"
    )
    await update.message.reply_text(text)

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Используй /quiz чтобы начать опрос.")

async def quiz_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['score'] = 0
    context.user_data['qindex'] = 0
    await send_question(update, context)

async def send_question(update_or_callback, context: ContextTypes.DEFAULT_TYPE):
    qindex = context.user_data.get('qindex', 0)
    if qindex >= len(QUESTIONS):
        score = context.user_data.get('score', 0)
        total = len(QUESTIONS)
        user = update_or_callback.effective_user

        stats = load_stats()
        stats[str(user.id)] = {
            'username': user.username or user.first_name,
            'score': score,
            'total': total
        }
        save_stats(stats)

        await update_or_callback.message.reply_text(f"Опрос завершён! Ваш результат: {score}/{total}")
        return

    q = QUESTIONS[qindex]

    if hasattr(update_or_callback, 'callback_query') and update_or_callback.callback_query:
        await update_or_callback.callback_query.message.reply_text(
            q['q'], reply_markup=make_options_keyboard(q['options'])
        )
    else:
        await update_or_callback.message.reply_text(
            q['q'], reply_markup=make_options_keyboard(q['options'])
        )

async def answer_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user_answer = query.data

    try:
        await query.edit_message_reply_markup(reply_markup=None)
    except Exception:
        pass

    await query.message.reply_text(f"Ваш ответ: {user_answer}")

    qindex = context.user_data.get('qindex', 0)
    if qindex < len(QUESTIONS):
        correct = QUESTIONS[qindex]['correct']
        if user_answer.strip() == correct.strip():
            context.user_data['score'] = context.user_data.get('score', 0) + 1

    context.user_data['qindex'] = qindex + 1
    await send_question(update, context)

async def stats_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    stats = load_stats()
    user = update.effective_user
    rec = stats.get(str(user.id))
    if not rec:
        await update.message.reply_text("Статистики нет — пройдите квиз через /quiz")
        return
    await update.message.reply_text(
        f"Последний результат: {rec.get('score')}/{rec.get('total')} (пользователь: {rec.get('username')})"
    )
