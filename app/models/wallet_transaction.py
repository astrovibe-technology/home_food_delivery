class WalletTransaction(Base):
    __tablename__ = "wallet_transactions"

    id = Column(Integer, primary_key=True)
    wallet_id = Column(Integer, ForeignKey("wallets.id"))
    amount = Column(Integer, nullable=False)
    transaction_type = Column(String)  # credit / debit
    source = Column(String)  # order / referral / incentive / refund / admin
    reference_id = Column(Integer, nullable=True)
    description = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)