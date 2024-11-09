from ulid import ULID
from datetime import datetime
from user.domain.user import User
from user.domain.repository.user_repo import IUserRepository
from fastapi import HTTPException
from utils.crypto import Crypto
from dependency_injector.wiring import inject

class UserService:
    @inject # 의존성 객체를 사용하는 함수에 주입받은 객체를 사용한다고 선언
    def __init__(
        self,
        # Depends 함수의 인수로 컨테이너에 등록된 UserRepository의 팩토리를 제공, UserService는 UserRepository를 직접 의존하지 않게 됨
        # user_repo: IUserRepository = Depends(Provide[Container.user_repo]) -> 인터페이스 계층 외 FastAPI와 느슨하게 구현하기 위해서 아래 코드로 변경
        user_repo: IUserRepository # 컨테이너에서 직접 user_repo 팩토리를 선언해두었기 때문에 타입 선언만으로도 UserService가 생성될 때 팩토리를 수행한 객체가 주입
    ):
        self.user_repo = user_repo
        self.ulid = ULID()
        self.crypto = Crypto()
        
    def create_user(self, name: str, email: str, password: str):
        _user = None # 데이터베이스에서 찾은 유저 변수
        
        try:
            _user = self.user_repo.find_by_email(email)
        except HTTPException as e:
            if e.status_code != 422:
                raise e
        if _user:
            raise HTTPException(status_code=422, detail="Email already exists") # 이미 가입한 유저일 경우 422 에러 발생

        now = datetime.now()
        user: User = User(
            id=self.ulid.generate(),
            name=name,
            email=email,
            password=self.crypto.encrypt(password),
            created_at=now,
            updated_at=now,
        )
        self.user_repo.save(user) # 생성된 유저 객체를 저장소로 전달해 저장
        
        return user