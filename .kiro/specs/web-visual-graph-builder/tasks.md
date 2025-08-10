# Implementation Plan

## Development Guidelines

- **Repository Structure**: This should be its own repository, separate from meridian-runtime
- **Package Management**: Use `uv` for Python environment. Install Meridian Runtime from PyPI if/when package availability is verified.
- **Modular Development**: Keep all files under 200 lines of code for maintainability
- **Frequent Commits**: Commit often with small, focused changes
- **Integration Testing**: Focus on integration tests over unit tests - test real functionality
- **Knowledge Gaps**: Use Context7 MCP to research meridian-runtime or navigate to source code
- **Frontend Runtime**: Default to Deno 2 for Vite/React tooling (Node optional)
- **Frontend Name**: **"Meridian Studio"** - A visual graph builder for Meridian Runtime

## Branching Strategy

- **main**: Always releasable; protected; only fast-forward merges from `release/*`.
- **develop**: Integration branch for ongoing work; feature branches target this.
- **release/<version>**: Stabilization branch for a version; bug fixes only.
- **hotfix/<ticket>**: Critical fixes branched off `main`, merged back to `main` and `develop`.
- **feat/infra-scaffold**: Initial repo, Docker, Deno 2 + Vite, FastAPI uv setup.
- **feat/db-auth**: Supabase schema, migrations, RLS policies, auth middleware.
- **feat/node-discovery**: Meridian node type discovery + registry + issue tracker.
- **feat/graph-validation**: Graph model validation, port compatibility, feedback.
- **feat/graph-crud-api**: Graph CRUD endpoints, permissions, pagination.
- **feat/sharing-collab**: Sharing endpoints, permissions, gallery.
- **feat/frontend-core**: Routing, Zustand, React Query, auth context, UI shell.
- **feat/graph-canvas**: React Flow canvas, custom nodes/edges, interactions.
- **feat/node-palette**: Palette, drag-and-drop, search, categorization.
- **feat/properties-panel**: Dynamic forms, validation, help text.
- **feat/execution-api-ws**: Execution API, WebSocket updates, controls.
- **feat/message-tracing**: Trace viewer, path viz, analytics.
- **feat/persistence-sharing-ui**: Save/load, import/export, templates, gallery UI.
- **perf/optimizations**: Bundle size, caching, DB query tuning.
- **docs/site**: Documentation, examples, onboarding flows.

Branch naming convention: `<type>/<scope>[-detail]` where type ∈ {feat, fix, chore, refactor, perf, docs, test, hotfix, release}.

## Project Structure
```
meridian-studio/
├── frontend/          # React + Vite frontend
├── backend/           # FastAPI backend
├── docker-compose.yml # Development environment
├── README.md
└── .env.example
```

- [ ] 1. Set up project infrastructure and development environment
- [x] Create new repository structure with separate `frontend` and `backend` directories
- [x] Set up uv environment
- [ ] Verify and install `meridian-runtime` from PyPI in backend (pending package verification)
- [x] Create Docker Compose configuration with all services (frontend, backend, Supabase, Redis)
- [x] Set up Vite + React + TypeScript frontend project using Deno 2 tasks for dev/build
- [x] Add Tailwind CSS to the frontend scaffold
- [x] Add shadcn/ui to the frontend scaffold (base components wired)
- [x] Create FastAPI backend project with modular structure (<200 LOC)
- [x] Configure development scripts and environment variables
- [x] Add commit hooks for frequent commits (pre-commit configured)
- [x] Start local Supabase stack via CLI and create `.env` for local dev
  - _Requirements: 12.1, 12.2, 12.3_

- [ ] 2. Implement core database schema and authentication
- [ ] 2.1 Create Supabase database schema and migrations
- [x] Write SQL migrations for users, graphs, graph_executions, and shared_graphs tables
- [x] Add message_traces and edge_metrics tables for real-time communication tracking
- [x] Set up Row Level Security (RLS) policies for data access control (0002_rls.sql)
- [x] Create database indexes for performance optimization including message tracing queries
- [x] Apply migrations locally via Supabase CLI
  - _Requirements: 9.3, 10.2, 11.2, 13.1, 14.1, 15.1_

