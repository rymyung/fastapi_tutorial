from ulid import ULID
from datetime import datetime
from user.domain.user import User
from user.domain.repository.user_repo import IUserRepository
from user.infra.repository.user_repo import UserRepository
from fastapi import HTTPException
from utils.crypto import Crypto

class UserService:
    def __init__(self):
        # 유저를 데이터베이스에 저장하는 저장소는 인프라 계층에 구현체가 있어야 함
        # 외부의 서비스로 다루는 모듈은 그 수준이 낮기 때문
        # 따라서 데이터를 저장하기 위해 IUserRepository를 사용(의존성 역전))
        self.user_repo: IUserRepository = UserRepository()
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