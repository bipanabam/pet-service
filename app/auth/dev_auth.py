from fastapi import Header, HTTPException


async def dev_auth(
    x_dev_user: str | None = Header(default=None),
):
    """
    Development-only authentication.
    Inject user manually via header.
    """

    if not x_dev_user:
        raise HTTPException(
            status_code=401,
            detail="Missing X-Dev-User header",
        )

    # mimic Appwrite account response
    return {
        "$id": x_dev_user,
        "email": "dev@test.com",
    }