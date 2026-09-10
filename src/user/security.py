from pwdlib import PasswordHash
import asyncio


password_hash = PasswordHash.recommended()


async def generate_password_hash(pwd: str) -> str:
    loop = asyncio.get_running_loop()
    hashed_password = await loop.run_in_executor(None, password_hash.hash, pwd) 
    return hashed_password


async def check_password_hash(plain_pwd: str, hash_pwd: str) -> bool:
    loop = asyncio.get_running_loop()
    res = await loop.run_in_executor(None, password_hash.verify, plain_pwd, hash_pwd)
    return res