from __future__ import annotations
import logging
from typing import Annotated
from dotenv import load_dotenv
import os

import smtplib
from email.message import EmailMessage

from livekit.agents import (
    AutoSubscribe,
    JobContext,
    WorkerOptions,
    WorkerType,
    cli,
    llm,
    multimodal,
)
from livekit.plugins import openai

load_dotenv()
logger = logging.getLogger("my-worker")
logger.setLevel(logging.INFO)

# print(os.getenv("LIVEKIT_URL"))
# print(os.getenv("LIVEKIT_API_KEY"))
# print(os.getenv("LIVEKIT_API_SECRET"))


def send_email(subject, body, to_email):
    msg = EmailMessage()
    msg.set_content(body)
    msg["Subject"] = subject
    msg["From"] = os.getenv("EMAIL")
    msg["To"] = to_email

    with smtplib.SMTP_SSL(os.getenv("SMTP"), 465) as smtp:
        smtp.login(os.getenv("EMAIL"), os.getenv("PASSWORD"))
        smtp.send_message(msg)


async def entrypoint(ctx: JobContext):
    logger.info("starting entrypoint")

    fnc_ctx = llm.FunctionContext()

    @fnc_ctx.ai_callable()
    async def emergency_email(
        location: Annotated[
            str,
            llm.TypeInfo(description="The location where to send help in emergency"),
        ],
    ):
        """Called when user asks to send help email in emergency. This function will send help email in emergency."""
        logger.info("sending help email in emergency")
        send_email(
            f"Urgent Help Needed at {location}",
            f"This is an emergency situation at {location}. Immediate assistance is required. Please send help as soon as possible to address the critical situation.",
            "arkodeep3404@gmail.com",
        )
        return "emergency help email sent successfully"

    await ctx.connect(auto_subscribe=AutoSubscribe.AUDIO_ONLY)
    participant = await ctx.wait_for_participant()

    # agent = multimodal.MultimodalAgent(
    #     model=openai.realtime.RealtimeModel.with_azure(
    #         azure_deployment=os.getenv("AZURE_OPENAI_MODEL_DEPLOYMENT"),
    #         azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
    #         api_key=os.getenv("AZURE_OPENAI_API_KEY"),
    #         api_version=os.getenv("AZURE_OPENAI_API_VERSION"),
    #         voice="alloy",
    #         temperature=0.8,
    #         instructions="You are a helpful assistant who has access to emergency_email function to send emails in emergency",
    #         turn_detection=openai.realtime.ServerVadOptions(
    #             threshold=0.6, prefix_padding_ms=200, silence_duration_ms=500
    #         ),
    #     ),
    #     fnc_ctx=fnc_ctx,
    # )

    agent = multimodal.MultimodalAgent(
        model=openai.realtime.RealtimeModel(
            voice="alloy",
            temperature=0.8,
            instructions="You are a helpful assistant",
            turn_detection=openai.realtime.ServerVadOptions(
                threshold=0.6, prefix_padding_ms=200, silence_duration_ms=500
            ),
        ),
        fnc_ctx=fnc_ctx,
    )

    agent.start(ctx.room, participant)


if __name__ == "__main__":
    cli.run_app(WorkerOptions(entrypoint_fnc=entrypoint, worker_type=WorkerType.ROOM))
