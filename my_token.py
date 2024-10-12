from livekit import api
import os
from datetime import timedelta

token = (
    api.AccessToken(os.getenv("LIVEKIT_API_KEY"), os.getenv("LIVEKIT_API_SECRET"))
    .with_identity("identity")
    .with_name("name")
    .with_grants(
        api.VideoGrants(
            room_join=True,
            room="my-room",
        )
    )
    .with_ttl(timedelta(days=30))
    .to_jwt()
)

print("TOKEN", token)

# eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZGVudGl0eSI6IiIsIm5hbWUiOiJuYW1lIiwidmlkZW8iOnsicm9vbUNyZWF0ZSI6ZmFsc2UsInJvb21MaXN0IjpmYWxzZSwicm9vbVJlY29yZCI6ZmFsc2UsInJvb21BZG1pbiI6ZmFsc2UsInJvb21Kb2luIjp0cnVlLCJyb29tIjoibXktcm9vbSIsImNhblB1Ymxpc2giOnRydWUsImNhblN1YnNjcmliZSI6dHJ1ZSwiY2FuUHVibGlzaERhdGEiOnRydWUsImNhblB1Ymxpc2hTb3VyY2VzIjpbXSwiY2FuVXBkYXRlT3duTWV0YWRhdGEiOmZhbHNlLCJpbmdyZXNzQWRtaW4iOmZhbHNlLCJoaWRkZW4iOmZhbHNlLCJyZWNvcmRlciI6ZmFsc2UsImFnZW50IjpmYWxzZX0sInNpcCI6eyJhZG1pbiI6ZmFsc2UsImNhbGwiOmZhbHNlfSwiYXR0cmlidXRlcyI6e30sIm1ldGFkYXRhIjoiIiwic2hhMjU2IjoiIiwia2luZCI6IiIsInN1YiI6ImlkZW50aXR5IiwiaXNzIjoiQVBJaGlrU3ZEQ000N1FxIiwibmJmIjoxNzI4NTM3MDkxLCJleHAiOjE3MzExMjkwOTF9.GMDrTNuiZBjifiu4y6e-XRHqadGWIHzhaIN1NlYH96Y
