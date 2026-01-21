class UserSettings(Base):
    __tablename__ = "user_settings"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    notifications_enabled = Column(Boolean, default=True)
    dark_mode = Column(Boolean, default=False)