{\rtf1\ansi\ansicpg1251\cocoartf2761
\cocoatextscaling0\cocoaplatform0{\fonttbl\f0\fswiss\fcharset0 Helvetica;}
{\colortbl;\red255\green255\blue255;}
{\*\expandedcolortbl;;}
\paperw11900\paperh16840\margl1440\margr1440\vieww11520\viewh8400\viewkind0
\pard\tx720\tx1440\tx2160\tx2880\tx3600\tx4320\tx5040\tx5760\tx6480\tx7200\tx7920\tx8640\pardirnatural\partightenfactor0

\f0\fs24 \cf0 import logging\
from telegram import Update\
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes, ConversationHandler\
import gspread\
from oauth2client.service_account import ServiceAccountCredentials\
from datetime import datetime\
\
# \uc0\u1053 \u1072 \u1079 \u1074 \u1072 \u1085 \u1080 \u1103  \u1096 \u1072 \u1075 \u1086 \u1074 \
SOBYTIE, MYSLI, EMOCII, REAKCII = range(4)\
\
# \uc0\u1053 \u1072 \u1089 \u1090 \u1088 \u1086 \u1081 \u1082 \u1080  Google \u1058 \u1072 \u1073 \u1083 \u1080 \u1094 \u1099 \
SCOPE = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']\
CREDS_FILE = 'seraphic-disk-427019-u9-33826b5b1941.json'  # \uc0\u1048 \u1084 \u1103  \u1090 \u1074 \u1086 \u1077 \u1075 \u1086  JSON-\u1092 \u1072 \u1081 \u1083 \u1072 \
SPREADSHEET_NAME = 'PIRUSdiary'\
\
# \uc0\u1053 \u1072 \u1089 \u1090 \u1088 \u1086 \u1081 \u1082 \u1072  \u1083 \u1086 \u1075 \u1080 \u1088 \u1086 \u1074 \u1072 \u1085 \u1080 \u1103 \
logging.basicConfig(level=logging.INFO)\
\
# \uc0\u1055 \u1086 \u1076 \u1082 \u1083 \u1102 \u1095 \u1072 \u1077 \u1084 \u1089 \u1103  \u1082  \u1090 \u1072 \u1073 \u1083 \u1080 \u1094 \u1077 \
creds = ServiceAccountCredentials.from_json_keyfile_name(CREDS_FILE, SCOPE)\
client = gspread.authorize(creds)\
sheet = client.open(SPREADSHEET_NAME).sheet1\
\
# \uc0\u1061 \u1088 \u1072 \u1085 \u1080 \u1083 \u1080 \u1097 \u1077  \u1074 \u1088 \u1077 \u1084 \u1077 \u1085 \u1085 \u1099 \u1093  \u1086 \u1090 \u1074 \u1077 \u1090 \u1086 \u1074 \
user_data = \{\}\
\
# \uc0\u1057 \u1090 \u1072 \u1088 \u1090 \
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:\
    await update.message.reply_text("\uc0\u1055 \u1088 \u1080 \u1074 \u1077 \u1090 ! \u1044 \u1072 \u1074 \u1072 \u1081  \u1085 \u1072 \u1095 \u1085 \u1105 \u1084  \u1090 \u1074 \u1086 \u1081  \u1057 \u1052 \u1069 \u1056 -\u1076 \u1085 \u1077 \u1074 \u1085 \u1080 \u1082  \u55356 \u57137 \\n\u1063 \u1090 \u1086  \u1089 \u1083 \u1091 \u1095 \u1080 \u1083 \u1086 \u1089 \u1100  (\u1057 \u1086 \u1073 \u1099 \u1090 \u1080 \u1077 )?")\
    return SOBYTIE\
\
async def sobytie(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:\
    user_data[update.effective_user.id] = \{'sobytie': update.message.text\}\
    await update.message.reply_text("\uc0\u1050 \u1072 \u1082 \u1080 \u1077  \u1091  \u1090 \u1077 \u1073 \u1103  \u1073 \u1099 \u1083 \u1080  \u1084 \u1099 \u1089 \u1083 \u1080 ?")\
    return MYSLI\
\
async def mysli(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:\
    user_data[update.effective_user.id]['mysli'] = update.message.text\
    await update.message.reply_text("\uc0\u1050 \u1072 \u1082 \u1080 \u1077  \u1101 \u1084 \u1086 \u1094 \u1080 \u1080  \u1090 \u1099  \u1087 \u1086 \u1095 \u1091 \u1074 \u1089 \u1090 \u1074 \u1086 \u1074 \u1072 \u1083 \u1072 ?")\
    return EMOCII\
\
async def emocii(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:\
    user_data[update.effective_user.id]['emocii'] = update.message.text\
    await update.message.reply_text("\uc0\u1050 \u1072 \u1082 \u1080 \u1077  \u1090 \u1077 \u1083 \u1077 \u1089 \u1085 \u1099 \u1077  \u1080 \u1083 \u1080  \u1087 \u1086 \u1074 \u1077 \u1076 \u1077 \u1085 \u1095 \u1077 \u1089 \u1082 \u1080 \u1077  \u1088 \u1077 \u1072 \u1082 \u1094 \u1080 \u1080  \u1090 \u1099  \u1079 \u1072 \u1084 \u1077 \u1090 \u1080 \u1083 \u1072 ?")\
    return REAKCII\
\
async def reakcii(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:\
    user_data[update.effective_user.id]['reakcii'] = update.message.text\
\
    # \uc0\u1057 \u1086 \u1093 \u1088 \u1072 \u1085 \u1103 \u1077 \u1084  \u1074  \u1090 \u1072 \u1073 \u1083 \u1080 \u1094 \u1091 \
    data = user_data[update.effective_user.id]\
    row = [datetime.now().strftime("%Y-%m-%d %H:%M"), data['sobytie'], data['mysli'], data['emocii'], data['reakcii']]\
    sheet.append_row(row)\
\
    await update.message.reply_text("\uc0\u1057 \u1087 \u1072 \u1089 \u1080 \u1073 \u1086 , \u1074 \u1089 \u1105  \u1079 \u1072 \u1087 \u1080 \u1089 \u1072 \u1085 \u1086  \u9989 \\n\u1053 \u1072 \u1087 \u1080 \u1096 \u1080  /start \u1095 \u1090 \u1086 \u1073 \u1099  \u1079 \u1072 \u1087 \u1086 \u1083 \u1085 \u1080 \u1090 \u1100  \u1077 \u1097 \u1105  \u1088 \u1072 \u1079 .")\
    return ConversationHandler.END\
\
async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:\
    await update.message.reply_text("\uc0\u1054 \u1082 \u1077 \u1081 , \u1074  \u1076 \u1088 \u1091 \u1075 \u1086 \u1081  \u1088 \u1072 \u1079 !")\
    return ConversationHandler.END\
\
# \uc0\u1047 \u1072 \u1087 \u1091 \u1089 \u1082 \
def main():\
    app = ApplicationBuilder().token("7862781306:AAEZjQ1HkXro61YTnGxFHUQE6MRInTW8J9s").build()\
\
    conv_handler = ConversationHandler(\
        entry_points=[CommandHandler('start', start)],\
        states=\{\
            SOBYTIE: [MessageHandler(filters.TEXT & ~filters.COMMAND, sobytie)],\
            MYSLI: [MessageHandler(filters.TEXT & ~filters.COMMAND, mysli)],\
            EMOCII: [MessageHandler(filters.TEXT & ~filters.COMMAND, emocii)],\
            REAKCII: [MessageHandler(filters.TEXT & ~filters.COMMAND, reakcii)],\
        \},\
        fallbacks=[CommandHandler('cancel', cancel)],\
    )\
\
    app.add_handler(conv_handler)\
\
    print("\uc0\u1041 \u1086 \u1090  \u1079 \u1072 \u1087 \u1091 \u1097 \u1077 \u1085 . \u1053 \u1072 \u1078 \u1084 \u1080  Ctrl+C \u1076 \u1083 \u1103  \u1086 \u1089 \u1090 \u1072 \u1085 \u1086 \u1074 \u1082 \u1080 .")\
    app.run_polling()\
\
if __name__ == '__main__':\
    main()}