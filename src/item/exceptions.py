from fastapi import HTTPException, status


class ItemErrors():
    @staticmethod
    def item_not_found():
        return HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="item not found"
        )

    @staticmethod
    def item_already_registered():
        return HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="item already registered"
        )
    
    @staticmethod
    def user_insufficient_privileges():
        return HTTPException(
            status_code = status.HTTP_403_FORBIDDEN,
            detail = "No editing rights"
        )


class StoreErrors:
    @staticmethod
    def not_found():
        return HTTPException(
            status_code = status.HTTP_400_BAD_REQUEST,
            detail = "store not found"
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