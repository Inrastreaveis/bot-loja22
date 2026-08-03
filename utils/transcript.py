import chat_exporter

async def gerar_transcript(channel):

    transcript = await chat_exporter.export(
        channel=channel
    )

    if transcript is None:
        return None

    with open(f"transcripts/{channel.id}.html", "w", encoding="utf-8") as arquivo:
        arquivo.write(transcript)

    return f"transcripts/{channel.id}.html"