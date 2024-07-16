import discord
from discord.ext import commands
import datetime


TOKEN = "<token>"
DESTINATION_CHANNEL = 1122444666726526996 


intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="/", intents=intents)


class EntryModal(discord.ui.Modal, title="Миграционная форма"):
    ign = discord.ui.TextInput(
        label = "Никнейм",
        style = discord.TextStyle.short,
        custom_id = "ign", 
        required = True, 
        min_length = 3, 
        max_length = 16,
    )
    source = discord.ui.TextInput(
        label = "Откуда вы узнали про нас?",
        style = discord.TextStyle.long,
        custom_id = "src", 
        required = True,
    )
    extra = discord.ui.TextInput(
        label = "Дополнительно: опишите своего персонажа",
        style = discord.TextStyle.long,
        placeholder="Это совсем не обязательно.",
        custom_id = "extra", 
        required = False,
    )

    async def on_submit(self, interaction: discord.Interaction):
        embed = discord.Embed(
            title = self.title,
            description=f"**{self.ign.label}**\n{self.ign}\n\n**{self.source.label}**\n{self.source}\n\n**{self.extra.label}**\n{self.extra}", 
            timestamp=datetime.datetime.now(), 
            color=discord.Colour.dark_gold())
        embed.set_author(
            name = interaction.user,
            icon_url=interaction.user.avatar
        )
        await interaction.guild.get_channel(DESTINATION_CHANNEL).send(embed=embed)
        await interaction.response.send_message("Ваша заявка обработана. Осталось только подождать.\nСпам заявками наказуем.", ephemeral=True)


class EntryView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="", custom_id="reg_button", style=discord.ButtonStyle.secondary, emoji="🌵")
    async def button_callback(self, button, interaction):
        await button.response.send_modal(EntryModal())


@bot.event
async def on_ready():
    print(f"Bot is ready and running as {bot.user}")
    embed = discord.Embed(
        title = "Bot is ready and running",
        timestamp = datetime.datetime.now(),
        color=discord.Colour.brand_green())
    await bot.get_channel(DESTINATION_CHANNEL).send(embed=embed)


@bot.command()
async def deploy(ctx):
    await ctx.send(file=discord.File("banner.png"))
    await ctx.send("# Добро пожаловать в Июль\nПросто нажмите на кактус. Давайте. Сделайте это.", view=EntryView())

bot.run(TOKEN)

