from uuid import UUID

from vellum_ee.workflows.display.nodes import BaseTemplatingNodeDisplay
from vellum_ee.workflows.display.nodes.types import PortDisplayOverrides
from vellum_ee.workflows.display.vellum import NodeDisplayData, NodeDisplayPosition

from ...nodes.templating_node_15 import TemplatingNode15


class TemplatingNode15Display(BaseTemplatingNodeDisplay[TemplatingNode15]):
    label = "Templating Node 15"
    node_id = UUID("ed96d879-cb62-40c8-9f8c-b14016740a2f")
    output_id = UUID("845ae624-f957-404e-a9e5-5a8ece09a1c9")
    target_handle_id = UUID("ed213a6c-2573-431c-8736-b8f062869db7")
    template_input_id = UUID("9fa804b1-1b86-4cc9-af3c-1c1a6718dc02")
    node_input_ids_by_name = {
        "API_KEY": UUID("8b10a7d8-9d35-4808-ad93-4e1774ca80dc"),
        "template": UUID("9fa804b1-1b86-4cc9-af3c-1c1a6718dc02"),
        "airline_name": UUID("4540ee13-ed34-4c88-86ba-6bc4f908a49b"),
        "arrival_airport": UUID("b2aef5a8-526a-4b48-8f35-6984077c48df"),
    }
    port_displays = {
        TemplatingNode15.Ports.default: PortDisplayOverrides(id=UUID("8eaafb2e-a666-4dc9-96c3-52839df75632"))
    }
    display_data = NodeDisplayData(position=NodeDisplayPosition(x=3304, y=1043), width=461, height=327)
