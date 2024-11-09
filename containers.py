from dependency_injector import containers, providers
from user.infra.repository.user_repo import UserRepository
from user.application.user_service import UserService

class Container(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(
        packages=["user"], # 의존성을 사용할 모듈을 선언
    )

    user_repo = providers.Factory(UserRepository) # 의존성을 제공할 모듈을 팩토리에 등록
    # UserService 객체를 생성할 팩토리를 제공
    # 이때, UserService 생성자로 전달될 user_repo 객체 역시 컨테이너에 있는 팩토리로 선언
    user_service = providers.Factory(UserService, user_repo=user_repo)