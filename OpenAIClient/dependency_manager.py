from typing import List, Dict
from pydantic import BaseModel

# Pydantic model for the POST request to add dependencies
class ScenarioDependency(BaseModel):
    scenario: str
    depends_on: str

# Pydantic model for the GET request to return scenario dependencies
class ScenarioResponse(BaseModel):
    dependencies: List[str]

class DependencyManager:
    def __init__(self):
        # A dictionary to store the dependencies between scenarios
        self.dependencies: Dict[str, set] = {}

    def add_dependency(self, scenario: str, depends_on: str):
        """Adds a dependency, meaning 'scenario' depends on 'depends_on'."""
        if scenario not in self.dependencies:
            self.dependencies[scenario] = set()
        self.dependencies[scenario].add(depends_on)

    def get_dependencies(self, scenario: str) -> List[str]:
        """Returns a list of scenarios that the given scenario depends on."""
        return list(self.dependencies.get(scenario, []))

    def get_dependents(self, scenario: str) -> List[str]:
        """Returns a list of scenarios that depend on the given scenario."""
        dependents = []
        for dependent, deps in self.dependencies.items():
            if scenario in deps:
                dependents.append(dependent)
        return dependents

    def remove_dependency(self, scenario: str, depends_on: str):
        """Removes a dependency, meaning 'scenario' no longer depends on 'depends_on'."""
        if scenario in self.dependencies and depends_on in self.dependencies[scenario]:
            self.dependencies[scenario].remove(depends_on)
            if not self.dependencies[scenario]:
                del self.dependencies[scenario]

    def list_all_dependencies(self) -> Dict[str, List[str]]:
        """Returns a dictionary of all the scenarios and their dependencies."""
        return self.dependencies
