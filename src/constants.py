from enum import Enum


class KnowledgePattern(str, Enum):
    IDEA_COMPASS = "idea_compass"
    KEYNOTE = "keynote"
    RECOMMENDATION = "recommendation"
    GITHUB_ISSUE = "github_issues"
    SUMMARY = "summary"


class Department(str, Enum):
    SERENDIPITY = "serendipity"
    TRADEMAN = "trademan"
    DHOOM_STUDIOS = "dhoom studios"
