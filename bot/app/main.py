import os
import interactions
from interactions import Client, Intents, Permissions, listen, slash_command, SlashContext, OptionType, slash_default_member_permission, slash_option, Modal, ParagraphText, ShortText, User, Member, component_callback, modal_callback, ComponentContext, ComponentCommand, Button, ButtonStyle, integration_types, ModalContext
from dotenv import load_dotenv
import requests


# Create a bot instance with the specified intents
bot = Client(intents=Intents.GUILDS |
             Intents.GUILD_MEMBERS | Intents.GUILD_MESSAGES | Intents.MESSAGE_CONTENT)
# intents are what events we want to receive from discord, `DEFAULT` is usually fine


@listen()  # this decorator tells snek that it needs to listen for the corresponding event, and run this coroutine
async def on_ready():
    # This event is called when the bot is ready to respond to commands
    print("Ready")
    print(f"This bot is owned by {bot.owner}")




@listen()
async def on_member_join(event: interactions.api.events.discord.MemberAdd):
    print(f"{event.member.username} joined")

    button = Button(
        style=ButtonStyle.PRIMARY,
        label="Fill out join form",
        custom_id="open_join_form"
    )

    try:
        # Find the "verification" channel in the guild
        guild = bot.get_guild(event.guild_id)  # Removed 'await' here
        verification_channel = next(
            (channel for channel in guild.channels if channel.name.lower() == "verification"), None)

        if verification_channel:
            # Send the join form button to the "verification" channel
            await verification_channel.send(
                f"👋 Welcome {event.member.mention}! Please click the button below to fill out the join form:",
                components=button
            )
            print(f"Sent join form button to the 'verification' channel for {event.member.username}")
        else:
            print("❌ 'Verification' channel not found in the server")

    except Exception as e:
        print(f"Error sending join form to 'verification' channel: {e}")


@component_callback("open_join_form")
async def on_button_click(ctx: ComponentContext):

    join_modal = Modal(
        ShortText(label="Name", required=True,
                  placeholder="Enter your name", custom_id="name_modal"),
        ShortText(label="Email", required=True,
                  placeholder="Enter your email", custom_id="email_modal"),
        ShortText(label="Student ID", required=True,
                  placeholder="Enter your student ID", custom_id="student_id_modal"),
        title="Join Form",
        custom_id="join_form"
    )
   
    await ctx.send_modal(join_modal)
    

@modal_callback("join_form")
async def on_modal_submit(ctx: ComponentContext, name_modal: str, email_modal: str, student_id_modal: str):
    try:
        # Respond *immediately* to avoid interaction timeout
        await ctx.send(
            f"✅ Thanks for submitting your info!\n**Name**: {name_modal}\n**Email**: {email_modal}\n**Student ID**: {student_id_modal}",
            ephemeral=True
        )

    
        guild = bot.get_guild(ctx.guild_id) 
        member = guild.get_member(ctx.author.id)  

      
        student_role = next((role for role in guild.roles if role.name.lower() == "student"), None)

        if student_role:
           
            await member.add_role(student_role)
            print(f"Assigned 'Student' role to {member.username}")
        else:
            print("❌ 'Student' role not found in the server")

       
        data = {
            'name': name_modal,
            'email': email_modal,
            'student_id': student_id_modal,
        }
      
        # requests.post(url="https://rag-dev.up.railway.app/users/", json=data)

    except Exception as e:
        print(f"❌ Error handling modal: {e}")


@listen()
async def on_message_create(event: interactions.api.events.discord.MessageCreate):
    # This event is called when a message is sent in a channel the bot can see
    print(type(event))
    print(f"message received: {event.message.jump_url}")
    if event.message.author.id != bot.user.id:
        await event.message.channel.send("lmao")

# command to create a thread from the current channel


@slash_command(name="chat", description="Create a thread from the current channel")
# string option
@slash_option(
    name="string_option",
    description="A string option for the command",
    required=True,
    opt_type=OptionType.STRING
)

# function that takes a SlashContext and a string option
async def create_thread_with_option(ctx: SlashContext, string_option: str):
    thread = await ctx.channel.create_thread(name=string_option,  # type: ignore
                                             auto_archive_duration=60)  # type: ignore
    await ctx.send(f"Thread created: {thread.mention}")

@listen()
async def on_message_create_in_thread(event: interactions.api.events.discord.MessageCreate):
    # Check if the channel is a thread
    if event.message.channel.type in [
        interactions.ChannelType.GUILD_PUBLIC_THREAD,
        interactions.ChannelType.GUILD_PRIVATE_THREAD
    ] and event.message.author.id != bot.user.id:
        message_content = event.message.content
        message_user = event.message.author
        print(f"Message in thread: {message_content}")
        print(f"user who sent: {message_user}")

load_dotenv()
bot.start(os.getenv("DISCORD_TOKEN"))
