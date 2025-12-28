import discord
from discord.ext import commands
from discord.ui import Button, View

TOKEN = "seu token" #seu token do discord pegue no portal developer application do discord https://discord.com/developers/applications

GUILD_ID = 0000000000000000000  #id do servidor do discord
CHANNEL_ID = 0000000000000000000  #canal em que vai ficar a embed 

ROLE_OLD_ID = 0000000000000000000  # cargo para ser removido quando receber o outro
ROLE_NEW_ID = 0000000000000000000  # cargo verificado

intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

class VerifyView(View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="Verificar ✅", style=discord.ButtonStyle.green)
    async def verify(self, interaction: discord.Interaction, button: Button):
        guild = interaction.guild
        member = interaction.user

        old_role = guild.get_role(ROLE_OLD_ID)
        new_role = guild.get_role(ROLE_NEW_ID)

        if new_role in member.roles:
            await interaction.response.send_message(
                "Você já está verificado.", ephemeral=True
            )
            return

        try:
            if old_role and old_role in member.roles:
                await member.remove_roles(old_role)

            await member.add_roles(new_role)

            await interaction.response.send_message(
                "✅ Verificação concluída! Cargo atualizado.",
                ephemeral=True
            )

        except discord.Forbidden:
            await interaction.response.send_message(
                "Não tenho permissão para gerenciar cargos.",
                ephemeral=True
            )

@bot.event
async def on_ready():
    print(f"Bot online {bot.user}")

    guild = bot.get_guild(GUILD_ID)
    if not guild:
        print("Guild não encontrada")
        return

    channel = guild.get_channel(CHANNEL_ID)
    if not channel:
        print("Canal não encontrado")
        return

    embed = discord.Embed(
        title="🔐 Verificação",
        description="Clique no botão abaixo para se verificar e acessar o servidor.",
        color=discord.Color.green()
    )

    await channel.send(embed=embed, view=VerifyView())

bot.run(TOKEN)