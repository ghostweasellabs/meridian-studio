# Requirements Document

## Introduction

**Meridian Studio** will provide a web-based visual interface for building and editing computational graphs using Meridian Runtime. Users will be able to drag and drop nodes from the extensive built-in node library (including DataProducer, MapTransformer, DataConsumer, Router, EventAggregator, AsyncWorker, and many others), connect them with typed edges, configure node properties, and visualize the flow of data through their graph in real-time. Meridian Studio will be built as a modern web application using Vite + React with shadcn/ui components, running via Deno 2 (npm interop) by default with Node optional. The application communicates with a FastAPI backend that interfaces with the Meridian Runtime engine (installed from PyPI, subject to availability verification) for graph execution and validation. All user data, graphs, and execution history will be stored in a self-hosted Supabase instance providing authentication, real-time features, and PostgreSQL database capabilities.

## Requirements

### Requirement 1

**User Story:** As a developer, I want to visually create computational graphs by dragging and dropping nodes, so that I can build complex workflows without writing code.

#### Acceptance Criteria

1. WHEN a user opens the visual graph builder THEN the system SHALL display a canvas area and a node palette
2. WHEN a user drags a node from the palette to the canvas THEN the system SHALL create a new node instance on the canvas
3. WHEN a user clicks on a node type in the palette THEN the system SHALL show available configuration options for that node type
4. WHEN a user drops a node on the canvas THEN the system SHALL position the node at the drop location and make it selectable

### Requirement 2

**User Story:** As a developer, I want to connect nodes with edges to define data flow, so that I can specify how data moves through my computational graph.

#### Acceptance Criteria

1. WHEN a user clicks and drags from a node's output port THEN the system SHALL display a connection line following the cursor
2. WHEN a user drops the connection line on a compatible input port THEN the system SHALL create an edge between the nodes
3. WHEN a user attempts to connect incompatible ports THEN the system SHALL prevent the connection and show an error message
4. WHEN a user right-clicks on an edge THEN the system SHALL provide options to delete or modify the connection

### Requirement 3

**User Story:** As a developer, I want to configure node properties through a visual interface, so that I can customize node behavior without editing code.

#### Acceptance Criteria

1. WHEN a user selects a node THEN the system SHALL display a properties panel with configurable parameters
2. WHEN a user modifies a property value THEN the system SHALL validate the input and update the node configuration
3. WHEN a user enters invalid property values THEN the system SHALL show validation errors and prevent saving
4. WHEN a user saves property changes THEN the system SHALL persist the configuration and update the visual representation

### Requirement 4

**User Story:** As a developer, I want to save and load graph definitions, so that I can persist my work and share graphs with others.

#### Acceptance Criteria

1. WHEN a user clicks save THEN the system SHALL serialize the current graph to a JSON format
2. WHEN a user loads a saved graph THEN the system SHALL recreate the visual representation with all nodes and connections
3. WHEN a user exports a graph THEN the system SHALL generate a downloadable file containing the graph definition
4. WHEN a user imports a graph file THEN the system SHALL validate the format and load the graph onto the canvas

### Requirement 5

**User Story:** As a developer, I want to execute graphs from the visual interface, so that I can test and run my workflows directly in the browser.

#### Acceptance Criteria

1. WHEN a user clicks the execute button THEN the system SHALL validate the graph structure and run the computation
2. WHEN a graph is executing THEN the system SHALL show visual indicators of data flow and node processing status
3. WHEN execution completes THEN the system SHALL display results and any output data from the graph
4. WHEN execution fails THEN the system SHALL highlight error locations and show detailed error messages

### Requirement 6

**User Story:** As a developer, I want to see real-time feedback during graph construction, so that I can identify issues early and understand graph behavior.

#### Acceptance Criteria

1. WHEN a user modifies the graph structure THEN the system SHALL perform real-time validation and show warnings
2. WHEN there are circular dependencies THEN the system SHALL highlight the problematic connections
3. WHEN nodes have missing required inputs THEN the system SHALL visually indicate incomplete connections
4. WHEN the graph is valid THEN the system SHALL show a green status indicator

### Requirement 7

**User Story:** As a developer, I want to organize complex graphs with grouping and layout features, so that I can manage large workflows effectively.

#### Acceptance Criteria

1. WHEN a user selects multiple nodes THEN the system SHALL allow grouping them into a collapsible container
2. WHEN a user applies auto-layout THEN the system SHALL arrange nodes in a logical flow pattern
3. WHEN a user zooms and pans the canvas THEN the system SHALL maintain smooth navigation performance
4. WHEN a user searches for nodes THEN the system SHALL highlight matching nodes and allow quick navigation

### Requirement 8

**User Story:** As a developer, I want to integrate the visual graph builder with existing Meridian node types, so that I can leverage all available functionality from the comprehensive built-in node library.

#### Acceptance Criteria

1. WHEN the system loads THEN it SHALL automatically discover and display all available Meridian built-in node types including DataProducer, MapTransformer, DataConsumer, Router, EventAggregator, AsyncWorker, ThrottleNode, CircuitBreakerNode, EncryptionNode, and others
2. WHEN a user creates a node THEN the system SHALL use the same configuration schema as the programmatic API with proper type validation
3. WHEN a graph is executed THEN the system SHALL use the existing Meridian Scheduler and runtime for computation with proper observability
4. WHEN a user configures node properties THEN the system SHALL validate inputs according to PortSpec definitions and provide appropriate error messages