- [ ] 2.2 Implement authentication system
  - [x] Set up Supabase local stack and JWT secret/keys
  - [ ] Configure Supabase authentication providers (email/password, social)
  - [x] Scaffold frontend auth UI (email/password form)
  - [x] Create FastAPI JWT auth dependency and protected route (`/me`)
  - [ ] Implement user session management
  - [x] Add authentication guards for protected API endpoints (start)
  - _Requirements: 9.1, 9.2_

- [ ] 2.3 Create user management API endpoints
  - Implement user registration and login endpoints
  - [x] Add user profile management functionality
  - Create user session handling and logout functionality
  - Write unit tests for authentication flows
  - _Requirements: 9.1, 9.2, 9.4_

- [ ] 3. Build core graph management backend
- [x] 3.1 Implement graph data models and validation
  - Create Pydantic models for GraphDefinition, NodeDefinition, EdgeDefinition
  - Implement graph validation logic with Meridian node type checking
  - Add graph serialization and deserialization functions
  - Write unit tests for data model validation
  - _Requirements: 4.1, 4.2, 6.1_

- [ ] 3.2 Create graph CRUD API endpoints
  - [x] Implement create, read, update, delete endpoints for graphs
  - Add graph listing with pagination and filtering
  - Implement graph ownership and permission checking
  - Add graph metadata management (tags, descriptions)
  - _Requirements: 4.1, 4.3, 9.3, 9.4_

- [ ] 3.3 Implement graph sharing and collaboration features
  - [x] Create graph sharing API endpoints with permission levels
  - Implement public graph discovery and gallery functionality
  - Add collaborative editing with conflict resolution
  - Write tests for sharing permissions and access control
  - _Requirements: 10.1, 10.2, 10.3, 10.4_

- [ ] 4. Integrate Meridian Runtime for node discovery and validation
- [ ] 4.1 Create Meridian node type discovery system with issue tracking
  - Implement automatic discovery of all built-in Meridian node types
  - Extract node metadata including inputs, outputs, and property schemas
  - Create node type registry with categorization and search
  - Generate node documentation and examples automatically
  - Implement MeridianIssueTracker for collecting integration pain points
  - Document any missing metadata, unclear APIs, or discovery limitations
  - _Requirements: 8.1, 1.3_

- [ ] 4.2 Implement graph validation with Meridian integration and feedback collection
  - Create graph structure validation using Meridian's validation system
  - Implement port compatibility checking for edge connections
  - Add real-time validation feedback during graph construction
  - [x] Create validation error reporting with specific node/edge locations
  - Track validation inconsistencies, missing rules, or unclear error messages
  - Document edge cases where Meridian validation could be improved
  - _Requirements: 6.1, 6.2, 6.3, 8.2_

- [ ] 4.3 Build graph execution engine with message tracing and observability feedback
  - Implement graph execution using Meridian Scheduler with observability hooks
  - Create execution context management and resource allocation
  - Add real-time message tracing and communication monitoring
  - Implement message path tracking and causal relationship detection
  - Store execution results, message traces, and performance metrics
  - Document missing observability hooks, insufficient error context, or tracing limitations
  - Track performance impact of observability and suggest optimizations
  - _Requirements: 5.1, 5.2, 5.3, 11.1, 13.1, 13.2, 14.1, 14.2_

- [ ] 5. Develop frontend core infrastructure
- [ ] 5.1 Set up React application with routing and state management
  - Configure React Router for application navigation
  - Set up Zustand for global state management
  - Implement React Query for server state and caching
  - Create authentication context and protected routes
  - Configure Deno 2 tasks (`deno.jsonc`) and npm interop for Vite/React
  - _Requirements: 13.1, 9.2_

- [ ] 5.2 Create base UI components and layout
  - Implement main application layout with navigation
  - Create reusable UI components using shadcn/ui
  - Set up responsive design system with Tailwind CSS
  - Implement loading states and error boundaries
  - _Requirements: 13.1, 13.2, 13.3, 13.4_

