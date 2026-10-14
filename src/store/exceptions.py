from fastapi import HTTPException, status

class StoreErrors:
    @staticmethod
    def not_found():
        return HTTPException(
            status_code = status.HTTP_400_BAD_REQUEST,
            detail = "store not found"
        )
    
    @staticmethod
    def already_exists():
        return HTTPException(
            status_code = status.HTTP_400_BAD_REQUEST,
            detail = "store alreadyexists"
        )
    
    @staticmethod
    def user_insufficient_privileges():
        return HTTPException(
            status_code = status.HTTP_403_FORBIDDEN,
            detail = "No editing rights"
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