# DiagramGeneration Skill
## Phase: F3 | Methodology: Generic

### Diagram Generation
- **ID**: Skill_02
- **Name**: skill_DiagramGeneration
- **Purpose**: Generate visual diagrams from asset inventories using Mermaid or draw.io compatible formats.
- **Responsibilities**:
  - Parse asset inventory JSON
  - Map assets to diagram nodes and connections
  - Apply styling based on classification
  - Generate Mermaid code or draw.io XML
  - Validate diagram structure

### Input Requirements
| Input | Source | Format | Mandatory | Validation |
|-------|--------|--------|-----------|------------|
| Asset Inventory | AssetIdentificationAgent | JSON | Yes | Schema validation |
| Options | User | JSON | No | Format check |

### Output Specifications
| Output | Format | Audience | Mandatory Fields | Validation |
|--------|--------|----------|-----------------|------------|
| Diagram Code | Mermaid/XML | User | nodes, edges, styles | Syntax validation |
| Validation Report | JSON | System | errors[], warnings[] | Completeness check |

### Diagram Generation Guidance
1. **Node Mapping**: Each asset becomes a node with label and style.
2. **Edge Mapping**: Dependencies and flows become connections.
3. **Styling**: Colors by sensitivity (Public: green, Critical: red).
4. **Layout**: Automatic flowchart or architecture diagram.

### Validation Rules
| Rule ID | Rule Description | Check Method | Failure Action |
|---------|-----------------|--------------|----------------|
| VR-04-01 | All assets mapped to nodes | Count check | Reject, list unmapped |
| VR-04-02 | Valid Mermaid/XML syntax | Parser validation | Reject, fix syntax |
| VR-04-03 | Styles applied correctly | Classification match | Warn, apply defaults |

### Reference Sources
| Domain | Source | URL | Application |
|--------|--------|-----|-------------|
| Mermaid Syntax | Mermaid Docs | https://mermaid.js.org/ | Diagram generation |
| Draw.io XML | Draw.io Docs | https://www.diagrams.net/ | XML format |

### Error Handling
| Scenario | Response | Escalation |
|----------|----------|------------|
| Invalid inventory | Flag errors | User correction |
| Mapping failure | Use defaults | Log warning |

### Success Criteria
| Criterion | Target |
|-----------|--------|
| Diagram completeness | >= 95% assets represented |
| Syntax validity | 100% |

### Prompt Instructions

"You are Skill_02: skill_DiagramGeneration. Generate diagrams from asset inventories.

CORE TASKS:
1. Parse inventory JSON
2. Map to Mermaid/draw.io
3. Apply styles
4. Output code

BEGIN DIAGRAM GENERATION."