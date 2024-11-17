from abc import ABCMeta, abstractmethod
from user.domain.user import User

# User 도메인의 저장소 인터페이스(I는 Interface를 의미)
# 이 인터페이스의 구현체는 인프라 계층에 존재
class IUserRepository(metaclass=ABCMeta):
    @abstractmethod
    def save(self, user: User):
        raise NotImplementedError
    
    @abstractmethod
    def find_by_email(self, email: str) -> User:
        """
        이메일로 유저를 검색한다.
        검색한 유저가 없을 경우 422 에러를 발생시킨다.
        """
        
        raise NotImplementedError
    
    @abstractmethod
    def find_by_id(self, id: str) -> User:
        raise NotImplementedError
    
    @abstractmethod
    def update(self, user: User):
        raise NotImplementedError
    
    @abstractmethod
    # Pagination
    def get_users(self, page: int, items_per_page: int) -> tuple[int, list[User]]:
        raise NotImplementedError
