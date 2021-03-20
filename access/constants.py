ACCESS_REQUEST_VALID_DAYS = 5  # In number of days

STATUS_PENDING = "pending"
STATUS_APPROVED = "approved"
STATUS_DECLINED = "declined"
STATUS_IN_USE = "in_use"  # solely for acquiring lock.
STATUS_USED = "used"
STATUS_EXPIRED = "expired"

ACCESS_REQUEST_STATUS_CHOICES = (
    (STATUS_PENDING, "Pending"),
    (STATUS_APPROVED, "Approved"),
    (STATUS_DECLINED, "Declined"),
    (STATUS_IN_USE, "In Use"),
    (STATUS_USED, "Used"),
    (STATUS_EXPIRED, "Expired"),
)
