from dataclasses import dataclass

@dataclass
class DashboardConfig:
    url: str
    username: str
    password: str

TEST_CONFIG = DashboardConfig(
    url="https://10.0.64.196:8443/",
    username="admin",
    password="admin@123"
)

