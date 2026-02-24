# backend/app/core/constants.py


# =============================
# AUTH CONSTANTS
# =============================

ACCESS_TOKEN_EXPIRE_MINUTES = 60
REFRESH_TOKEN_EXPIRE_DAYS = 7

ALGORITHM = "HS256"


# =============================
# USER ROLES
# =============================

ROLE_ADMIN = "admin"
ROLE_ORGANIZER = "organizer"
ROLE_CUSTOMER = "customer"


# =============================
# EVENT STATUS
# =============================

EVENT_STATUS_UPCOMING = "upcoming"
EVENT_STATUS_ONGOING = "ongoing"
EVENT_STATUS_COMPLETED = "completed"
EVENT_STATUS_CANCELLED = "cancelled"


# =============================
# SEAT STATUS
# =============================

SEAT_AVAILABLE = "available"
SEAT_LOCKED = "locked"
SEAT_BOOKED = "booked"

SEAT_LOCK_DURATION_MINUTES = 5


# =============================
# BOOKING STATUS
# =============================

BOOKING_PENDING = "pending"
BOOKING_CONFIRMED = "confirmed"
BOOKING_CANCELLED = "cancelled"
BOOKING_FAILED = "failed"


# =============================
# PAYMENT STATUS
# =============================

PAYMENT_UNPAID = "unpaid"
PAYMENT_PAID = "paid"
PAYMENT_FAILED = "failed"
PAYMENT_REFUNDED = "refunded"


# =============================
# TICKET STATUS
# =============================

TICKET_ACTIVE = "active"
TICKET_USED = "used"
TICKET_CANCELLED = "cancelled"
TICKET_EXPIRED = "expired"


# =============================
# REFUND STATUS
# =============================

REFUND_REQUESTED = "requested"
REFUND_APPROVED = "approved"
REFUND_REJECTED = "rejected"
REFUND_PROCESSED = "processed"
REFUND_FAILED = "failed"


# =============================
# SUPPORT STATUS
# =============================

SUPPORT_OPEN = "open"
SUPPORT_IN_PROGRESS = "in_progress"
SUPPORT_RESOLVED = "resolved"
SUPPORT_CLOSED = "closed"
SUPPORT_REJECTED = "rejected"


# =============================
# PAGINATION DEFAULTS
# =============================

DEFAULT_PAGE = 1
DEFAULT_PAGE_SIZE = 10
MAX_PAGE_SIZE = 100


# =============================
# COMMON RESPONSE MESSAGES
# =============================

MSG_UNAUTHORIZED = "Unauthorized access"
MSG_FORBIDDEN = "Permission denied"
MSG_NOT_FOUND = "Resource not found"
MSG_INTERNAL_ERROR = "Internal server error"