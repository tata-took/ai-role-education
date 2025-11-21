from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Dict, List, Optional

MAX_CONCURRENT_JUDGMENTS = 5
REEDUCATION_TIMEOUT_HOURS = 48


@dataclass
class RoleStatus:
    role_id: str
    credit: int
    state: str  # "active" | "injured" | "terminated"
    injured_at: Optional[datetime] = None
    last_action_at: Optional[datetime] = None
    reeducation_submitted_at: Optional[datetime] = None


@dataclass
class ReeducationCase:
    role_id: str
    submitted_at: datetime
    status: str  # "queued" | "in_review" | "approved" | "rejected" | "timeout"
    notes: str = ""


class JudgeSystem:
    def __init__(self):
        self.waiting_room: Dict[str, RoleStatus] = {}
        self.active_cases: Dict[str, ReeducationCase] = {}
        self.history: List[ReeducationCase] = []

    def mark_injured(self, role: RoleStatus, now: datetime) -> None:
        role.state = "injured"
        role.injured_at = now
        self.waiting_room[role.role_id] = role

    def submit_reeducation_plan(self, role_id: str, now: datetime) -> None:
        role = self.waiting_room.get(role_id)
        if not role:
            return

        role.reeducation_submitted_at = now

        if self._current_active_count() >= MAX_CONCURRENT_JUDGMENTS:
            case = ReeducationCase(
                role_id=role_id,
                submitted_at=now,
                status="queued",
            )
            self.active_cases[role_id] = case
        else:
            case = ReeducationCase(
                role_id=role_id,
                submitted_at=now,
                status="in_review",
            )
            self.active_cases[role_id] = case

    def _current_active_count(self) -> int:
        return sum(
            1
            for case in self.active_cases.values()
            if case.status in ("queued", "in_review")
        )

    def tick(self, now: datetime) -> None:
        available_slots = MAX_CONCURRENT_JUDGMENTS - sum(
            1 for case in self.active_cases.values() if case.status == "in_review"
        )
        if available_slots > 0:
            for case in self.active_cases.values():
                if available_slots <= 0:
                    break
                if case.status == "queued":
                    case.status = "in_review"
                    available_slots -= 1

        timeout_delta = timedelta(hours=REEDUCATION_TIMEOUT_HOURS)
        to_terminate: List[str] = []

        for role_id, role in list(self.waiting_room.items()):
            base_time = role.reeducation_submitted_at or role.injured_at or now
            if now - base_time >= timeout_delta:
                to_terminate.append(role_id)

        for role_id in to_terminate:
            self._terminate_role(role_id, now)

    def _terminate_role(self, role_id: str, now: datetime) -> None:
        case = self.active_cases.get(role_id)
        if case:
            case.status = "timeout"
            self.history.append(case)

        role = self.waiting_room.pop(role_id, None)
        if role:
            role.state = "terminated"
            role.last_action_at = now
