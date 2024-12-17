import re
from typing import List, Dict
from pydantic import BaseModel


class Scenario(BaseModel):
    id: int
    title: str
    content: str
    dependencies: List[int] = []

    def add_dependency(self, dependency_id: int):
        """
        Add a dependency to the scenario.
        """
        if dependency_id not in self.dependencies:
            self.dependencies.append(dependency_id)


class ScenarioDependencyResponse(BaseModel):
    scenario_id: int
    dependencies: List[int]


class AllDependenciesResponse(BaseModel):
    dependencies: Dict[int, List[int]]


class DependencyManager:
    def __init__(self):
        self.scenarios: Dict[int, Scenario] = {}
        self.next_id = 1

    def parse_scenarios(self, content: str) -> List[Scenario]:
        """
        Parse scenarios from the input content and assign unique IDs.
        """
        scenario_blocks = re.findall(r'Scenario: "(.+?)"\n(.*?)\n\n', content, re.DOTALL)
        parsed_scenarios = []

        for title, scenario_content in scenario_blocks:
            scenario = Scenario(self.next_id, title, scenario_content.strip())
            self.scenarios[self.next_id] = scenario
            self.next_id += 1
            parsed_scenarios.append(scenario)

        return parsed_scenarios

    def set_dependency(self, scenario_id: int, dependency_id: int):
        """
        Set a dependency between scenarios.
        """
        if scenario_id in self.scenarios and dependency_id in self.scenarios:
            self.scenarios[scenario_id].add_dependency(dependency_id)
        else:
            raise ValueError("Invalid scenario or dependency ID.")

    def get_scenario_by_id(self, scenario_id: int) -> Scenario:
        """
        Retrieve a scenario by its ID.
        """
        return self.scenarios.get(scenario_id, None)

    def generate_dependency_report(self) -> str:
        """
        Generate a report showing the dependencies for all scenarios.
        """
        report_lines = []
        for scenario in self.scenarios.values():
            dependencies = ", ".join(map(str, scenario.dependencies)) or "None"
            report_lines.append(f"Scenario ID: {scenario.id} - '{scenario.title}'\n"
                                 f"  Dependencies: {dependencies}\n")
        return "\n".join(report_lines)

    def update_content_with_ids(self, content: str) -> str:
        """
        Update the input content with unique scenario IDs.
        """
        updated_content = content
        for scenario_id, scenario in self.scenarios.items():
            updated_content = re.sub(
                rf'Scenario: "{re.escape(scenario.title)}"',
                f'Scenario: [{scenario_id}] "{scenario.title}"',
                updated_content
            )
        return updated_content


if __name__ == "__main__":
    # Example usage:
    input_content = """
    Scenario: "Assembling Lego"
    Given the position of the robot "Assembler" is "default" 
    When the robot "Assembler" moves to position "point2" 
    Then the position of the robot "Assembler" is "point2"

    Scenario: "Assembling Lego2"
    Given the position of the robot "Assembler2" is "default" 
    When the robot "Assembler2" moves to position "point2" 
    Then the position of the robot "Assembler2" is "point2"
    """

    manager = DependencyManager()

    # Parse and assign IDs
    manager.parse_scenarios(input_content)

    # Set dependencies
    manager.set_dependency(2, 1)  # Scenario 2 depends on Scenario 1

    # Generate report
    report = manager.generate_dependency_report()
    print(report)

    # Update content with scenario IDs
    updated_content = manager.update_content_with_ids(input_content)
    print("\nUpdated Content:\n")
    print(updated_content)
