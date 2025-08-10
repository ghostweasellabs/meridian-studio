-- Core schema for Meridian Studio

CREATE EXTENSION IF NOT EXISTS pgcrypto;

-- users
CREATE TABLE IF NOT EXISTS users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email VARCHAR(255) UNIQUE NOT NULL,
    name VARCHAR(255),
    avatar_url TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- graphs
CREATE TABLE IF NOT EXISTS graphs (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    definition JSONB NOT NULL,
    is_public BOOLEAN DEFAULT FALSE,
    tags TEXT[] DEFAULT '{}',
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);
CREATE INDEX IF NOT EXISTS idx_graphs_user_id ON graphs(user_id);
CREATE INDEX IF NOT EXISTS idx_graphs_tags ON graphs USING GIN(tags);
CREATE INDEX IF NOT EXISTS idx_graphs_public ON graphs(is_public) WHERE is_public = TRUE;

-- graph_executions
CREATE TABLE IF NOT EXISTS graph_executions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    graph_id UUID NOT NULL REFERENCES graphs(id) ON DELETE CASCADE,
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    status VARCHAR(50) NOT NULL DEFAULT 'pending',
    started_at TIMESTAMPTZ,
    completed_at TIMESTAMPTZ,
    results JSONB,
    error_message TEXT,
    execution_metrics JSONB,
    communication_analytics JSONB,
    created_at TIMESTAMPTZ DEFAULT NOW()
);
CREATE INDEX IF NOT EXISTS idx_executions_graph_id ON graph_executions(graph_id);
CREATE INDEX IF NOT EXISTS idx_executions_user_id ON graph_executions(user_id);
CREATE INDEX IF NOT EXISTS idx_executions_status ON graph_executions(status);

-- message_traces
CREATE TABLE IF NOT EXISTS message_traces (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    execution_id UUID NOT NULL REFERENCES graph_executions(id) ON DELETE CASCADE,
    message_id VARCHAR(255) NOT NULL,
    timestamp TIMESTAMPTZ NOT NULL,
    message_type VARCHAR(20) NOT NULL,
    payload JSONB,
    metadata JSONB DEFAULT '{}',
    source_node VARCHAR(255) NOT NULL,
    target_node VARCHAR(255) NOT NULL,
    edge_id VARCHAR(255) NOT NULL,
    processing_time FLOAT DEFAULT 0,
    queue_time FLOAT DEFAULT 0,
    created_at TIMESTAMPTZ DEFAULT NOW()
);
CREATE INDEX IF NOT EXISTS idx_message_traces_execution_id ON message_traces(execution_id);
CREATE INDEX IF NOT EXISTS idx_message_traces_message_id ON message_traces(message_id);
CREATE INDEX IF NOT EXISTS idx_message_traces_timestamp ON message_traces(timestamp);
CREATE INDEX IF NOT EXISTS idx_message_traces_edge_id ON message_traces(edge_id);

-- edge_metrics
CREATE TABLE IF NOT EXISTS edge_metrics (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    execution_id UUID NOT NULL REFERENCES graph_executions(id) ON DELETE CASCADE,
    edge_id VARCHAR(255) NOT NULL,
    timestamp TIMESTAMPTZ NOT NULL,
    throughput FLOAT DEFAULT 0,
    latency FLOAT DEFAULT 0,
    queue_depth INTEGER DEFAULT 0,
    dropped_messages INTEGER DEFAULT 0,
    created_at TIMESTAMPTZ DEFAULT NOW()
);
CREATE INDEX IF NOT EXISTS idx_edge_metrics_execution_id ON edge_metrics(execution_id);
CREATE INDEX IF NOT EXISTS idx_edge_metrics_edge_id ON edge_metrics(edge_id);
CREATE INDEX IF NOT EXISTS idx_edge_metrics_timestamp ON edge_metrics(timestamp);

-- shared_graphs
CREATE TABLE IF NOT EXISTS shared_graphs (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    graph_id UUID NOT NULL REFERENCES graphs(id) ON DELETE CASCADE,
    shared_by UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    shared_with UUID REFERENCES users(id) ON DELETE CASCADE,
    permissions VARCHAR(50) NOT NULL DEFAULT 'read',
    expires_at TIMESTAMPTZ,
    created_at TIMESTAMPTZ DEFAULT NOW()
);
CREATE INDEX IF NOT EXISTS idx_shared_graphs_graph_id ON shared_graphs(graph_id);
CREATE INDEX IF NOT EXISTS idx_shared_graphs_shared_with ON shared_graphs(shared_with);


