from datetime import datetime, timezone

from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.redis import RedisClient, OtpValidator
from app.repository import UserRepository

from app.models import User
from app.schemas import LoginRequest, RegisterRequest, RegisterResponse, EmailVerificationRequest, EmailVerificationResponse

from .utils import PasswordUtility, EmailVerificationUtility



class AuthService:

    def __init__(self, db_session: AsyncSession, client: RedisClient) -> None:

        self.db_session    = db_session

        self.redis_client = client


    async def Login(self, req: LoginRequest) -> None:

        pass 


    async def Register(self, req: RegisterRequest) -> RegisterResponse:

        user_repo = UserRepository(self.db_session)

        email = req.email.strip()

        try:

            user = await user_repo.get_by_email(email)

            if user is not None and user.is_active:
                return RegisterResponse(
                    success=False,
                    message="Email ID already exists",
                    data=None,
                )
            
            if user is not None:
                otp = EmailVerificationUtility.generate_otp()

                otp_validator = OtpValidator(self.redis_client)

                await otp_validator.store_otp(email, otp, window=600)

                EmailVerificationUtility.send_otp(email, otp, 10)

                return RegisterResponse(
                    success=True,
                    message="Validate Your Email Address",
                    data=None,
                )

            user = await user_repo.create(
                User(
                    email=email,
                    password_hash=PasswordUtility.hash(req.password),
                    is_active=False
                )
            )

            await user_repo.commit()

        except IntegrityError:

            await self.db_session.rollback()

            return RegisterResponse(
                success=False,
                message="Email ID already exists",
                data=None,
            )

        otp = EmailVerificationUtility.generate_otp()

        otp_validator = OtpValidator(self.redis_client)

        await otp_validator.store_otp(email, otp, window=600)

        EmailVerificationUtility.send_otp(email, otp, 10)

        return RegisterResponse(
            success=True,
            message="Validate Your Email Address",
            data=None,
        )


    async def EmailVerification(self, req: EmailVerificationRequest) -> EmailVerificationResponse:

        email = req.email.strip().lower()

        otp_validator = OtpValidator(self.redis_client)

        is_valid = await otp_validator.validate_otp(email, req.otp)

        if not is_valid:
            return EmailVerificationResponse(
                success=False,
                message="Invalid or expired OTP",
            )

        user_repo = UserRepository(self.db_session)

        try:

            user = await user_repo.get_by_email(email)

            if user is None:
                return EmailVerificationResponse(
                    success=False,
                    message="User not found"
                )

            if user.is_active:
                return EmailVerificationResponse(
                    success=True,
                    message="Email already verified"
                )

            user.updated_at = datetime.now(timezone.utc)

            user.is_active = True

            await user_repo.commit()

            return EmailVerificationResponse(
                success=True,
                message="Email verified successfully"
            )

        except Exception:
            await user_repo.rollback()

            return EmailVerificationResponse(
                success=False,
                message="Something Went Wrong"
            )