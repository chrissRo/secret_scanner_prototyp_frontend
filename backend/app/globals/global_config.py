from enum import Enum


class AvailableScanner(Enum):
    GITLEAKS = 0
    TRUFFLEHOG = 1


class InputType(Enum):
    FileSystem = 0
    API = 1
