from src.user.model import UserRole


class Role():
    @staticmethod
    async def check_admin(user: UserRole) -> bool:
        if user is UserRole.ADMIN:
            pass
        
