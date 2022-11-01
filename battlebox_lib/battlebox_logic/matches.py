import enum
from dataclasses import dataclass
from pynamodb.models import Model
from pynamodb.indexes import AllProjection, KeysOnlyProjection, GlobalSecondaryIndex
from pynamodb.attributes import UnicodeAttribute, NumberAttribute, UTCDateTimeAttribute
from datetime import datetime, timezone
from typing import Optional, Dict, Any
import os


class Match(Model):
    """
    fields
    - knockouts
    - winner
    """
    class Meta:
        table_name = "BattleBoxMatch"
        region = "us-west-2"
        projection = AllProjection()
    match_id = UnicodeAttribute(hash_key=True)


def create_match():
    import uuid
    match_id = str(uuid.uuid4())
    model = Match(match_id=match_id)
    model.save()
    return match_id