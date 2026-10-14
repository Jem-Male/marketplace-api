from fastapi import HTTPException, status


class CategoryErrors:
    @staticmethod
    def category_not_found():
        return HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="category not found"
        )

    @staticmethod
    def category_is_exists():
        return HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="category already exists"
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