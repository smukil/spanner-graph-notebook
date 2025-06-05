# Copyright 2024 Google LLC

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#     https://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
This module contains implementation for talking to spanner database
via snapshot queries.
"""

from __future__ import annotations
from typing import Any, Dict, List, Tuple
import json
import os
import csv
from abc import ABC, abstractmethod

import spanner_graphs.cloud_database

class SpannerDatabase(ABC): # Changed to ABC
    """The spanner class holding the database connection"""

    @abstractmethod
    def _extract_graph_name(self, query: str) -> str:
        pass

    @abstractmethod
    def _get_schema_for_graph(self, graph_query: str):
        pass

    @abstractmethod
    def execute_query(
        self,
        query: str,
        limit: int = None,
        is_test_query: bool = False,
    ) -> Tuple[Dict[str, List[Any]], List[StructType.Field], List, Any | None, Exception | None]:
        pass

class MockSpannerDatabase(ABC): # Changed to ABC
    """Mock database class - Abstract Base Class"""

    # Removed __init__ method and path attributes

    @abstractmethod # Added
    def execute_query(
        self,
        query: str,
        limit: int = 5
    ) -> Tuple[Dict[str, List[Any]], List[StructType.Field], List, Optional[Dict], Optional[Exception]]: # Adjusted return type for consistency
        pass
