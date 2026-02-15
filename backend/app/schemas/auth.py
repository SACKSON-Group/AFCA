from pydantic import BaseModel, Field, model_validator


class OtpRequestIn(BaseModel):
    phone: str | None = Field(default=None, min_length=8, max_length=16)
    email: str | None = Field(default=None, max_length=255)

    @model_validator(mode="after")
    def has_phone_or_email(self) -> "OtpRequestIn":
        if not self.phone and not self.email:
            raise ValueError("either phone or email must be provided")
        return self


class OtpVerifyIn(BaseModel):
    phone: str | None = Field(default=None, min_length=8, max_length=16)
    email: str | None = Field(default=None, max_length=255)
    code: str = Field(min_length=4, max_length=8)

    @model_validator(mode="after")
    def has_phone_or_email(self) -> "OtpVerifyIn":
        if not self.phone and not self.email:
            raise ValueError("either phone or email must be provided")
        return self


class TokenOut(BaseModel):
    access_token: str
    token_type: str = "bearer"