### Requirement 9

**User Story:** As a developer, I want to create an account and securely store my graphs, so that I can persist my work and access it from anywhere.

#### Acceptance Criteria

1. WHEN a user visits the application THEN they SHALL be able to create an account using email/password or social login (Google, GitHub)
2. WHEN a user logs in THEN the system SHALL authenticate them using Supabase and provide secure access to their graphs
3. WHEN a user creates or modifies a graph THEN it SHALL be automatically saved to their personal Supabase database
4. WHEN a user logs in from a different device THEN they SHALL see all their previously created graphs

### Requirement 10

**User Story:** As a developer, I want to share my graphs with others, so that I can collaborate and showcase my work.

#### Acceptance Criteria

1. WHEN a user owns a graph THEN they SHALL be able to share it with specific users or make it publicly accessible
2. WHEN a user shares a graph THEN they SHALL be able to set permissions (read-only, edit, execute)
3. WHEN a user receives a shared graph THEN they SHALL be able to view and interact with it according to their permissions
4. WHEN a user makes a graph public THEN it SHALL be discoverable by other users in a public gallery

### Requirement 11

**User Story:** As a developer, I want to track the execution history of my graphs, so that I can monitor performance and debug issues.

#### Acceptance Criteria

1. WHEN a user executes a graph THEN the system SHALL record the execution details, results, and performance metrics
2. WHEN a user views a graph THEN they SHALL see a history of previous executions with timestamps and status
3. WHEN an execution fails THEN the system SHALL store error details and stack traces for debugging
4. WHEN a user reviews execution history THEN they SHALL be able to compare results across different runs

### Requirement 12

**User Story:** As a developer, I want the application to be easily deployable and maintainable, so that it can be run in different environments.

#### Acceptance Criteria

1. WHEN deploying the application THEN it SHALL run in Docker containers for consistent environments
2. WHEN setting up locally THEN developers SHALL be able to start the entire stack with docker-compose up
3. WHEN the application runs THEN it SHALL include all necessary services: frontend, backend, database, authentication, and caching
4. WHEN scaling the application THEN individual services SHALL be independently scalable through container orchestration

### Requirement 13

**User Story:** As a developer, I want to visualize real-time communication between nodes during graph execution, so that I can understand data flow and debug issues effectively.

#### Acceptance Criteria

1. WHEN a graph is executing THEN the system SHALL display animated visual indicators showing messages flowing through edges in real-time
2. WHEN a message passes through an edge THEN the system SHALL show the message payload, type (DATA/CONTROL/ERROR), and timestamp
3. WHEN a user clicks on an active edge THEN the system SHALL display a detailed message trace showing all recent communications
4. WHEN multiple messages flow simultaneously THEN the system SHALL visually distinguish between different message types and show queue depth

### Requirement 14

**User Story:** As a developer, I want to trace the complete path of message communication through my graph, so that I can understand complex data transformations and identify bottlenecks.

#### Acceptance Criteria

1. WHEN a user selects a message in the trace viewer THEN the system SHALL highlight the complete path the message took through the graph
2. WHEN a message triggers downstream processing THEN the system SHALL show the causal relationship between input and output messages
3. WHEN a user inspects a node during execution THEN the system SHALL show all incoming and outgoing messages with their transformation details
4. WHEN execution completes THEN the system SHALL provide a complete message flow diagram showing all communication paths taken

### Requirement 15

**User Story:** As a developer, I want to monitor and analyze communication patterns between nodes, so that I can optimize graph performance and identify issues.

#### Acceptance Criteria

1. WHEN a graph executes THEN the system SHALL collect metrics on message throughput, latency, and queue depths for each edge
2. WHEN a user views communication analytics THEN they SHALL see real-time charts of message rates, processing times, and backpressure indicators
3. WHEN bottlenecks occur THEN the system SHALL visually highlight slow or blocked edges with performance warnings
4. WHEN a user reviews execution history THEN they SHALL be able to compare communication patterns across different runs

### Requirement 16

**User Story:** As a developer, I want the visual interface to be modern and responsive, so that I can have an excellent user experience while building graphs.

#### Acceptance Criteria

1. WHEN a user accesses the application THEN it SHALL load as a modern single-page application built with Vite and React (powered by Deno 2 runtime for tooling)
2. WHEN a user interacts with UI components THEN they SHALL use shadcn/ui components for consistent design and accessibility
3. WHEN a user works on different screen sizes THEN the interface SHALL be responsive and usable on desktop and tablet devices
4. WHEN a user performs actions THEN the interface SHALL provide immediate visual feedback and smooth animations

## Development Workflow (Branches)

- Graph building UI (Req 1–3, 6–8, 13–16): `feat/graph-canvas`, `feat/node-palette`, `feat/properties-panel`, `feat/edge-connections`
- Persistence & sharing (Req 4, 9–11): `feat/graph-persistence`, `feat/sharing-collab`, `feat/execution-history`
- Execution & realtime (Req 5, 13–15): `feat/execution-api-ws`, `feat/message-tracing`, `feat/communication-analytics`
- Infrastructure & deployment (Req 12): `feat/infra-scaffold`, `feat/docker-compose`, `release/<version>`
- Hot fixes and patches: `hotfix/<ticket>` merged to `main` and `develop`