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
Utilities for database related classes
"""

from typing import Any, Dict, List, Tuple

from spanner_graphs.cloud_database import SpannerDatabase, CloudSpannerDatabase
# from spanner_graphs.graph_server import GraphServer

class MockSpannerResult:

    def __init__(self, file_path: str):
        self.file_path = file_path
        self.fields: List[StructType] = []
        self._rows: List[List[Any]] = []
        self._load_data()

    def _load_data(self):
        with open(self.file_path, "r", encoding="utf-8") as csvfile:
            csv_reader = csv.reader(csvfile)
            headers = next(csv_reader)
            self.fields = [
                StructType.Field(name=header, type_=Type(code=TypeCode.JSON))
                for header in headers
            ]

            for row in csv_reader:
                parsed_row = []
                for value in row:
                    try:
                        js = bytes(value, "utf-8").decode("unicode_escape")
                        parsed_row.append(json.loads(js))
                    except json.JSONDecodeError:
                        pass
                self._rows.append(parsed_row)

    def __iter__(self):
        return iter(self._rows)


class MockSpannerDatabase:
    """Mock database class"""

    def __init__(self):
        dirname = os.path.dirname(__file__)
        self.graph_csv_path = os.path.join(
                            dirname, "graph_mock_data.csv")
        self.schema_json_path = os.path.join(
                            dirname, "graph_mock_schema.json")
        self.schema_json: dict = {}

    def execute_query(
        self,
        _: str,
        limit: int = 5
    ) -> Tuple[Dict[str, List[Any]], List[StructType.Field], List, str]:
        """Mock execution of query"""

        # Before the actual query we fetch the schema as well
        with open(self.schema_json_path, "r", encoding="utf-8") as js:
            self.schema_json = json.load(js)

        results = MockSpannerResult(self.graph_csv_path)
        fields: List[StructType.Field] = results.fields
        rows = list(results)
        data = {field.name: [] for field in fields}

        if len(fields) == 0:
            return data, fields, rows

        for i, row in enumerate(results):
            if limit is not None and i >= limit:
                break
            for field, value in zip(fields, row):
                data[field.name].append(value)

        return data, fields, rows, self.schema_json, None

database_instances: dict[str, SpannerDatabase | MockSpannerDatabase] = {}

def get_database_instance(project: str, instance: str, database: str) -> SpannerDatabase:
    if mock:
        return MockSpannerDatabase()
    #if not GraphServer.is_cloud_mode:
    #    raise NotImplementedError(
    #        "Database operations are not supported when not in cloud mode. "
    #        "Initialize GraphServer in cloud mode to proceed."
    #    )

    key = f"{project}_{instance}_{database}"
    db = database_instances.get(key) # Simpler get

    if not db:
        db = CloudSpannerDatabase(project, instance, database)
        database_instances[key] = db

    return db

