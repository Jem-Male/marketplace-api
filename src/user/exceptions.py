from fastapi import HTTPException, status


class UserErrors:
    @staticmethod
    def user_not_found():
        return HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="user not found"
        )
    
    @staticmethod
    def invalid_password():
        return HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="password is not valid"
        )
    
    @staticmethod
    def email_is_exists():
        return HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="email already exits"
        )
    
    @staticmethod
    def phone_is_exists():
        return HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="phone number already exits"
        )
    
    @staticmethod
    def incorrect_email_phone():
        return HTTPException(
            status_code = status.HTTP_400_BAD_REQUEST,
            detail = "Incorrect email/phone or password"
        )

    @staticmethod
    def insufficient_privileges():
        return HTTPException(
            status_code = status.HTTP_403_FORBIDDEN,
            detail = "Insufficient privileges"
        )


class QueruErrors:
    @staticmethod
    def bad_query():
        return HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="bad query"
        )


class DBErrors:
    @staticmethod
    def fatal_delet():
        return HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="fatal delet"
        )
    
    @staticmethod
    def fatal_deactivaite():
        return HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="fatal deactivaite"
        )