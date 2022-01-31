import os
from routes.utils import app
from quart import Quart, redirect, url_for, render_template, request
import os

app = Quart(__name__)

#, requires_authorization, Unauthorized

try:
  from quart_discord import DiscordOAuth2Session, requires_authorization, Unauthorized
except:
  subprocess.check_call([sys.executable, "-m", "pip", "install", "quart-discord"])
  from quart_discord import DiscordOAuth2Session, requires_authorization, Unauthorized

app.secret_key = os.environ.get("session")
os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "true"
app.config["DISCORD_CLIENT_ID"] = 900992402356043806
app.config["DISCORD_CLIENT_SECRET"] = os.environ.get("CLIENT_SECRET")
app.config["DISCORD_REDIRECT_URI"] = os.environ.get("RI")
app.config["DISCORD_BOT_TOKEN"] = os.environ.get("token")
discordd = DiscordOAuth2Session(app)

@app.route("/")
async def home():
  logged = ""
  lst = []
  data = {}

  if await discordd.authorized:
    logged = True
    user = await discordd.fetch_user()
    database.load()

  return await render_template("index.html", logged=logged)


@app.route("/login/")
async def login():
  return await discordd.create_session(scope=["identify", "guilds"])

@app.route("/logout/")
async def logout():
  discordd.revoke()
  return redirect(url_for(".home"))

@app.route("/me/")
@requires_authorization
async def me():
  user = await discordd.fetch_user()
  return redirect(url_for(".home"))

@app.route("/callback/")
async def callback():
  await discordd.callback()
  try:
    return redirect(bot.url)
  except:
    return redirect(url_for(".me"))

@app.errorhandler(Unauthorized)
async def redirect_unauthorized(e):
  bot.url = request.url
  return redirect(url_for(".login"))