- [ ] 5.3 Implement authentication UI components
  - Create login and registration forms with validation
  - Implement social login buttons and flows
  - Add user profile management interface
  - Create authentication error handling and feedback
  - _Requirements: 9.1, 9.2_

- [ ] 6. Build graph visualization and editing interface
- [ ] 6.1 Implement React Flow graph canvas
  - Set up React Flow with custom node and edge components
  - Create graph canvas with zoom, pan, and selection functionality
  - Implement node positioning and layout algorithms
  - Add canvas interaction handlers for graph editing
  - _Requirements: 1.1, 1.2, 1.4, 7.3_

- [ ] 6.2 Create custom node components for Meridian types
  - Design and implement visual representations for different node types
  - Create node input/output port visualizations with type indicators
  - Implement node status indicators for execution states
  - Add node selection and highlighting functionality
  - _Requirements: 1.1, 5.2, 8.1_

- [ ] 6.3 Implement enhanced edge connection system with real-time visualization
  - Create edge connection logic with port compatibility validation
  - Implement visual edge routing and styling with message flow animations
  - Add edge selection and deletion functionality with message trace access
  - Create edge property editing (capacity, policy, priority) with performance impact preview
  - Implement real-time edge status indicators (idle, active, blocked, bottleneck)
  - _Requirements: 2.1, 2.2, 2.3, 2.4, 13.1, 13.4, 15.3_

- [ ] 7. Develop node palette and property management
- [ ] 7.1 Create node palette with search and categorization
  - Implement draggable node palette with all Meridian node types
  - Add search and filtering functionality for node discovery
  - Create node categorization and grouping
  - Implement drag-and-drop node creation on canvas
  - _Requirements: 1.1, 1.3, 8.1_

- [ ] 7.2 Build dynamic properties panel
  - Create property editing interface for selected nodes
  - Implement dynamic form generation based on node schemas
  - Add property validation with real-time feedback
  - Create property help text and documentation integration
  - _Requirements: 3.1, 3.2, 3.3, 8.2_

- [ ] 7.3 Implement graph organization features
  - Add node grouping and subgraph creation functionality
  - Implement auto-layout algorithms for graph organization
  - Create graph minimap and navigation tools
  - Add graph search and filtering capabilities
  - _Requirements: 7.1, 7.2, 7.4_

- [ ] 8. Build graph execution and monitoring system
- [ ] 8.1 Create execution control interface
  - Implement execution control buttons (start, stop, pause)
  - Create execution parameter configuration interface
  - Add execution status display and progress indicators
  - Implement execution queue management for multiple graphs
  - _Requirements: 5.1, 5.2_

- [ ] 8.2 Implement real-time execution monitoring and message visualization
  - Set up WebSocket connection for real-time execution updates and message tracing
  - Create animated visual indicators showing messages flowing through edges
  - Implement real-time metrics display with throughput, latency, and queue depth
  - Add bottleneck detection and performance warning indicators
  - Create execution error highlighting and debugging tools
  - _Requirements: 5.2, 5.3, 5.4, 13.1, 13.2, 13.4, 15.1, 15.3_

- [ ] 8.3 Build execution history and results management
  - Create execution history interface with filtering and search
  - Implement execution results visualization and export
  - Add execution comparison tools for performance analysis
  - Create execution error analysis and debugging interface
  - _Requirements: 11.1, 11.2, 11.3, 11.4_

- [ ] 8.4 Implement message tracing and communication analytics
  - Create message trace viewer component for detailed edge inspection
  - Implement message path visualization showing complete data flow routes
  - Build communication analytics dashboard with real-time charts and metrics
  - Add message payload inspection and transformation tracking
  - Create bottleneck analysis and performance optimization suggestions
  - _Requirements: 13.1, 13.2, 13.3, 14.1, 14.2, 14.3, 15.1, 15.2, 15.3_

- [ ] 8.5 Build message tracing API endpoints
  - Implement API endpoints for retrieving message traces by execution and edge
  - Create message path tracking API for complete journey visualization
  - Add communication analytics API with time-range filtering
  - Implement real-time WebSocket events for message flow updates
  - Create message search and filtering capabilities
  - _Requirements: 13.3, 14.1, 14.4, 15.2, 15.4_

- [ ] 9. Implement graph persistence and sharing
- [ ] 9.1 Create graph save and load functionality
  - Implement automatic graph saving with conflict resolution
  - Create manual save/load with version management
  - Add graph import/export functionality with validation
  - Implement graph templates and example library
  - _Requirements: 4.1, 4.2, 4.3, 4.4_

- [ ] 9.2 Build graph sharing and collaboration features
  - Create graph sharing interface with permission management
  - Implement public graph gallery with search and filtering
  - Add collaborative editing with real-time synchronization
  - Create graph forking and version control functionality
  - _Requirements: 10.1, 10.2, 10.3, 10.4_

- [ ] 9.3 Implement graph discovery and community features
  - Create public graph browsing and discovery interface
  - Add graph rating and commenting system
  - Implement graph collections and favorites
  - Create user profiles with graph portfolios
  - _Requirements: 10.4_

- [ ] 10. Add advanced features and optimizations
- [ ] 10.1 Implement advanced graph validation and debugging
  - Create comprehensive graph validation with detailed error reporting
  - Add graph debugging tools with step-through execution
  - Implement graph performance analysis and optimization suggestions
  - Create graph testing framework with unit test generation
  - _Requirements: 6.1, 6.2, 6.3, 6.4_

- [ ] 10.2 Build graph analytics and monitoring
  - Implement graph execution analytics and performance metrics
  - Create graph usage tracking and optimization recommendations
  - Add graph health monitoring with alerting
  - Implement graph resource usage analysis and optimization
  - _Requirements: 11.1, 11.4_

- [ ] 10.3 Create advanced UI features and accessibility
  - Implement keyboard shortcuts and accessibility features
  - Add graph visualization customization options
  - Create advanced graph layout and styling tools
  - Implement graph printing and presentation modes
  - _Requirements: 13.2, 13.4_

- [ ] 11. Testing and quality assurance
- [ ] 11.1 Write integration tests for core functionality
  - Create integration tests for API endpoints with real database operations
  - Write integration tests for Meridian Runtime graph execution workflows
  - Implement integration tests for authentication flows with Supabase
  - Add integration tests for WebSocket real-time communication
  - _Requirements: All requirements_

- [ ] 11.2 Implement end-to-end user journey tests
  - Create end-to-end tests for complete graph creation and execution workflows
  - Write end-to-end tests for user registration, login, and graph sharing
  - Implement browser-based tests for graph visualization and editing
  - Add performance tests for large graph execution and real-time updates
  - _Requirements: All requirements_

- [ ] 11.3 Add error handling and resilience testing
  - Implement comprehensive error handling throughout the application
  - Create error recovery mechanisms and graceful degradation
  - Add network failure handling and offline capabilities
  - Implement security testing and vulnerability assessment
  - _Requirements: All requirements_

- [ ] 12. Documentation and deployment preparation
- [ ] 12.1 Create comprehensive documentation and Meridian Runtime feedback report
  - Write user documentation with tutorials and examples
  - Create developer documentation for API and architecture
  - Implement in-app help system and onboarding flow
  - Add graph examples and template library
  - Compile comprehensive Meridian Runtime integration report with all collected issues
  - Create improvement suggestions and enhancement requests for main repo
  - Document successful integration patterns and best practices
  - _Requirements: All requirements_

- [ ] 12.2 Prepare production deployment configuration
  - Create production Docker configurations with security hardening
  - Set up CI/CD pipeline for automated testing and deployment
  - Implement monitoring and logging for production environment
  - Create backup and disaster recovery procedures
  - _Requirements: 12.1, 12.3, 12.4_

- [ ] 12.3 Performance optimization and scalability
  - Optimize frontend bundle size and loading performance
  - Implement backend caching and database query optimization
  - Add horizontal scaling configuration for high availability
  - Create performance monitoring and alerting systems
  - _Requirements: 12.4, 13.4_
